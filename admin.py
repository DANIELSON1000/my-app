# -*- coding: utf-8 -*-
"""
Admin portal — manages tenants, payments, messages, reminders, and file downloads.
All tenant files are stored securely inside tenant_files/
"""
import os
import json
import datetime
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Try to import user modules (if they exist). If some are missing, provide safe fallbacks.
try:
    from database import (
        load_tenants,
        save_tenants,
        load_messages,
        save_messages,
        load_payments,
        save_payments,
        timestamp_now
    )
except Exception:
    # Fallback simple CSV/JSON implementations
    def timestamp_now():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def load_tenants():
        if os.path.exists("tenants.csv"):
            return pd.read_csv("tenants.csv", dtype=str)
        # Provide an empty dataframe with expected columns
        cols = ["tenant_id","fullname","id_number","phone","email","sex","people","house_status","start_date","rent","agreement_file","created_at"]
        return pd.DataFrame(columns=cols)

    def save_tenants(df):
        df.to_csv("tenants.csv", index=False)

    def load_messages():
        if os.path.exists("messages.csv"):
            return pd.read_csv("messages.csv", dtype=str)
        cols = ["message_id","tenant_id","message","reply","date_sent","date_reply","status"]
        return pd.DataFrame(columns=cols)

    def save_messages(df):
        df.to_csv("messages.csv", index=False)

    def load_payments():
        if os.path.exists("payments.csv"):
            return pd.read_csv("payments.csv", dtype=str)
        cols = ["payment_id","tenant_id","month","status","paid_date"]
        return pd.DataFrame(columns=cols)

    def save_payments(df):
        df.to_csv("payments.csv", index=False)

# agreement generator
try:
    from agreement_generator import generate_agreement
except Exception:
    def generate_agreement(tenant, landlord):
        # create a simple placeholder file and return its path
        TENANT_FILES_DIR = "tenant_files"
        os.makedirs(TENANT_FILES_DIR, exist_ok=True)
        pid = tenant.get("tenant_id", tenant.get("id_number", "unknown"))
        path = os.path.join(TENANT_FILES_DIR, f"{pid}_agreement.pdf")
        # Write a small placeholder so download works
        with open(path, "wb") as f:
            f.write(b"%PDF-1.4\n% Placeholder agreement\n")
        return path

# message service (sms/email)
try:
    from message_service import send_email, send_sms
except Exception:
    def send_sms(phone, text):
        # Fake send: return ok True and info string
        return True, "sms-fake"
    def send_email(email, subject, body):
        return True, "email-fake"

# Admin password from .env (or default)
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

# TENANT FILES location
TENANT_FILES_DIR = "tenant_files"
os.makedirs(TENANT_FILES_DIR, exist_ok=True)

