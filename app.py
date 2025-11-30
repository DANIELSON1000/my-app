# -*- coding: utf-8 -*-
"""
Main app entry — Tenant Management System with attractive wallpaper and UI.
"""
import streamlit as st
from tenant import tenant_portal
from admin import admin_portal
import os

# Page configuration
st.set_page_config(page_title="Tenant Management System", page_icon="🏠", layout="wide")

# Ensure tenant_files folder exists
os.makedirs("tenant_files", exist_ok=True)

# Custom CSS for wallpaper and UI
def local_css():
    st.markdown(f"""
    <style>
    /* Full-screen background image */
    .stApp {{
        background: url('pictures/landlord.png') no-repeat center center fixed;
        background-size: cover;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #062745;
    }}

    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background: rgba(11, 37, 69, 0.9) !important;
        color:white !important;
        font-weight: bold;
        font-size: 16px;
    }}

    /* Transparent card overlay for main content */
    .card {{
        background: rgba(255, 255, 255, 0.85) !important;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.2) !important;
        border: none !important;
        margin-bottom: 20px;
    }}

    /* Headings and text */
    h1, h2, h3, p, span, label {{
        color: #062745 !important;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.6);
    }}

    /* Buttons styling */
    .stButton>button {{
        background-color: #0b63d6 !important;
        color:white !important;
        border-radius:12px;
        padding:12px 20px;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.2);
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background-color:#084ab0 !important;
        transform: scale(1.05);
    }}

    /* Input boxes styling */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea, 
    .stSelectbox>div>div>div {{
        border-radius:12px !important;
        padding:12px !important;
        font-size: 16px;
        border: 1px solid #ccc !important;
    }}

    /* Selectbox hover */
    .stSelectbox>div>div>div:hover {{
        border-color: #0b63d6 !important;
    }}

    </style>
    """, unsafe_allow_html=True)

local_css()

# Sidebar menu
st.sidebar.title("🏠 Menu")
role = st.sidebar.selectbox("Hitamo uruhande rwawe:", ["Tenant", "Admin"])

# Main title with overlay card
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.title("Tenant Management System")
st.write("Murakaza neza!")
st.markdown("</div>", unsafe_allow_html=True)

# Show portals based on role
if role == "Tenant":
    tenant_portal()
else:
    admin_portal()
