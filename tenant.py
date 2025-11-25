# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 15:02:33 2025

@author: ELINA
"""

# tenant.py
import streamlit as st
import pandas as pd
from database import load_tenants, save_messages, load_messages, timestamp_now, load_payments
from database import save_messages as save_msgs_table
from database import load_tenants as load_tenants_table

def tenant_portal():
    st.header("Ahantu h'abakiriya (Tenant Portal)")

    tenants = load_tenants_table()
    phone = st.text_input("Injiza nomero ya telefone yawe (Login)")

    if st.button("Injira"):
        user = tenants[tenants["phone"] == phone]
        if user.empty:
            st.error("Ntiboneka umukiriya ufite iyo nomero. Reba neza cyangwa hamagara administrator.")
            return
        user = user.iloc[0].to_dict()
        st.success(f"Mwaramutse {user.get('fullname')}")
        st.markdown("---")

        # Show info (read-only)
        st.subheader("Amakuru Yawe")
        info = {
            "Amazina yose": user.get("fullname"),
            "Indangamuntu": user.get("id_number"),
            "Telefone": user.get("phone"),
            "Igitsina": user.get("sex"),
            "Abatuye mu nzu": user.get("people"),
            "Status y'inzu": user.get("house_status"),
            "Itariki y'itangira": user.get("start_date"),
            "Amafaranga buri kwezi": user.get("rent")
        }
        st.table(pd.DataFrame(list(info.items()), columns=["Igice","Agaciro"]))

        st.markdown("---")
        # Payment status
        st.subheader("Status y'Ubwishyu")
        payments = load_payments()
        my_pay = payments[payments["tenant_id"] == str(user.get("tenant_id"))]
        if my_pay.empty:
            st.info("Nta makuru y'ubwishyu aboneka.")
        else:
            st.dataframe(my_pay)

        st.markdown("---")
        # Messages
        st.subheader("Ohereza Igitekerezo / Ikirego")
        message = st.text_area("Andika ubutumwa bwawe hano")
        if st.button("Ohereza ubutumwa"):
            if not message.strip():
                st.warning("Andika ubutumwa mbere yo kohereza.")
            else:
                msgs = load_messages()
                new_id = str(int(msgs["message_id"].astype(int).max()) + 1) if not msgs.empty else "1"
                new_row = {
                    "message_id": new_id,
                    "tenant_id": str(user.get("tenant_id")),
                    "message": message,
                    "reply": "",
                    "date_sent": timestamp_now(),
                    "date_reply": "",
                    "status": "sent"
                }
                msgs = pd.concat([msgs, pd.DataFrame([new_row])], ignore_index=True)
                save_msgs_table(msgs)
                st.success("Ubutumwa bwoherejwe. Administrator azagusubiza.")
        st.markdown("---")
        # View messages
        st.subheader("Amameypu / Ibisubizo")
        msgs = load_messages()
        my_msgs = msgs[msgs["tenant_id"] == str(user.get("tenant_id"))].sort_values("date_sent", ascending=False)
        if my_msgs.empty:
            st.info("Nta butumwa bwawe bubonetse.")
        else:
            st.dataframe(my_msgs[["message","reply","date_sent","date_reply","status"]])
