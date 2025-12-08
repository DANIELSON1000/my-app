# -*- coding: utf-8 -*-
"""
Admin portal — manages tenants, payments, messages, reminders, and file downloads.
All tenant files are stored securely inside tenant_files/
"""
import streamlit as st
import pandas as pd
import json
import os
import datetime
from dotenv import load_dotenv

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
        "Payment Monitoring",
        "Dosiye z'Abakiriya",
        "Kohereza SMS/Email"
    ])
# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import os
import json
import datetime

# ===============================================================
# FUNCTIONS
# ===============================================================

TENANT_DIR = "tenant_files"
os.makedirs(TENANT_DIR, exist_ok=True)

def timestamp_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def load_tenants():
    if os.path.exists("tenants.csv"):
        return pd.read_csv("tenants.csv", dtype=str)
    return pd.DataFrame()

def save_tenants(df):
    df.to_csv("tenants.csv", index=False)

def save_tenant_profile_file(data):
    path = os.path.join(TENANT_DIR, f"{data['tenant_id']}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    return path

def generate_agreement(tenant, landlord):
    # Dummy PDF path (you already have your working PDF generator)
    pdf_path = os.path.join(TENANT_DIR, f"{tenant['tenant_id']}_agreement.pdf")
    with open(pdf_path, "w") as f:
        f.write("PDF AGREEMENT PLACEHOLDER")
    return pdf_path


# ===============================================================
# UI MENU
# ===============================================================
menu = st.sidebar.selectbox(
    "MENU",
    ["Kongeramo umukiriya", "Reba abakiriya", "Hindura umukiriya"]
)

tenants = load_tenants()


# ======================================================================================
# 1) ADD TENANT
# ======================================================================================
if menu == "Kongeramo umukiriya":
    st.subheader("🧍‍♂️ Kongeramo umukiriya mushya")

    with st.form("add_tenant"):
        fullname = st.text_input("Amazina yose y'umukiriya")
        id_number = st.text_input("Indangamuntu (ID)")
        phone = st.text_input("Nomero ya telefone")
        email = st.text_input("Email y'umukiriya")
        sex = st.selectbox("Igitsina", ["Gabo", "Gore"])
        people = st.number_input("Abantu batuye mu nzu", min_value=1, value=1)
        house_status = st.text_input("Ubwoko bw'inzu")
        start_date = st.date_input("Itariki atangiye kubamo")
        rent = st.number_input("Amafaranga y'ubukode (buri kwezi)", min_value=0)

        submitted = st.form_submit_button("Bika umukiriya")

        if submitted:
            new_tenants = tenants.copy()
            new_id = str(int(new_tenants["tenant_id"].astype(int).max()) + 1) if not new_tenants.empty else "1"

            tenant_dict = {
                "tenant_id": new_id,
                "fullname": fullname,
                "id_number": id_number,
                "phone": phone,
                "email": email,
                "sex": sex,
                "people": str(people),
                "house_status": house_status,
                "start_date": str(start_date),
                "rent": str(rent),
                "username": phone,
                "password": "1234",
                "created_at": timestamp_now()
            }

            AGREEMENT_LANDLORD = {
                "name": "NTAKIRUTIMANA EZECHIEL",
                "phone": "0785042128",
                "email": "offliqz@gmail.com"
            }

            pdf_path = generate_agreement(tenant_dict, AGREEMENT_LANDLORD)
            tenant_dict["agreement_file"] = pdf_path

            profile_path = save_tenant_profile_file(tenant_dict)

            new_tenants = pd.concat([new_tenants, pd.DataFrame([tenant_dict])], ignore_index=True)
            save_tenants(new_tenants)

            st.success("Umukiriya yongewe neza!")
            st.info(f"PDF Agreement: {pdf_path}")
            st.info(f"Dosiye JSON: {profile_path}")


# ======================================================================================
# 2) VIEW TENANTS
# ======================================================================================
elif menu == "Reba abakiriya":
    st.subheader("📋 Urutonde rw'abakiriya bose")

    tenants = load_tenants()
    st.dataframe(tenants)

    # DELETE TENANT
    st.write("### 🗑️ Gusiba umukiriya")
    tenant_to_delete = st.text_input("Shyiramo Tenant ID yo gusiba")
    if st.button("Siba Tenant"):
        if tenant_to_delete.strip() == "":
            st.warning("Injiza Tenant ID")
        elif tenant_to_delete not in tenants["tenant_id"].astype(str).values:
            st.error("Tenant ID ntiboneka")
        else:
            tenants = tenants[tenants["tenant_id"].astype(str) != tenant_to_delete]
            save_tenants(tenants)
            st.success(f"Tenant ID {tenant_to_delete} yasibwe neza!")


# ======================================================================================
# 3) EDIT TENANT (NEW CLEAN LOGIC)
# ======================================================================================
elif menu == "Hindura umukiriya":

    st.subheader("✏️ Hindura amakuru y'umukiriya")
    st.info("👉 Shyiramo **Tenant ID** ushaka guhindura – mbere nta form ihita igaragara")

    tenant_id_input = st.text_input("Injiza Tenant ID")

    if tenant_id_input:

        if tenant_id_input not in tenants["tenant_id"].astype(str).values:
            st.error("❌ Tenant ntabonetse!")
        else:
            t = tenants[tenants["tenant_id"].astype(str) == tenant_id_input].iloc[0]

            st.success("Tenant yabonetse! Hindura amakuru hepfo:")

            with st.form("edit_tenant_form"):
                fullname = st.text_input("Amazina yose y'umukiriya", t["fullname"])
                id_number = st.text_input("Indangamuntu", t["id_number"])
                phone = st.text_input("Telefoni", t["phone"])
                email = st.text_input("Email", t["email"])
                sex = st.selectbox("Igitsina", ["Gabo", "Gore"], index=0 if t["sex"] == "Gabo" else 1)
                people = st.number_input("Abantu mu nzu", min_value=1, value=int(t["people"]))
                house_status = st.text_input("Ubwoko bw’inzu", t["house_status"])
                start_date = st.date_input("Itariki atangiye", datetime.date.fromisoformat(t["start_date"]))
                rent = st.number_input("Ubukode (buri kwezi)", min_value=0, value=int(t["rent"]))

                submitted = st.form_submit_button("Hindura amakuru")

                if submitted:
                    tenants.loc[
                        tenants["tenant_id"].astype(str) == tenant_id_input,
                        ["fullname", "id_number", "phone", "email",
                         "sex", "people", "house_status", "start_date", "rent"]
                    ] = [
                        fullname, id_number, phone, email, sex,
                        str(people), house_status, str(start_date), str(rent)
                    ]

                    updated_dict = tenants[tenants["tenant_id"].astype(str) == tenant_id_input].iloc[0].to_dict()
                    save_tenant_profile_file(updated_dict)
                    save_tenants(tenants)

                    st.success("Amakuru yahinduwe neza!")

            
            
    

    # ======================================================================================
    # 3) MESSAGES
    # ======================================================================================
    elif menu == "Ubutumwa":
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
    elif menu == "Imyishyurire":
        st.subheader("💰 Imyishyurire y'abakiriya")
        payments = load_payments()
        st.dataframe(payments)

        with st.form("add_payment"):
            tenant_id = st.text_input("ID y'umukiriya")
            month = st.text_input("Ukwezi (ex: 2025-01)")
            status = st.selectbox("Status yo kwishyura", ["Yishyuye", "Yatinze", "Ntabwo Yishyuye"])
            paid_date = st.date_input("Itariki yishyuwe")
            if st.form_submit_button("Ongeramo Imyishyurire"):
                new_id = str(int(payments["payment_id"].astype(int).max()) + 1) if not payments.empty else "1"
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
    # 5) PAYMENT MONITORING
    # ======================================================================================
    elif menu == "Payment Monitoring":
        st.subheader("⏰ Payment Dashboard + Reminders")
        today = datetime.date.today()
        reminders, overdue, upcoming = [], [], []

        for _, t in tenants.iterrows():
            try:
                start_date = datetime.date.fromisoformat(t["start_date"])
                due_day = start_date.day
                this_month_due = today.replace(day=due_day)
                next_due = this_month_due if this_month_due >= today else (
                    datetime.date(this_month_due.year + 1, 1, due_day) if this_month_due.month == 12
                    else datetime.date(this_month_due.year, this_month_due.month + 1, due_day)
                )
                days_left = (next_due - today).days
                item = {"fullname": t["fullname"], "phone": t["phone"], "email": t.get("email", ""), "due_date": str(next_due), "days_left": days_left}
                if days_left < 0: overdue.append(item)
                elif days_left == 5: reminders.append(item)
                elif 0 <= days_left <= 10: upcoming.append(item)
            except: pass

        # 🔴 Overdue
        if overdue:
            st.error("❗ ABAKIRIYA BATINZE KWIISHYURA (OVERDUE)")
            for r in overdue:
                st.write(f"<span style='color:red; font-weight:bold;'>‼️ {r['fullname']} — Due: {r['due_date']} ({abs(r['days_left'])} days late)</span>", unsafe_allow_html=True)

        # 🔔 Reminders 5 days before
        if reminders:
            st.warning("🔔 ABAKENYEYE KWIBUKWA — 5 Days Before Payment")
            for r in reminders:
                st.info(f"➡️ {r['fullname']} — Rent due in 5 days (Due: {r['due_date']})")
                send_sms(r["phone"], f"MWIBUKIJE: Ubukode buzishyurwa ku {r['due_date']}. Murakoze!")
                if r["email"]:
                    send_email(r["email"], "REMINDER: Ubukode burarangira", f"Muraho {r['fullname']}, mwibukijwe ko ubukode buzishyurwa ku {r['due_date']}.\nMurakoze!")

        # 🟡 Upcoming
        if upcoming:
            st.info("📅 Abakiriya bafite ubukode hafi kurangira (Within 10 days)")
            for r in upcoming:
                st.write(f"➡️ {r['fullname']} — {r['days_left']} days left (Due: {r['due_date']})")

        st.write("---")
        # Filter by days left
        st.subheader("🔍 Reba abishyura vuba")
        max_days = st.slider("Minsi isigaye imbere ya due date", 0, 30, 7)
        filtered = [t for t in upcoming if t["days_left"] <= max_days]
        if filtered:
            st.write(f"### Abakiriya bafite {max_days} days cyangwa munsi basigaye")
            for r in filtered: st.write(f"➡️ **{r['fullname']}** — {r['days_left']} days left")
        else:
            st.info("Nta mukiriya uri muri ubwo bwiciro.")

    # ======================================================================================
    # 6) FILE MANAGEMENT
    # ======================================================================================
    elif menu == "Dosiye z'Abakiriya":
        st.subheader("📂 Dosiye z'abakiriya")
        tenants = load_tenants()

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
        for _, t in tenants.iterrows():
            phone = t["phone"]
            st.write(f"### 👤 {t['fullname']} — {phone}")

            # JSON
            json_file = os.path.join(TENANT_FILES_DIR, f"{phone}.json")
            if os.path.exists(json_file):
                with open(json_file, "rb") as f:
                    st.download_button(
                        label="📥 Kuramo Dosiye (JSON)",
                        data=f,
                        file_name=f"{phone}.json",
                        mime="application/json"
                    )

            # PDF
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
    # 7) SEND SMS & EMAIL MANUALLY
    # ======================================================================================
    elif menu == "Kohereza SMS/Email":
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
