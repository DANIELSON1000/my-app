# -*- coding: utf-8 -*-
"""
Tenant Management System — Full-page wallpaper version
"""
import streamlit as st
from tenant import tenant_portal
from admin import admin_portal
import os

# Page configuration
st.set_page_config(page_title="Tenant Management System", page_icon="🏠", layout="wide")

# Ensure tenant_files folder exists
os.makedirs("tenant_files", exist_ok=True)

# Full-page wallpaper + UI styling
def local_css():
    st.markdown("""
    <style>

    /* ================================
       FULL PAGE WALLPAPER BACKGROUND
       ================================ */
    .stApp {
        background-image: url('pictures/landlord.png');
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
        min-height: 100vh;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* ================================
       SIDEBAR STYLING
       ================================ */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.80) !important;
        color: #0b2545 !important;
        font-weight: bold;
        padding: 20px;
        border-radius: 12px;
        backdrop-filter: blur(6px);
    }

    /* ================================
       MAIN CARD (CENTER BOX)
       ================================ */
    .card {
        background: rgba(255, 255, 255, 0.88);
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(4px);
    }

    /* ================================
       TEXT & HEADINGS
       ================================ */
    h1, h2, h3, p, span, label {
        color: #062745 !important;
        text-shadow: 1px 1px 4px rgba(255,255,255,0.7);
    }

    /* ================================
       BUTTON DESIGN
       ================================ */
    .stButton>button {
        background-color: #ff0054 !important;
        color: white !important;
        border-radius: 25px;
        padding: 12px 25px;
        font-weight: 600;
        border: none;
        transition: 0.25s;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.25);
    }

    .stButton>button:hover {
        background-color: #e60047 !important;
        transform: scale(1.05);
    }

    /* ================================
       INPUT FIELDS
       ================================ */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>div {
        border-radius: 20px !important;
        padding: 14px !important;
        border: 1px solid #cccccc !important;
        font-size: 16px !important;
        background: rgba(255, 255, 255, 0.90) !important;
    }

    .stSelectbox>div>div>div:hover {
        border-color: #ff0054 !important;
    }

    </style>
    """, unsafe_allow_html=True)

local_css()

# Sidebar menu
st.sidebar.title("🏠 Menu")
role = st.sidebar.selectbox("Hitamo uruhande rwawe:", ["Tenant", "Admin"])

# Main content card
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.title("Tenant Management System")
st.write("Murakaza neza!")
st.markdown("</div>", unsafe_allow_html=True)

# Show correct portal
if role == "Tenant":
    tenant_portal()
else:
    admin_portal()
