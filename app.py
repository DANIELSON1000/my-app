# -*- coding: utf-8 -*-
"""
Tenant Management System — full-page wallpaper covering all index
"""
import streamlit as st
from tenant import tenant_portal
from admin import admin_portal
import os

# Page configuration
st.set_page_config(page_title="Tenant Management System", page_icon="🏠", layout="wide")

# Ensure tenant_files folder exists
os.makedirs("tenant_files", exist_ok=True)

# Full-page wallpaper and UI styling
def local_css():
    st.markdown("""
    <style>
    /* Full-page background */
    .stApp {
        background-image: url('pictures/landlord.png');
        background-size: cover;          /* Cover entire page */
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;    /* stays fixed when scrolling */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #062745;
        min-height: 100vh;               /* ensures full height */
    }

    /* Make sidebar transparent to show wallpaper */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.85) !important;
        color: #0b2545 !important;
        font-weight: bold;
        font-size: 16px;
        border-radius: 12px;
        padding: 20px;
    }

    /* Overlay card for main content */
    .card {
        background: rgba(255, 255, 255, 0.85) !important;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.2) !important;
        border: none !important;
        margin-bottom: 30px;
    }

    /* Headings and text */
    h1, h2, h3, p, span, label {
        color: #062745 !important;
        text-shadow: 1px 1px 4px rgba(255,255,255,0.7);
    }

    /* Buttons styling */
    .stButton>button {
        background-color: #ff0054 !important;
        color:white !important;
        border-radius: 25px;
        padding:12px 25px;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color:#e60047 !important;
        transform: scale(1.05);
    }

    /* Input boxes styling */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea, 
    .stSelectbox>div>div>div {
        border-radius:20px !important;
        padding:14px !important;
        font-size: 16px;
        border: 1px solid #ccc !important;
    }

    /* Selectbox hover */
    .stSelectbox>div>div>div:hover {
        border-color: #ff0054 !important;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# Sidebar menu
st.sidebar.title("🏠 Menu")
role = st.sidebar.selectbox("Hitamo uruhande rwawe:", ["Tenant", "Admin"])

# Main card overlay
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.title("Tenant Management System")
st.write("Murakaza neza! Hitamo uruhande rwawe muri sidebar kugirango utangire.")
st.markdown("</div>", unsafe_allow_html=True)

# Show portals based on role
if role == "Tenant":
    tenant_portal()
else:
    admin_portal()
