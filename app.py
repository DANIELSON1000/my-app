# -*- coding: utf-8 -*-
"""
Main app entry — unchanged layout, ensures tenant_files folder exists.
"""
import streamlit as st
from tenant import tenant_portal
from admin import admin_portal
import os

st.set_page_config(page_title="Tenant Management System", page_icon="🏠", layout="wide")

# Ensure tenant_files folder exists
os.makedirs("tenant_files", exist_ok=True)

# Custom CSS for attractive UI + background wallpaper
def local_css():
    st.markdown(f"""
    <style>
    /* Background image */
    .stApp {{
        background: url('pictures/landlord.png') no-repeat center center fixed;
        background-size: cover;
    }}

    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background: #0b2545 !important;
        color:white !important;
    }}

    /* Card styling */
    .card {{
        background: rgba(255, 255, 255, 0.7) !important;
        padding: 18px;
        border-radius: 12px;
        box-shadow: none !important;
        border: none !important;
    }}

    /* Text styling */
    h1, h2, h3, p, span, label {{
        color: #062745 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        text-shadow: none !important;
    }}

    /* Button styling */
    .stButton>button {{
        background-color: #0b63d6 !important;
        color:white !important;
        border-radius:10px;
        padding:10px 18px;
        font-weight: 600 !important;
        border: none !important;
    }}
    .stButton>button:hover {{
        background-color:#084ab0 !important;
    }}

    /* Input styling */
    .stTextInput>div>div>input {{
        border-radius:8px !important;
        padding:10px !important;
    }}

    .stSelectbox>div>div>div {{
        border-radius:8px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

local_css()

st.sidebar.title("Menu")
role = st.sidebar.selectbox("Hitamo", ["Tenant", "Admin"])

st.title("🏠 Tenant Management")

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.write("Murakaza neza!")
st.markdown("</div>", unsafe_allow_html=True)

if role == "Tenant":
    tenant_portal()
else:
    admin_portal()
