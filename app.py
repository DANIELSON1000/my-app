# -*- coding: utf-8 -*-
"""
Full single-file Admin + Tenant portal (Option A) in Kinyarwanda.
Run with: streamlit run app.py
"""
import os
import json
import datetime
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# ----------------------------
# Streamlit page config
# ----------------------------
st.set_page_config(
    page_title="Rental Management System",
    layout="wide",
    page_icon="🏠"
)

# ----------------------------
# Try to import existing modules, otherwise provide safe fallbacks
# ----------------------------
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
    def timestamp_now():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def load_tenants():
        if os.path.exists("tenants.csv"):
            return pd.read_csv("tenants.csv", dtype=str)
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

try:
    from agreement_generator import generate_agreement
except Exception:
    def generate_agreement(tenant, landlord):
        os.makedirs("tenant_files", exist_ok=True)
        pid = tenant.get("tenant_id") or tenant.get("id_number") or "unknown"
        path = os.path.join("tenant_files", f"{pid}_agreement.pdf")
        with open(path, "wb") as f:
            f.write(b"%PDF-1.4\n% Placeholder agreement\n")
        return path

try:
    from message_service import send_email, send_sms
except Exception:
    def send_sms(phone, text):
        return True, "sms-fake"
    def send_email(email, subject, body):
        return True, "email-fake"

# ----------------------------
# Globals
# ----------------------------
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
TENANT_FILES_DIR = "tenant_files"
os.makedirs(TENANT_FILES_DIR, exist_ok=True)

# ----------------------------
# Helpers
# ----------------------------
def ensure_tenants_columns(df):
    expected = ["tenant_id","fullname","id_number","phone","email","sex","people","house_status","start_date","rent","agreement_file","created_at"]
    for c in expected:
        if c not in df.columns:
            df[c] = ""
    return df

def gen_new_tenant_id(tenants_df):
    if tenants_df.empty:
        return "1"
    ids = tenants_df["tenant_id"].astype(str).str.extract(r"(\d+)").dropna()
    if ids.empty:
        return str(len(tenants_df) + 1)
    try:
        maxn = ids.astype(int).max().values[0]
        return str(int(maxn) + 1)
    except Exception:
        return str(len(tenants_df) + 1)

