# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 15:07:37 2025

@author: ELINA
"""

# app.py
import streamlit as st
from tenant import tenant_portal
from admin import admin_portal

st.set_page_config(page_title="Tenant Management System", page_icon="🏠", layout="wide")

# Custom CSS for attractive UI
def local_css():
    st.markdown("""
    <style>
    .stApp { background: linear-gradient(180deg,#f7f9fc,#eef5ff); }
    [data-testid="stSidebar"] { background: #0b2545; color:white; }
    .card { background: white; padding: 18px; border-radius: 12px; box-shadow: 0 6px 18px rgba(14,30,37,0.08); }
    h1 { color: #062745; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .big-number { font-size:28px; font-weight:700; color:#062745; }
    .stButton>button { background-color: #0b63d6; color:white; border-radius:10px; padding:10px 18px; }
    .stButton>button:hover { background-color:#084ab0; }
    .stTextInput>div>div>input { border-radius:8px; padding:10px; }
    .stSelectbox>div>div>div { border-radius:8px; }
    </style>
    """, unsafe_allow_html=True)

local_css()

st.sidebar.title("Menu")
role = st.sidebar.selectbox("Hitamo uruhare (Role)", ["Tenant (Umukiriya)", "Admin (Umuyobozi)"])

st.title("🏠 Sisitemu yo gucunga abakiriya (Tenant Management)")

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.write("Murakaza neza! Hitamo uruhare rwawe kuri sidebar hanyuma ukore login.")
st.markdown("</div>", unsafe_allow_html=True)

if role.startswith("Tenant"):
    tenant_portal()
else:
    admin_portal()
