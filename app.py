# -*- coding: utf-8 -*-
"""
Tenant Management System — Full-page wallpaper version (Corrected)
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
        background-image: url('pictures/landlord.png') !important;
        background-size: cover !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    /* ================================
       SIDEBAR STYLING
       ================================ */
    [data-testid="stSidebar"] {
        background: rgba(255,255,255,0.75) !important;
        backdrop-filter: blur(6px);
        padding: 20px !important;
        border-right: 1px solid #e0e0e0 !important;
    }

    /* ================================
       MAIN CARD (CENTER BOX)
       ================================ */
    .main-card {
        background: rgba(255,255,255,0.85);
        padding: 30px;
        border-radius: 18px;
        margin-bottom: 25px;
        backdrop-filter: blur(6px);
        box-shadow: 0px 8px 25px rgba(0,0,0,0.15);
    }

    /* ================================
       TEXT & HEADINGS
       ================================ */
    h1, h2, h3, p, label, span {
        color: #062745 !important;
        text-shadow: none !important;
    }

    /* ================================
       BUTTON DESIGN
       ================================ */
    .stButton>button {
        background-color:#ff0054 !important;
        color:white !important;
        padding:12px 25px !important;
        border-radius:20px !important;
        border:none !important;
        font-weight:600 !important;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.25);
        transition: 0.25s;
    }
    .stButton>button:hover {
        background-color:#e60047 !important;
        transform:scale(1.03);
    }

    /* ================================
       INPUT FIELDS
       ================================ */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>div {
        border-radius:20px !important;
        padding:14px !important;
        border:1px solid #ccc !important;
        background: rgba(255,255,255,0.9) !important;
    }

    .stSelectbox>div>div>div:hover {
        border-color:#ff0054 !important;
    }

    </style>
    """, unsafe_allow_html=True)

local_css()

# ---------------------------------------
# Sidebar Menu
# ---------------------------------------
st.sidebar.title("🏠 Menu")
role = st.sidebar.selectbox("Hitamo uruhande rwawe:", ["Tenant", "Admin"])

# ---------------------------------------
# Main Content Card
# ---------------------------------------
st.markdown("<div class='main-card'>", unsafe_allow_html=True)
st.title("Tenant Management System")
st.write("Murakaza neza!")
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------
# Load Portal Based on Role
# ---------------------------------------
if role == "Tenant":
    tenant_portal()
else:
    admin_portal()