def save_tenant_profile_file(tenant_dict):
    tenant_id = str(tenant_dict.get("tenant_id") or tenant_dict.get("id_number") or tenant_dict.get("phone"))
    path = os.path.join(TENANT_FILES_DIR, f"{tenant_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tenant_dict, f, ensure_ascii=False, indent=4)
    tenant_folder = os.path.join(TENANT_FILES_DIR, tenant_id)
    os.makedirs(tenant_folder, exist_ok=True)
    return path

def load_tenant_profile_file(tenant_id):
    path = os.path.join(TENANT_FILES_DIR, f"{tenant_id}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# ----------------------------
# Tenant portal function
# ----------------------------
def tenant_portal():
    st.header("Tenant Portal (Urubuga rw'Umukiriya)")

    tenants = load_tenants()
    tenants = ensure_tenants_columns(tenants)

    phone = st.text_input("Injiza nomero ya telefone yawe (Login)")

    if st.button("Injira"):
        if phone.strip() == "":
            st.warning("Injiza nomero ya telefone")
            return
        user_df = tenants[tenants["phone"] == phone]
        if user_df.empty:
            st.error("Ntiboneka umukiriya ufite iyo nomero. Reba neza cyangwa hamagara administrator.")
            return

        user = user_df.iloc[0].to_dict()
        tenant_id = str(user.get("tenant_id"))
        st.success(f"Mwaramutse {user.get('fullname')}")
        st.markdown("---")

        # Show tenant info
        st.subheader("Amakuru Yawe")
        info = {
            "Amazina yose": user.get("fullname"),
            "Indangamuntu": user.get("id_number"),
            "Telefone": user.get("phone"),
            "Email": user.get("email"),
            "Igitsina": user.get("sex"),
            "Abatuye mu nzu": user.get("people"),
            "Status y'inzu": user.get("house_status"),
            "Itariki y'itangira": user.get("start_date"),
            "Amafaranga buri kwezi": user.get("rent")
        }
        st.table(pd.DataFrame(list(info.items()), columns=["Igice","Agaciro"]))
        st.markdown("---")

        # Payment countdown
        st.subheader("⏰ Countdown y'Ubwishyu")
        try:
            start_date = datetime.date.fromisoformat(user["start_date"])
            due_day = start_date.day
            today = datetime.date.today()
            try:
                this_month_due = today.replace(day=due_day)
            except ValueError:
                last_day = (today.replace(day=1) + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)
                this_month_due = last_day
            next_due = this_month_due if this_month_due >= today else (
                datetime.date(this_month_due.year + 1, 1, due_day) if this_month_due.month == 12
                else datetime.date(this_month_due.year, this_month_due.month + 1, due_day)
            )
            days_left = (next_due - today).days
            if days_left < 0:
                st.error(f"❗ Hari {abs(days_left)} iminsi urenze due date! Mwihutire kwishyura.")
            elif days_left == 0:
                st.warning(f"⚠️ LEAKI UYU MUNSI — TODAY is the due date ({next_due})!")
            else:
                st.info(f"📅 Mufite **{days_left} iminsi** mbere yo kwishyura (Due: {next_due})")
        except Exception:
            st.warning("Date ya payment ntiboneka neza.")

        st.markdown("---")
        # Payment history
        st.subheader("Status y'Ubwishyu")
        payments = load_payments()
        my_pay = payments[payments["tenant_id"].astype(str) == tenant_id] if not payments.empty else pd.DataFrame()
        if my_pay.empty:
            st.info("Nta makuru y'ubwishyu aboneka.")
        else:
            st.dataframe(my_pay)

        st.markdown("---")
        # Messages
        st.subheader("Ohereza Igitekerezo /Ikifuzo/Ikibazo")
        message = st.text_area("Andika ubutumwa bwawe hano")
        if st.button("Ohereza ubutumwa"):
            if not message.strip():
                st.warning("Andika ubutumwa mbere yo kohereza.")
            else:
                msgs = load_messages()
                new_id = str(int(msgs["message_id"].astype(int).max()) + 1) if (not msgs.empty and msgs["message_id"].astype(str).str.isnumeric().any()) else "1"
                new_row = {
                    "message_id": new_id,
                    "tenant_id": tenant_id,
                    "message": message,
                    "reply": "",
                    "date_sent": timestamp_now(),
                    "date_reply": "",
                    "status": "sent"
                }
                msgs = pd.concat([msgs, pd.DataFrame([new_row])], ignore_index=True)
                save_messages(msgs)
                st.success("Ubutumwa bwoherejwe. Administrator azagusubiza.")

        st.markdown("---")
        # Replies
        st.subheader("Ibisubizo")
        msgs = load_messages()
        my_msgs = msgs[msgs["tenant_id"].astype(str) == tenant_id].sort_values("date_sent", ascending=False) if not msgs.empty else pd.DataFrame()
        if my_msgs.empty:
            st.info("Nta butumwa bwawe bubonetse.")
        else:
            st.dataframe(my_msgs[["message","reply","date_sent","date_reply","status"]])

        st.markdown("---")
        # Tenant files (only theirs)
        st.subheader("📂 Dosiye zawe zibitswe")
        found = False

        # Agreement (from record)
        agreement_path = user.get("agreement_file")
        if agreement_path and os.path.exists(agreement_path):
            st.write("• Amasezerano (Agreement PDF)")
            with open(agreement_path, "rb") as pdf:
                st.download_button(
                    label="Kuramo Amasezerano (PDF)",
                    data=pdf,
                    file_name=os.path.basename(agreement_path),
                    mime="application/pdf"
                )
            found = True

        # Files in tenant folder
        tenant_folder = os.path.join(TENANT_FILES_DIR, tenant_id)
        if os.path.exists(tenant_folder):
            files = sorted(os.listdir(tenant_folder))
            for f in files:
                path = os.path.join(tenant_folder, f)
                if os.path.isfile(path):
                    st.write("•", f)
                    with open(path, "rb") as file:
                        st.download_button(label=f"Kuramo {f}", data=file, file_name=f)
                    found = True

        if not found:
            st.info("Nta dosiye yawe ibitswe muri server (tenant_files/).")

# ----------------------------
# Admin portal function
# ----------------------------
def admin_portal():
    st.header("👨‍💼Admin Portal")

    pwd = st.text_input("Injiza ijambo ry'ibanga (Admin Password)", type="password")
    if pwd != ADMIN_PASSWORD:
        st.warning("⚠️ Ijambo ry'ibanga si ryo")
        return

    st.success("Murakaza neza, Administrator 👍")

    tenants = load_tenants()
    tenants = ensure_tenants_columns(tenants)
    messages = load_messages()
    payments = load_payments()

    menu = st.sidebar.selectbox("MENU", [
        "Kongeramo Umukiriya",
        "Reba Abakiriya",
        "Hindura Umukiriya",
        "Imyishyurire",
        "Payment Monitoring",
        "Ubutumwa",
        "Gucunga Dosiye z'Abakiriya",
        "Ohereza SMS/Email",
        "Settings"
    ])

    # 1) Add Tenant
    if menu == "Kongeramo Umukiriya":
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
            new_id = gen_new_tenant_id(new_tenants)
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
                "agreement_file": "",
                "created_at": timestamp_now()
            }
            landlord = {"name":"NTAKIRUTIMANA EZECHIEL","phone":"0785042128","email":"offliqz@gmail.com"}
            pdf_path = generate_agreement(tenant_dict, landlord)
            tenant_dict["agreement_file"] = pdf_path
            profile_path = save_tenant_profile_file(tenant_dict)
            new_tenants = pd.concat([new_tenants, pd.DataFrame([tenant_dict])], ignore_index=True)
            save_tenants(new_tenants)
            st.success("Umukiriya yongewe neza!")
            st.info(f"PDF Agreement: {pdf_path}")
            st.info(f"Dosiye JSON: {profile_path}")

    # -------------------------
    # 2) View Tenants
    # -------------------------
    elif menu == "Reba Abakiriya":
        st.subheader("📋 Urutonde rw'abakiriya bose")
        tenants = load_tenants()
        tenants = ensure_tenants_columns(tenants)
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
                profile_json = os.path.join(TENANT_FILES_DIR, f"{tenant_to_delete}.json")
                if os.path.exists(profile_json):
                    os.remove(profile_json)
                folder = os.path.join(TENANT_FILES_DIR, tenant_to_delete)
                if os.path.exists(folder):
                    try:
                        for f in os.listdir(folder):
                            os.remove(os.path.join(folder, f))
                        os.rmdir(folder)
                    except Exception:
                        pass
                st.success(f"Tenant ID {tenant_to_delete} yasibwe neza!")
                tenants = load_tenants()

    # -------------------------
    # 3) Edit Tenant
    # -------------------------
    elif menu == "Hindura Umukiriya":
        st.subheader("✏️ Hindura amakuru y'umukiriya")
        st.write("Shyiramo Tenant ID ushaka guhindura, hanyuma kanda **Shaka Umukiriya**")

        edit_id = st.text_input("Injiza Tenant ID ushaka guhindura")

        if st.button("Shaka Umukiriya"):
            st.session_state["edit_search_id"] = edit_id.strip()

        search_id = st.session_state.get("edit_search_id", "")

        if search_id:
            if search_id not in tenants["tenant_id"].astype(str).values:
                st.error("Tenant ID ntiboneka muri system.")
            else:
                t = tenants[tenants["tenant_id"].astype(str) == search_id].iloc[0]
                st.success(f"Uhitanye: {t['fullname']}")

                with st.form("edit_tenant_form"):
                    fullname = st.text_input("Amazina yose y'umukiriya", t["fullname"])
                    id_number = st.text_input("Indangamuntu (ID)", t.get("id_number", ""))
                    phone = st.text_input("Nomero ya telefone", t.get("phone", ""))
                    email = st.text_input("Email", t.get("email", ""))
                    sex = st.selectbox("Igitsina", ["Gabo", "Gore"], index=0 if t["sex"]=="Gabo" else 1)
                    people = st.number_input("Abantu batuye mu nzu", min_value=1, value=int(t.get("people",1)))
                    house_status = st.text_input("Ubwoko bw'inzu", t.get("house_status",""))
                    try:
                        sd = datetime.date.fromisoformat(t["start_date"])
                    except Exception:
                        sd = datetime.date.today()
                    start_date = st.date_input("Itariki atangiye kubamo", sd)
                    rent = st.number_input("Amafaranga y'ubukode (buri kwezi)", min_value=0, value=int(t.get("rent",0)))
                    submitted = st.form_submit_button("Hindura amakuru")

                if submitted:
                    tenants.loc[tenants["tenant_id"].astype(str) == search_id,
                        ["fullname", "id_number", "phone", "email",
                         "sex","people","house_status","start_date","rent"]] = [
                            fullname, id_number, phone, email, sex,
                            str(people), house_status, str(start_date), str(rent)
                        ]
                    updated_dict = tenants[tenants["tenant_id"].astype(str) == search_id].iloc[0].to_dict()
                    save_tenant_profile_file(updated_dict)
                    save_tenants(tenants)
                    st.success("Amakuru y'umukiriya yahinduwe neza!")
                    st.session_state["edit_search_id"] = ""

    # -------------------------
    # 4) Payments
    # -------------------------
    elif menu == "Imyishyurire":
        st.subheader("💰 Imyishyurire y'abakiriya")
        payments = load_payments()
        st.dataframe(payments)
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

    # -------------------------
    # 5) Messages
    # -------------------------
    elif menu == "Ubutumwa":
        st.subheader("✉️ Ubutumwa bw'abakiriya")
        st.dataframe(messages)

    # -------------------------
    # 6) Tenant Files Management
    # -------------------------
    elif menu == "Gucunga Dosiye z'Abakiriya":
        st.subheader("📂 Dosiye z'abakiriya")
        tenants = load_tenants()
        if tenants.empty:
            st.info("Nta tenants zibitswe.")
        else:
            # Download Excel of all tenants
            if st.button("⬇️ Kuramo Database yose (Excel)"):
                excel_path = os.path.join(TENANT_FILES_DIR, "ABAKIRIYA_ALL.xlsx")
                tenants.to_excel(excel_path, index=False)
                with open(excel_path, "rb") as f:
                    st.download_button(
                        label="📥 Download ABAKIRIYA_ALL.xlsx",
                        data=f,
                        file_name="ABAKIRIYA_ALL.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            st.write("---")
            for _, t in tenants.iterrows():
                tenant_id = str(t["tenant_id"])
                fullname = t["fullname"]
                st.write(f"### 👤 {fullname} — ID: {tenant_id}")

                json_file = os.path.join(TENANT_FILES_DIR, f"{tenant_id}.json")
                if os.path.exists(json_file):
                    with open(json_file, "rb") as f:
                        st.download_button(
                            label="📥 Kuramo Dosiye ya Tenant (JSON)",
                            data=f,
                            file_name=f"{tenant_id}.json",
                            mime="application/json"
                        )
                else:
                    st.warning("⚠️ Nta dosiye ya JSON ibonetse kuri uyu mukiriya.")

                agreement = t.get("agreement_file", "")
                if pd.notna(agreement) and agreement and os.path.exists(agreement):
                    with open(agreement, "rb") as f:
                        st.download_button(
                            label="📥 Kuramo Amasezerano ya PDF",
                            data=f,
                            file_name=os.path.basename(agreement),
                            mime="application/pdf"
                        )
                else:
                    st.info("📝 Nta masezerano ya PDF abitswe cyangwa file yaburiwe.")

                tenant_folder = os.path.join(TENANT_FILES_DIR, tenant_id)
                if os.path.exists(tenant_folder):
                    extra_files = [f for f in os.listdir(tenant_folder) if os.path.isfile(os.path.join(tenant_folder, f))]
                    if extra_files:
                        st.write("📎 **Ibindi byongewe na tenant:**")
                        for ex in extra_files:
                            fpath = os.path.join(tenant_folder, ex)
                            with open(fpath, "rb") as f:
                                st.download_button(label=f"📥 {ex}", data=f, file_name=ex)
                    else:
                        st.write("Nta bindi byongewe n'uyu mukiriya.")
                else:
                    st.write("Nta folder ya dosiye ibonetse kuri uyu mukiriya.")

                st.write("---")

# ----------------------------
# MAIN APP
# ----------------------------
def main():
    st.sidebar.title("🏠TENANT MONITORING SYSTEM")
    app_mode = st.sidebar.selectbox("Hitamo Portal", ["Tenant Portal", "Admin Portal"])
    if app_mode == "Tenant Portal":
        tenant_portal()
    else:
        admin_portal()

if __name__ == "__main__":
    main()