# Utility: save tenant profile JSON into tenant_files/<tenant_id>.json
def save_tenant_profile_file(tenant_dict):
    tenant_id = str(tenant_dict.get("tenant_id") or tenant_dict.get("id_number") or tenant_dict.get("phone"))
    path = os.path.join(TENANT_FILES_DIR, f"{tenant_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tenant_dict, f, ensure_ascii=False, indent=4)
    # ensure tenant-specific folder exists
    tenant_folder = os.path.join(TENANT_FILES_DIR, tenant_id)
    os.makedirs(tenant_folder, exist_ok=True)
    return path

# Helper: read tenant json file if exists
def load_tenant_profile_file(tenant_id):
    path = os.path.join(TENANT_FILES_DIR, f"{tenant_id}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# ----------------------------
# ADMIN PORTAL
# ----------------------------
def admin_portal():
    st.header("👨‍💼 Ubuyobozi — Admin Portal")

    # LOGIN
    pwd = st.text_input("Injiza ijambo ry'ibanga (Admin Password)", type="password")
    if pwd != ADMIN_PASSWORD:
        st.warning("⚠️ Ijambo ry'ibanga si ryo")
        return

    st.success("Murakaza neza, Administrator 👍")

    # Load datasets (from database module or fallback)
    tenants = load_tenants()
    messages = load_messages()
    payments = load_payments()

    # Ensure tenants DF has expected columns (avoid KeyError)
    expected_tenant_cols = ["tenant_id","fullname","id_number","phone","email","sex","people","house_status","start_date","rent","agreement_file","created_at"]
    for c in expected_tenant_cols:
        if c not in tenants.columns:
            tenants[c] = ""

    # MENU
    menu = st.sidebar.selectbox("Hitamo icyo ushaka gukora", [
        "Kongeramo umukiriya",
        "Reba abakiriya",
        "Ubutumwa",
        "Imyishyurire",
        "Payment Monitoring",
        "Dosiye z'Abakiriya",
        "Kohereza SMS/Email"
    ])

    # ======================
    # 1) ADD TENANT
    # ======================
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
            start_date = st.date_input("Itariki atangiye kubamo", value=datetime.date.today())
            rent = st.number_input("Amafaranga y'ubukode (buri kwezi)", min_value=0)
            submitted = st.form_submit_button("Bika umukiriya")

        if submitted:
            new_tenants = tenants.copy()
            new_id = str(int(new_tenants["tenant_id"].astype(int).max()) + 1) if (not new_tenants.empty and new_tenants["tenant_id"].astype(str).str.isnumeric().any()) else "1"

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

            # generate agreement file (uses your generator or fallback)
            AGREEMENT_LANDLORD = {
                "name": "NTAKIRUTIMANA EZECHIEL",
                "phone": "0785042128",
                "email": "offliqz@gmail.com"
            }
            try:
                pdf_path = generate_agreement(tenant_dict, AGREEMENT_LANDLORD)
            except Exception as e:
                st.warning("Agreement generator failed; using placeholder.")
                pdf_path = generate_agreement(tenant_dict, AGREEMENT_LANDLORD)

            tenant_dict["agreement_file"] = pdf_path

            # save profile JSON
            profile_path = save_tenant_profile_file(tenant_dict)

            # append to tenants dataframe and persist
            new_tenants = pd.concat([new_tenants, pd.DataFrame([tenant_dict])], ignore_index=True)
            save_tenants(new_tenants)
            tenants = new_tenants  # update in-memory

            st.success("Umukiriya yongewe neza!")
            st.info(f"PDF Agreement: {pdf_path}")
            st.info(f"Dosiye JSON: {profile_path}")

    # ======================
    # 2) VIEW TENANTS (and delete)
    # ======================
    elif menu == "Reba abakiriya":
        st.subheader("📋 Urutonde rw'abakiriya bose")
        tenants = load_tenants()
        if tenants.empty:
            st.info("Nta tenants zibitswe.")
        else:
            st.dataframe(tenants.reset_index(drop=True))

        st.write("---")
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
                # remove profile json if exists
                profile_json = os.path.join(TENANT_FILES_DIR, f"{tenant_to_delete}.json")
                if os.path.exists(profile_json):
                    os.remove(profile_json)
                st.success(f"Tenant ID {tenant_to_delete} yasibwe neza!")
                tenants = load_tenants()

    # ======================
    # 3) MESSAGES
    # ======================
    elif menu == "Ubutumwa":
        st.subheader("✉️ Ubutumwa bw'abakiriya")
        msgs = load_messages()
        if msgs.empty:
            st.info("Nta butumwa buraboneka ubu.")
        else:
            st.dataframe(msgs)

            st.write("---")
            sel = st.text_input("Andika message_id ushaka gusubiza")
            reply = st.text_area("Andika igisubizo hano")
            if st.button("Ohereza Igisubizo"):
                if not sel.strip():
                    st.warning("Injiza message_id")
                else:
                    msgs = msgs.copy()
                    idx_list = msgs.index[msgs["message_id"].astype(str) == str(sel)].tolist()
                    if not idx_list:
                        st.error("Message ID ntiboneka")
                    else:
                        i = idx_list[0]
                        msgs.at[i, "reply"] = reply
                        msgs.at[i, "date_reply"] = timestamp_now()
                        msgs.at[i, "status"] = "replyed"
                        save_messages(msgs)
                        tenant_id = msgs.at[i, "tenant_id"]
                        # fetch tenant phone/email safely
                        try:
                            t = tenants[tenants["tenant_id"].astype(str) == str(tenant_id)].iloc[0]
                            if "phone" in t and pd.notna(t["phone"]) and t["phone"]:
                                send_sms(t["phone"], f"Igisubizo: {reply}")
                            if "email" in t and pd.notna(t["email"]) and t["email"]:
                                send_email(t["email"], "Ibisubizo by'ubutumwa", reply)
                        except Exception:
                            pass
                        st.success("Reply yoherejwe neza!")

    # ======================
    # 4) PAYMENTS
    # ======================
    elif menu == "Imyishyurire":
        st.subheader("💰 Imyishyurire y'abakiriya")
        payments = load_payments()
        if payments.empty:
            st.info("Nta makuru y'imyishyurire abitswe.")
        else:
            st.dataframe(payments)

        st.write("---")
        with st.form("add_payment"):
            tenant_id = st.text_input("ID y'umukiriya")
            month = st.text_input("Ukwezi (ex: 2025-01)")
            status = st.selectbox("Status yo kwishyura", ["Yishyuye", "Yatinze", "Ntabwo Yishyuye"])
            paid_date = st.date_input("Itariki yishyuwe", value=datetime.date.today())
            if st.form_submit_button("Ongeramo Imyishyurire"):
                payments = payments.copy()
                new_id = str(int(payments["payment_id"].astype(int).max()) + 1) if (not payments.empty and payments["payment_id"].astype(str).str.isnumeric().any()) else "1"
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

    # ======================
    # 5) PAYMENT MONITORING & REMINDERS
    # ======================
    elif menu == "Payment Monitoring":
        st.subheader("⏰ Payment Dashboard + Reminders")
        tenants = load_tenants()
        today = datetime.date.today()
        reminders, overdue, upcoming = [], [], []

        for _, t in tenants.iterrows():
            try:
                if not t.get("start_date") or pd.isna(t.get("start_date")) or t["start_date"] == "":
                    continue
                start_date = datetime.date.fromisoformat(t["start_date"])
                due_day = start_date.day
                # compute this month's due safely
                try:
                    this_month_due = today.replace(day=due_day)
                except ValueError:
                    # if day does not exist in this month (e.g., 31 in Feb), pick last day of month
                    last_day = (today.replace(day=1) + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)
                    this_month_due = last_day
                next_due = this_month_due if this_month_due >= today else (
                    datetime.date(this_month_due.year + 1, 1, due_day) if this_month_due.month == 12
                    else datetime.date(this_month_due.year, this_month_due.month + 1, due_day)
                )
                days_left = (next_due - today).days
                item = {"tenant_id": t["tenant_id"], "fullname": t["fullname"], "phone": t.get("phone",""), "email": t.get("email",""), "due_date": str(next_due), "days_left": days_left}
                if days_left < 0:
                    overdue.append(item)
                elif days_left == 5:
                    reminders.append(item)
                elif 0 <= days_left <= 10:
                    upcoming.append(item)
            except Exception:
                continue

        if overdue:
            st.error("❗ ABAKIRIYA BATINZE KWIISHYURA (OVERDUE)")
            for r in overdue:
                st.write(f"‼️ {r['fullname']} — Due: {r['due_date']} ({abs(r['days_left'])} days late)")

        if reminders:
            st.warning("🔔 ABAKENYEYE KWIBUKWA — 5 Days Before Payment")
            st.write("If you want to send reminders now, check the box below.")
            send_now = st.checkbox("Ohereza reminders ubu (SMS & Email)", value=False)
            for r in reminders:
                st.write(f"➡️ {r['fullname']} — Due: {r['due_date']}")
            if send_now:
                for r in reminders:
                    if r["phone"]:
                        send_sms(r["phone"], f"MWIBUKIJE: Ubukode buzishyurwa ku {r['due_date']}. Murakoze!")
                    if r["email"]:
                        send_email(r["email"], "REMINDER: Ubukode burarangira", f"Muraho {r['fullname']}, mwibukijwe ko ubukode buzishyurwa ku {r['due_date']}.")
                st.success("Reminders zohererejwe!")

        if upcoming:
            st.info("📅 Abakiriya bafite ubukode hafi kurangira (Within 10 days)")
            for r in upcoming:
                st.write(f"➡️ {r['fullname']} — {r['days_left']} days left (Due: {r['due_date']})")

        st.write("---")
        st.subheader("🔍 Reba abishyura vuba")
        max_days = st.slider("Minsi isigaye imbere ya due date", 0, 30, 7)
        filtered = [t for t in upcoming if t["days_left"] <= max_days]
        if filtered:
            st.write(f"### Abakiriya bafite {max_days} days cyangwa munsi basigaye")
            for r in filtered:
                st.write(f"➡️ **{r['fullname']}** — {r['days_left']} days left")
        else:
            st.info("Nta mukiriya uri muri ubwo bwiciro.")

    # ======================
    # 6) FILE MANAGEMENT
    # ======================
    elif menu == "Dosiye z'Abakiriya":
        st.subheader("📂 Dosiye z'abakiriya")
        tenants = load_tenants()
        if tenants.empty:
            st.info("Nta tenants zibitswe.")
        else:
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
                tenant_id = str(t["tenant_id"])
                st.write(f"### 👤 {t['fullname']} — ID: {tenant_id}")

                # JSON profile
                json_file = os.path.join(TENANT_FILES_DIR, f"{tenant_id}.json")
                if os.path.exists(json_file):
                    with open(json_file, "rb") as f:
                        st.download_button(
                            label="📥 Kuramo Dosiye (JSON)",
                            data=f,
                            file_name=f"{tenant_id}.json",
                            mime="application/json"
                        )
                else:
                    st.write("Nta JSON profile ibonetse.")

                # Agreement PDF (path stored in tenants df)
                agreement = t.get("agreement_file", "")
                if pd.notna(agreement) and agreement and os.path.exists(agreement):
                    with open(agreement, "rb") as f:
                        st.download_button(
                            label="📥 Kuramo Amasezerano (PDF)",
                            data=f,
                            file_name=os.path.basename(agreement),
                            mime="application/pdf"
                        )
                else:
                    st.write("Nta agreement PDF ibonetse cyangwa file yabuze.")

                # any extra files inside tenant folder
                tenant_folder = os.path.join(TENANT_FILES_DIR, tenant_id)
                if os.path.exists(tenant_folder):
                    extras = [x for x in os.listdir(tenant_folder) if os.path.isfile(os.path.join(tenant_folder,x))]
                    if extras:
                        st.write("— Ibindi byoherejwe na tenant:")
                        for ex in extras:
                            path_ex = os.path.join(tenant_folder, ex)
                            with open(path_ex, "rb") as f:
                                st.download_button(label=f"📥 {ex}", data=f, file_name=ex)
                st.write("---")

    # ======================
    # 7) SEND SMS & EMAIL MANUALLY
    # ======================
    elif menu == "Kohereza SMS/Email":
        st.subheader("📨 Kohereza ubutumwa")
        st.write("Ohereza SMS cyangwa Email ku nomero/email wahisemo.")
        col1, col2 = st.columns(2)
        with col1:
            phone = st.text_input("Nomero ya telefone")
            if st.button("Ohereza SMS"):
                ok, info = send_sms(phone, st.session_state.get("manual_text", "Muraho"))
                if ok:
                    st.success("SMS yoherejwe!")
                else:
                    st.error(f"SMS error: {info}")
        with col2:
            email = st.text_input("Email")
            if st.button("Ohereza Email"):
                ok, info = send_email(email, "Ubutumwa bwa Nyirinzu", st.session_state.get("manual_text", "Muraho"))
                if ok:
                    st.success("Email yoherejwe!")
                else:
                    st.error(f"Email error: {info}")

        st.write("---")
        text = st.text_area("Ubutumwa", value="Muraho, iyi ni message ivuye ku nyir'inzu.")
        st.session_state["manual_text"] = text


if __name__ == "__main__":
    admin_portal()
