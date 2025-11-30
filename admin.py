# -*- coding: utf-8 -*-
"""
Admin portal — saves tenant files to tenant_files/ and lets admin download all files.
"""

import streamlit as st
import pandas as pd
import json
import os
from database import (
    load_tenants, save_tenants,
    load_messages, save_messages,
    load_payments, save_payments,
    timestamp_now
)
from agreement_generator import generate_agreement
from message_service import send_email, send_sms
from dotenv import load_dotenv
load_dotenv()

# -----------------------------
# CONFIGURATION
# -----------------------------
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
TENANT_FILES_DIR = "tenant_files"
os.makedirs(TENANT_FILES_DIR, exist_ok=True)

LANDLORD_INFO = {
    "name": "NTAKIRUTIMANA EZECHIEL",
    "phone": "0785042128",
    "email": "offliqz@gmail.com"
}

# -------------------------------------------------
# FUNCTION: SAVE TENANT PROFILE AS JSON FILE
# -------------------------------------------------
def save_tenant_profile_file(tenant_dict):
    """Save tenant profile as JSON in tenant_files/{phone}.json"""
    phone = tenant_dict.get("phone", "unknown")
    filename = os.path.join(TENANT_FILES_DIR, f"{phone}.json")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(tenant_dict, f, ensure_ascii=False, indent=4)

    return filename


