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

    /* Background of full app */
    .stApp { 
        background: #eef5ff !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] { 
        background: #0b2545 !important; 
        color:white !important; 
    }

    /* Remove white background from cards */
    .card { 
        background: transparent !important; 
        padding: 18px;
        border-radius: 12px;
        box-shadow: none !important;
        border: none !important;
    }

    /* Clear text */
    h1, h2, h3, p, span, label {
        color: #062745 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        text-shadow: none !important;
    }

    .big-number { 
        font-size:28px; 
        font-weight:700; 
        color:#062745 !important; 
    }

    /* Buttons */
    .stButton>button { 
        background-color: #0b63d6 !important; 
        color:white !important; 
        border-radius:10px; 
        padding:10px 18px;
        font-weight: 600 !important;
        border: none !important;
    }
    .stButton>button:hover { 
        background-color:#084ab0 !important; 
    }

    /* Inputs */
    .stTextInput>div>div>input { 
        border-radius:8px !important; 
        padding:10px !important; 
    }

    .stSelectbox>div>div>div { 
        border-radius:8px !important; 
    }

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
