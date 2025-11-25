# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 15:01:36 2025

@author: ELINA
"""

# admin.py
import streamlit as st
import pandas as pd
from database import load_tenants, save_tenants, load_messages, save_messages, load_payments, save_payments, next_id, timestamp_now
from agreement_generator import generate_agreement
from message_service import send_email, send_sms
import os
from dotenv import load_dotenv
load_dotenv()
import database

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

def admin_portal():
    st.header("Admin Panel (Umuyobozi)")

    pwd = st.text_input("Injiza ijambo ry'ibanga (password)", type="password")
    if pwd != ADMIN_PASSWORD:
        st.warning("Ijambo ry'ibanga si ryo")
        return

    st.success("Murakaza neza, Administrator")
    tenants = load_tenants()

    menu = st.sidebar.selectbox("Hitamo icyo ushaka gukora", ["Kongeramo umukiriya", "Reba abakiriya", "Ubutumwa", "Imyishyurire", "Kohereza SMS/Email"])

    if menu == "Kongeramo umukiriya":
        with st.form("add_tenant"):
            st.write("Andika amakuru y'umukiriya")
            fullname = st.text_input("Amazina yose")
            id_number = st.text_input("Indangamuntu")
            phone = st.text_input("Nomero ya telefone")
            sex = st.selectbox("Igitsina", ["Gabo","Gore"])
            people = st.number_input("Umubare w'abantu batuye mu nzu", min_value=1, value=1)
            house_status = st.text_input("Status y'inzu (ex: Icyumba 1)")
            start_date = st.date_input("Itariki y'itangira")
            rent = st.number_input("Amafaranga y'ubukode buri kwezi", min_value=0)
            submitted = st.form_submit_button("Bika umukiriya")
            if submitted:
                new_tenants = tenants.copy()
                nid = str(int(new_tenants["tenant_id"].astype(int).max())+1) if not new_tenants.empty else "1"
                agreement_path = generate_agreement({
                    "tenant_id": nid,
                    "fullname": fullname,
                    "id_number": id_number,
                    "phone": phone,
                    "sex": sex,
                    "people": str(people),
                    "house_status": house_status,
                    "start_date": str(start_date),
                    "rent": str(rent)
                }, {"name":"Nyir'inzu", "phone":"0780000000", "email":"nyiri@example.com"})
                new_row = {
                    "tenant_id": nid,
                    "fullname": fullname,
                    "id_number": id_number,
                    "phone": phone,
                    "sex": sex,
                    "people": str(people),
                    "house_status": house_status,
                    "start_date": str(start_date),
                    "rent": str(rent),
                    "username": phone,
                    "password": "1234",
                    "agreement_file": agreement_path,
                    "created_at": timestamp_now()
                }
                new_tenants = pd.concat([new_tenants, pd.DataFrame([new_row])], ignore_index=True)
                save_tenants(new_tenants)
                st.success("Umukiriya yongewe kandi Kontrare yanditswe (PDF).")

    if menu == "Reba abakiriya":
        st.subheader("Urutonde rw'abakiriya")
        tenants = load_tenants()
        st.dataframe(tenants)

        if st.button("Refresha"):
            tenants = load_tenants()
            st.experimental_rerun()

    if menu == "Ubutumwa":
        st.subheader("Ubutumwa bwoherejwe n'abakiriya")
        msgs = load_messages()
        if msgs.empty:
            st.info("Nta butumwa")
        else:
            st.dataframe(msgs)
            sel = st.text_input("Injiza message_id yo gusubizaho (ex: 1)")
            reply = st.text_area("Andika igisubizo hano")
            if st.button("Ohereza Reply"):
                if not sel.strip():
                    st.warning("Injiza message_id")
                else:
                    msgs = msgs.copy()
                    idx = msgs.index[msgs["message_id"]==sel].tolist()
                    if not idx:
                        st.error("Message id ntiboneka")
                    else:
                        i = idx[0]
                        msgs.at[i,"reply"] = reply
                        msgs.at[i,"date_reply"] = timestamp_now()
                        msgs.at[i,"status"] = "replyed"
                        save_messages(msgs)
                        # send email or sms if tenant has contact
                        tenants = load_tenants()
                        tenant = tenants[tenants["tenant_id"]==msgs.at[i,"tenant_id"]]
                        if not tenant.empty:
                            t = tenant.iloc[0]
                            # try email first (if you store tenant email in future)
                            # Here we'll send SMS
                            ok, info = send_sms(t["phone"], f"Reply from Landlord: {reply}")
                            if ok:
                                st.success("Reply saved kandi SMS yoherejwe")
                            else:
                                st.warning(f"Reply saved ariko SMS ntibyagenze: {info}")

    if menu == "Imyishyurire":
        st.subheader("Gucunga imyishyurire")
        payments = load_payments()
        tenants = load_tenants()
        st.dataframe(payments)
        with st.form("add_payment"):
            tenant_id = st.text_input("Tenant ID")
            month = st.text_input("Ukwezi (ex: 2025-11)")
            status = st.selectbox("Status", ["Yishyuye","Yatinze","Ntabwo Yishyuye"])
            paid_date = st.date_input("Itariki yishyuwe")
            if st.form_submit_button("Ongeramo Payment"):
                payments = payments.copy()
                pid = str(int(payments["payment_id"].astype(int).max())+1) if not payments.empty else "1"
                new_row = {"payment_id":pid,"tenant_id":str(tenant_id),"month":month,"status":status,"paid_date":str(paid_date)}
                payments = pd.concat([payments, pd.DataFrame([new_row])], ignore_index=True)
                save_payments(payments)
                st.success("Payment yanditswe")

    if menu == "Kohereza SMS/Email":
        st.subheader("Ohereza SMS cyangwa Email by'intangarugero")
        phone = st.text_input("Nomero ya Tel")
        text = st.text_area("Igitekerezo / Ubutumwa")
        if st.button("Ohereza SMS sample"):
            ok, info = send_sms(phone, text)
            if ok:
                st.success("SMS yoherejwe")
            else:
                st.error(f"SMS ntiyoherejwe: {info}")
        email = st.text_input("Email (cyangwa usige ubusa)")
        if st.button("Ohereza Email sample"):
            ok, info = send_email(email, "Ubutumwa bwa Administrator", text)
            if ok:
                st.success("Email yoherejwe")
            else:
                st.error(f"Email ntiyoherejwe: {info}")