# -------------------------------------------------
# ADMIN PORTAL
# -------------------------------------------------
def admin_portal():
    st.header("Admin (Umuyobozi)")

    # Password
    pwd = st.text_input("Injiza ijambo ry'ibanga (password)", type="password")
    if pwd != ADMIN_PASSWORD:
        st.warning("⚠️ Ijambo ry'ibanga si ryo!")
        return

    st.success("Murakaza neza, Administrator 👑")
    tenants = load_tenants()

    # Menu
    menu = st.sidebar.selectbox("Hitamo icyo ushaka gukora", [
        "Kongeramo umukiriya",
        "Reba abakiriya",
        "Ubutumwa",
        "Imyishyurire",
        "Dosiye z'Abakiriya",
        "Kohereza SMS/Email"
    ])

    # -------------------------------------------------
    # 1) ADD TENANT
    # -------------------------------------------------
    if menu == "Kongeramo umukiriya":
        with st.form("add_tenant"):
            st.subheader("➕ Kongeramo umukiriya mushya")

            fullname = st.text_input("Amazina yose")
            id_number = st.text_input("Indangamuntu")
            phone = st.text_input("Nomero ya telefone")
            sex = st.selectbox("Igitsina", ["Gabo", "Gore"])
            people = st.number_input("Umubare w'abantu batuye mu nzu", min_value=1, value=1)
            house_status = st.text_input("Ubwoko bw'inzu")
            start_date = st.date_input("Itariki y'itangira gutura")
            rent = st.number_input("Ubukode buri kwezi (FRW)", min_value=0)

            submitted = st.form_submit_button("💾 Bika umukiriya")

            if submitted:
                new_tenants = tenants.copy()

                # Automatic tenant ID
                nid = str(int(new_tenants["tenant_id"].astype(int).max()) + 1) if not new_tenants.empty else "1"

                # Build tenant dict
                tenant_dict = {
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
                    "created_at": timestamp_now()
                }

                # -----------------------------------------------
                # Generate PDF AGREEMENT
                # -----------------------------------------------
                agreement_path = generate_agreement(tenant_dict, LANDLORD_INFO)
                tenant_dict["agreement_file"] = agreement_path

                # -----------------------------------------------
                # SAVE TENANT PROFILE JSON
                # -----------------------------------------------
                profile_path = save_tenant_profile_file(tenant_dict)

                # Save to main database
                new_row = tenant_dict.copy()
                new_row["agreement_file"] = str(agreement_path)

                new_tenants = pd.concat([new_tenants, pd.DataFrame([new_row])], ignore_index=True)
                save_tenants(new_tenants)

                st.success("🎉 Umukiriya yongewe kandi amasezerano (PDF) yarakozwe.")
                st.info(f"📁 Files saved:\n- {agreement_path}\n- {profile_path}")

    # -------------------------------------------------
    # 2) VIEW TENANTS
    # -------------------------------------------------
    if menu == "Reba abakiriya":
        st.subheader("📋 Urutonde rw'abakiriya")
        tenants = load_tenants()
        st.dataframe(tenants)

        if st.button("🔄 Refresha"):
            st.experimental_rerun()

    # -------------------------------------------------
    # 3) MESSAGE CENTER
    # -------------------------------------------------
    if menu == "Ubutumwa":
        st.subheader("📨 Ubutumwa bwoherejwe n'abakiriya")

        msgs = load_messages()
        if msgs.empty:
            st.info("Nta butumwa buraboneka.")
        else:
            st.dataframe(msgs)

            sel = st.text_input("Injiza message_id ushaka gusubiza")
            reply = st.text_area("Andika igisubizo hano")

            if st.button("📩 Ohereza igisubizo"):
                if not sel.strip():
                    st.warning("Injiza message_id neza.")
                else:
                    msgs = msgs.copy()
                    idx = msgs.index[msgs["message_id"] == sel].tolist()

                    if not idx:
                        st.error("Message ID ntiboneka.")
                    else:
                        i = idx[0]
                        msgs.at[i, "reply"] = reply
                        msgs.at[i, "date_reply"] = timestamp_now()
                        msgs.at[i, "status"] = "replyed"
                        save_messages(msgs)

                        tenants = load_tenants()
                        tenant = tenants[tenants["tenant_id"] == msgs.at[i, "tenant_id"]]

                        if not tenant.empty:
                            t = tenant.iloc[0]
                            ok, info = send_sms(t["phone"], f"Igisubizo cya Landlord: {reply}")

                            if ok:
                                st.success("Ubutumwa bwasubijwe kandi SMS yoheretswe.")
                            else:
                                st.warning(f"Reply yabikwe ariko SMS ntiyoherejwe: {info}")

    # -------------------------------------------------
    # 4) PAYMENT MANAGEMENT
    # -------------------------------------------------
    if menu == "Imyishyurire":
        st.subheader("💰 Imyishyurire y'abakiriya")

        payments = load_payments()
        st.dataframe(payments)

        with st.form("add_payment"):
            tenant_id = st.text_input("Tenant ID")
            month = st.text_input("Ukwezi (ex: 2025-11)")
            status = st.selectbox("Status y'ubwishyu", ["Yishyuye", "Yatinze", "Ntabwo Yishyuye"])
            paid_date = st.date_input("Itariki yishyuwe")

            if st.form_submit_button("➕ Ongeramo ubwishyu"):
                payments = payments.copy()
                pid = str(int(payments["payment_id"].astype(int).max()) + 1) if not payments.empty else "1"

                new_row = {
                    "payment_id": pid,
                    "tenant_id": str(tenant_id),
                    "month": month,
                    "status": status,
                    "paid_date": str(paid_date)
                }

                payments = pd.concat([payments, pd.DataFrame([new_row])], ignore_index=True)
                save_payments(payments)

                st.success("Uburyo bw'ubwishyu bwongewe.")

    # -------------------------------------------------
    # 5) TENANT FILES — ADMIN
    # -------------------------------------------------
    if menu == "Dosiye z'Abakiriya":
        st.subheader("📂 Dosiye zose z'abakiriya")

        files = sorted(os.listdir(TENANT_FILES_DIR))

        if not files:
            st.info("Nta dosiye ibitswe muri tenant_files/")
        else:
            for f in files:
                path = os.path.join(TENANT_FILES_DIR, f)
                st.write("•", f)

                with open(path, "rb") as file:
                    st.download_button(
                        label=f"⬇️ Kuramo {f}",
                        data=file,
                        file_name=f
                    )

    # -------------------------------------------------
    # 6) SEND SMS / EMAIL
    # -------------------------------------------------
    if menu == "Kohereza SMS/Email":
        st.subheader("📤 Ohereza SMS cyangwa Email")

        phone = st.text_input("Nomero ya telefone")
        text = st.text_area("Ubutumwa")

        if st.button("📨 Ohereza SMS"):
            ok, info = send_sms(phone, text)
            if ok:
                st.success("SMS yoherejwe!")
            else:
                st.error(f"SMS ntiyoherejwe: {info}")

        email = st.text_input("Email")

        if st.button("📧 Ohereza Email"):
            ok, info = send_email(email, "Ubutumwa bwa Administrator", text)
            if ok:
                st.success("Email yoherejwe!")
            else:
                st.error(f"Email ntiyoherejwe: {info}")
