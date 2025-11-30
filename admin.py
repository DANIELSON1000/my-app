# -*- coding: utf-8 -*-
"""
Admin portal — manages tenants, payments, messages, and file downloads.
All tenant files are stored securely inside tenant_files/
"""
import streamlit as st
import pandas as pd
import json
import os

from database import (
    load_tenants,
    save_tenants,
    load_messages,
    save_messages,
    load_payments,
    save_payments,
    timestamp_now
)

from agreement_generator import generate_agreement
from message_service import send_email, send_sms

from dotenv import load_dotenv
load_dotenv()

# Admin password stored in .env
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

# Folder where tenant JSON + PDF will be saved
TENANT_FILES_DIR = "tenant_files"
os.makedirs(TENANT_FILES_DIR, exist_ok=True)


# 🔵 SAVE TENANT PROFILE INTO JSON FILE
def save_tenant_profile_file(tenant_dict):
    phone = tenant_dict.get("phone", "unknown")
    file_path = os.path.join(TENANT_FILES_DIR, f"{phone}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(tenant_dict, f, ensure_ascii=False, indent=4)

    return file_path



# ======================================================================================
# ADMIN PORTAL
# ======================================================================================
def admin_portal():

    st.header("👨‍💼 Ubuyobozi — Admin Portal")

    # ------------------------
    # LOGIN
    # ------------------------
    pwd = st.text_input("Injiza ijambo ry'ibanga (Admin Password)", type="password")
    if pwd != ADMIN_PASSWORD:
        st.warning("⚠️ Ijambo ry'ibanga si ryo")
        return

    st.success("Murakaza neza, Administrator 👍")
    tenants = load_tenants()

    # ------------------------
    # MENU
    # ------------------------
    menu = st.sidebar.selectbox("Hitamo icyo ushaka gukora", [
        "Kongeramo umukiriya",
        "Reba abakiriya",
        "Ubutumwa",
        "Imyishyurire",
        "Dosiye z'Abakiriya",
        "Kohereza SMS/Email"
    ])

    # ======================================================================================
    # 1) ADD TENANT
    # ======================================================================================
    if menu == "Kongeramo umukiriya":
        st.subheader("🧍‍♂️ Kongeramo umukiriya mushya")

        with st.form("add_tenant"):
            fullname = st.text_input("Amazina yose y'umukiriya")
            id_number = st.text_input("Indangamuntu (ID)")
            phone = st.text_input("Nomero ya telefone")
            sex = st.selectbox("Igitsina", ["Gabo", "Gore"])
            people = st.number_input("Abantu batuye mu nzu", min_value=1, value=1)
            house_status = st.text_input("Ubwoko bw'inzu")
            start_date = st.date_input("Itariki atangiye kubamo")
            rent = st.number_input("Amafaranga y'ubukode (buri kwezi)", min_value=0)

            submitted = st.form_submit_button("Bika umukiriya")

            if submitted:
                new_tenants = tenants.copy()

                # generate new tenant ID
                new_id = (
                    str(int(new_tenants["tenant_id"].astype(int).max()) + 1)
                    if not new_tenants.empty else "1"
                )

                tenant_dict = {
                    "tenant_id": new_id,
                    "fullname": fullname,
                    "id_number": id_number,
                    "phone": phone,
                    "sex": sex,
                    "people": str(people),
                    "house_status": house_status,
                    "start_date": str(start_date),
                    "rent": str(rent),
                    "username": phone,
                    "password": "1234",  # default password
                    "created_at": timestamp_now()
                }

                # 1) Generate agreement PDF
                AGREEMENT_LANDLORD = {
                    "name": "NTAKIRUTIMANA EZECHIEL",
                    "phone": "0785042128",
                    "email": "offliqz@gmail.com"
                }

                pdf_path = generate_agreement(tenant_dict, AGREEMENT_LANDLORD)
                tenant_dict["agreement_file"] = pdf_path

                # 2) Save JSON file
                profile_path = save_tenant_profile_file(tenant_dict)

                # 3) Save to tenants database
                new_tenants = pd.concat([new_tenants, pd.DataFrame([tenant_dict])], ignore_index=True)
                save_tenants(new_tenants)

                st.success("Umukiriya yongewe neza!")
                st.info(f"PDF Agreement: {pdf_path}")
                st.info(f"Dosiye JSON: {profile_path}")



    # ======================================================================================
    # 2) VIEW TENANTS
    # ======================================================================================
    if menu == "Reba abakiriya":
        st.subheader("📋 Urutonde rw'abakiriya bose")
        tenants = load_tenants()
        st.dataframe(tenants)

        if st.button("🔄 Refresha"):
            st.experimental_rerun()



    # ======================================================================================
    # 3) MESSAGES
    # ======================================================================================
    if menu == "Ubutumwa":
        st.subheader("✉️ Ubutumwa bw'abakiriya")

        msgs = load_messages()
        if msgs.empty:
            st.info("Nta butumwa buraboneka ubu.")
        else:
            st.dataframe(msgs)

            sel = st.text_input("Andika message_id ushaka gusubiza")
            reply = st.text_area("Andika igisubizo hano")

            if st.button("Ohereza Igisubizo"):
                if not sel.strip():
                    st.warning("Injiza message_id")
                else:
                    msgs = msgs.copy()
                    idx = msgs.index[msgs["message_id"] == sel].tolist()

                    if not idx:
                        st.error("Message ID ntiboneka")
                    else:
                        i = idx[0]
                        msgs.at[i, "reply"] = reply
                        msgs.at[i, "date_reply"] = timestamp_now()
                        msgs.at[i, "status"] = "replyed"
                        save_messages(msgs)

                        tenant_id = msgs.at[i, "tenant_id"]
                        t = tenants[tenants["tenant_id"] == tenant_id].iloc[0]

                        send_sms(t["phone"], f"Igisubizo cya nyir'inzu: {reply}")

                        st.success("Reply yoherejwe neza!")


    # ======================================================================================
    # 4) PAYMENT MANAGEMENT
    # ======================================================================================
    if menu == "Imyishyurire":
        st.subheader("💰 Imyishyurire y'abakiriya")

        payments = load_payments()
        st.dataframe(payments)

        with st.form("add_payment"):
            tenant_id = st.text_input("ID y'umukiriya")
            month = st.text_input("Ukwezi (ex: 2025-01)")
            status = st.selectbox("Status yo kwishyura", ["Yishyuye", "Yatinze", "Ntabwo Yishyuye"])
            paid_date = st.date_input("Itariki yishyuwe")

            if st.form_submit_button("Ongeramo Imyishyurire"):
                new_id = (
                    str(int(payments["payment_id"].astype(int).max()) + 1)
                    if not payments.empty else "1"
                )

                new_row = {
                    "payment_id": new_id,
                    "tenant_id": tenant_id,
                    "month": month,
                    "status": status,
                    "paid_date": str(paid_date),
                }

                payments = pd.concat([payments, pd.DataFrame([new_row])], ignore_index=True)
                save_payments(payments)
                st.success("Imyishyurire yabitswe!")



    # ======================================================================================
    # 5) FILE MANAGEMENT (JSON + PDF + EXCEL EXPORT)
    # ======================================================================================
    if menu == "Dosiye z'Abakiriya":

        st.subheader("📂 Dosiye z'abakiriya")

        tenants = load_tenants()

        # 🟦 DOWNLOAD ALL TENANTS AS EXCEL
        if st.button("⬇️ Kuramo Tenant Database (Excel)"):
            excel_path = os.path.join(TENANT_FILES_DIR, "ALL_TENANTS.xlsx")
            tenants.to_excel(excel_path, index=False)

            with open(excel_path, "rb") as f:
                st.download_button(
                    label="📥 Download ALL_TENANTS.xlsx",
                    data=f,
                    file_name="ALL_TENANTS.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        st.write("---")

        # 🟦 INDIVIDUAL TENANT FILES
        for _, t in tenants.iterrows():
            phone = t["phone"]
            st.write(f"### 👤 {t['fullname']} — {phone}")

            # JSON profile
            json_file = os.path.join(TENANT_FILES_DIR, f"{phone}.json")
            if os.path.exists(json_file):
                with open(json_file, "rb") as f:
                    st.download_button(
                        label="📥 Kuramo Dosiye (JSON)",
                        data=f,
                        file_name=f"{phone}.json",
                        mime="application/json"
                    )

            # PDF agreement
            if "agreement_file" in t and os.path.exists(t["agreement_file"]):
                with open(t["agreement_file"], "rb") as f:
                    st.download_button(
                        label="📥 Kuramo Amasezerano (PDF)",
                        data=f,
                        file_name=os.path.basename(t["agreement_file"]),
                        mime="application/pdf"
                    )

            st.write("---")



    # ======================================================================================
    # 6) SEND SMS & EMAIL MANUALLY
    # ======================================================================================
    if menu == "Kohereza SMS/Email":
        st.subheader("📨 Kohereza ubutumwa")

        phone = st.text_input("Nomero ya telefone")
        text = st.text_area("Ubutumwa bwo kohereza")

        if st.button("Ohereza SMS"):
            ok, info = send_sms(phone, text)
            st.success("SMS yoherejwe!" if ok else f"Error: {info}")

        email = st.text_input("Email")
        if st.button("Ohereza Email"):
            ok, info = send_email(email, "Ubutumwa bwa Nyirinzu", text)
            st.success("Email yoherejwe!" if ok else f"Error: {info}")
