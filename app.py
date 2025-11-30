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
        background-image: linear-gradient(rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.7)), 
                          url('https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/landlord.png');
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
        background: rgba(255, 255, 255, 0.92) !important;
        color: #0b2545 !important;
        font-weight: bold;
        padding: 20px;
        border-radius: 12px;
        backdrop-filter: blur(10px);
        border-right: 3px solid #ff0054;
    }

    /* ================================
       MAIN CARD (CENTER BOX)
       ================================ */
    .card {
        background: rgba(255, 255, 255, 0.95);
        padding: 40px;
        border-radius: 25px;
        margin: 40px auto;
        box-shadow: 0px 12px 40px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        text-align: center;
        max-width: 800px;
    }

    /* ================================
       WELCOME HEADER STYLING
       ================================ */
    .welcome-header {
        background: linear-gradient(135deg, #ff0054, #6a11cb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 20px !important;
        text-shadow: none !important;
    }

    .welcome-subtitle {
        color: #062745 !important;
        font-size: 1.4rem !important;
        margin-bottom: 30px !important;
        font-weight: 400;
    }

    /* ================================
       FEATURE CARDS
       ================================ */
    .feature-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 30px 0;
        flex-wrap: wrap;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.15);
        text-align: center;
        flex: 1;
        min-width: 200px;
        max-width: 250px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-top: 4px solid #ff0054;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0px 12px 25px rgba(0, 0, 0, 0.2);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
    }
    
    .feature-title {
        color: #062745 !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        margin-bottom: 10px !important;
    }
    
    .feature-desc {
        color: #666 !important;
        font-size: 0.9rem !important;
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
        background: linear-gradient(135deg, #ff0054, #e60047) !important;
        color: white !important;
        border-radius: 30px;
        padding: 14px 30px;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0px 6px 15px rgba(255, 0, 84, 0.3);
        font-size: 1.1rem;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0px 8px 20px rgba(255, 0, 84, 0.4);
    }

    /* ================================
       INPUT FIELDS
       ================================ */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>div {
        border-radius: 20px !important;
        padding: 14px !important;
        border: 2px solid #e0e0e0 !important;
        font-size: 16px !important;
        background: rgba(255, 255, 255, 0.95) !important;
        transition: border-color 0.3s ease;
    }

    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus,
    .stSelectbox>div>div>div:focus {
        border-color: #ff0054 !important;
        box-shadow: 0 0 0 2px rgba(255, 0, 84, 0.1) !important;
    }

    /* ================================
       SIDEBAR SELECT BOX
       ================================ */
    .stSelectbox>div>div>div {
        background: white !important;
        border-radius: 15px !important;
    }

    /* ================================
       FOOTER STYLING
       ================================ */
    .footer {
        text-align: center;
        margin-top: 40px;
        padding: 20px;
        color: #062745 !important;
        font-size: 0.9rem;
        opacity: 0.8;
    }

    </style>
    """, unsafe_allow_html=True)

local_css()

# Sidebar menu
st.sidebar.title("🏠 Menu")
st.sidebar.markdown("---")
role = st.sidebar.selectbox("Hitamo uruhande rwawe:", ["Tenant", "Admin"])

# Main content with creative design
st.markdown("<div class='card'>", unsafe_allow_html=True)

# Welcome Header
st.markdown("<h1 class='welcome-header'>Tenant Management System</h1>", unsafe_allow_html=True)
st.markdown("<p class='welcome-subtitle'>Gestion des locataires & propriétés - Simplified Property Management</p>", unsafe_allow_html=True)

# Divider
st.markdown("---")

# Feature Cards
st.markdown("### 🔧 Services Available")
st.markdown("<div class='feature-container'>", unsafe_allow_html=True)

# Feature 1
st.markdown("""
<div class='feature-card'>
    <div class='feature-icon'>📋</div>
    <h3 class='feature-title'>Tenant Portal</h3>
    <p class='feature-desc'>Submit maintenance requests, pay rent, and communicate with property management</p>
</div>
""", unsafe_allow_html=True)

# Feature 2
st.markdown("""
<div class='feature-card'>
    <div class='feature-icon'>👨‍💼</div>
    <h3 class='feature-title'>Admin Dashboard</h3>
    <p class='feature-desc'>Manage properties, tenants, requests, and financial records efficiently</p>
</div>
""", unsafe_allow_html=True)

# Feature 3
st.markdown("""
<div class='feature-card'>
    <div class='feature-icon'>💬</div>
    <h3 class='feature-title'>Communication</h3>
    <p class='feature-desc'>Direct messaging between tenants and property managers</p>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Current Selection Highlight
st.markdown("---")
if role == "Tenant":
    st.success("🎯 **Currently Selected:** Tenant Portal - Access your tenant dashboard")
else:
    st.info("🎯 **Currently Selected:** Admin Portal - Access management tools")

# Quick Stats (placeholder - you can connect to real data later)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Active Tenants", "24", "+2")
with col2:
    st.metric("Pending Requests", "5", "-1")
with col3:
    st.metric("Properties", "8", "0")

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class='footer'>
    <p>🏠 Tenant Management System v2.0 | Built with Streamlit | © 2024 Property Management Solutions</p>
</div>
""", unsafe_allow_html=True)

# Show correct portal
if role == "Tenant":
    tenant_portal()
else:
    admin_portal()
