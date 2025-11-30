# -*- coding: utf-8 -*-
"""
Tenant Management System — Full-page wallpaper version
"""
import streamlit as st
from tenant import tenant_portal
from admin import admin_portal
import os

# Ensure tenant_files folder exists
os.makedirs("tenant_files", exist_ok=True)

# Page configuration
st.set_page_config(
    page_title="Tenant Management System",
    page_icon="🏠",
    layout="wide"
)

# ----------------------------
# CSS for background & styling
# ----------------------------
def local_css():
    st.markdown("""
    <style>
    /* Full-page background */
    .stApp {
        background-image: url('./pictures/landlord.png');
        background-size: cover !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    /* Make all text readable */
    * {
        color: #062745 !important;
        text-shadow: none !important;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(255,255,255,0.75) !important;
        backdrop-filter: blur(6px);
        padding: 20px !important;
        border-right: 1px solid #e0e0e0 !important;
    }

    /* Card styling */
    .main-card {
        background: rgba(255,255,255,0.85);
        padding: 30px;
        border-radius: 18px;
        margin-bottom: 25px;
        backdrop-filter: blur(6px);
        box-shadow: 0px 8px 25px rgba(0,0,0,0.15);
    }

    /* Button styling */
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

    /* Input styling */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>div {
        border-radius:20px !important;
        padding:14px !important;
        border:1px solid #ccc !important;
        background: rgba(255,255,255,0.9) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Apply CSS
local_css()

# ----------------------------
# Main app logic
# ----------------------------
# Example layout
st.title("🏠 Tenant Management System")

st.markdown('<div class="main-card">Welcome to the Tenant Portal!</div>', unsafe_allow_html=True)

# Sidebar navigation
menu = ["Tenant Portal", "Admin Portal"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Tenant Portal":
    tenant_portal()
else:
    admin_portal()
