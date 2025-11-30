# -*- coding: utf-8 -*-
"""
Tenant & Landlord Management System
"""
import streamlit as st
from tenant import tenant_portal
from admin import admin_portal
import os

# Page configuration
st.set_page_config(page_title="Tenant & Landlord System", page_icon="🏠", layout="wide")

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
        background-image: linear-gradient(rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.15)), 
                          url('landlord.png');
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
        min-height: 100vh;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* ================================
       SIDEBAR STYLING - CLEAN DESIGN
       ================================ */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.90) !important;
        color: #0b2545 !important;
        padding: 25px;
        border-radius: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin: 15px;
    }

    /* ================================
       MAIN CARD (CLEAN DESIGN)
       ================================ */
    .main-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 40px;
        border-radius: 25px;
        margin: 40px auto;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        text-align: center;
        max-width: 850px;
    }

    /* ================================
       HEADER STYLING
       ================================ */
    .main-header {
        background: linear-gradient(135deg, #ff0054, #7928CA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 10px !important;
    }

    .welcome-subtitle {
        color: #062745 !important;
        font-size: 1.4rem !important;
        margin-bottom: 30px !important;
        font-weight: 500;
    }

    /* ================================
       ROLE SELECTION CARDS
       ================================ */
    .role-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin: 30px 0;
    }
    
    .role-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 30px 20px;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: all 0.3s ease;
        border: 3px solid transparent;
    }
    
    .role-card.tenant {
        border-color: #007CF0;
    }
    
    .role-card.landlord {
        border-color: #ff0054;
    }
    
    .role-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    }
    
    .role-icon {
        font-size: 3rem;
        margin-bottom: 15px;
        display: block;
    }
    
    .role-title {
        color: #062745 !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        margin-bottom: 10px !important;
    }
    
    .role-desc {
        color: #666 !important;
        font-size: 1rem !important;
        line-height: 1.5;
    }

    /* ================================
       BUTTON DESIGN
       ================================ */
    .stButton>button {
        background: linear-gradient(135deg, #ff0054, #e60047) !important;
        color: white !important;
        border-radius: 50px;
        padding: 14px 30px;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(255, 0, 84, 0.3);
        font-size: 1rem;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(255, 0, 84, 0.4);
    }

    /* ================================
       INPUT FIELDS
       ================================ */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>div {
        border-radius: 15px !important;
        padding: 14px 18px !important;
        border: 2px solid #e0e0e0 !important;
        font-size: 16px !important;
        background: rgba(255, 255, 255, 0.95) !important;
        transition: all 0.3s ease;
    }

    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus,
    .stSelectbox>div>div>div:focus {
        border-color: #ff0054 !important;
        box-shadow: 0 0 0 3px rgba(255, 0, 84, 0.1) !important;
    }

    /* ================================
       SELECTION INDICATOR
       ================================ */
    .selection-badge {
        background: linear-gradient(135deg, #ff0054, #7928CA);
        color: white !important;
        padding: 12px 25px;
        border-radius: 25px;
        font-weight: 600;
        display: inline-block;
        margin: 20px 0;
    }

    /* ================================
       SIMPLE STATS
       ================================ */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 15px;
        margin: 25px 0;
    }
    
    .stat-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
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

    /* ================================
       RESPONSIVE DESIGN
       ================================ */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem !important;
        }
        .role-container {
            grid-template-columns: 1fr;
        }
    }

    </style>
    """, unsafe_allow_html=True)

local_css()

# Sidebar menu - Clear and Simple
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <h2 style="color: #062745; margin-bottom: 5px;">🏠</h2>
    <h3 style="color: #062745; margin: 0;">Choose Your Role</h3>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
role = st.sidebar.selectbox("**Select your role:**", ["Tenant", "Landlord"])
st.sidebar.markdown("---")

# Simple help in sidebar
st.sidebar.markdown("""
<div style="background: rgba(255, 0, 84, 0.05); padding: 15px; border-radius: 15px;">
    <p style="color: #062745; font-size: 0.9rem; margin: 0;">
        <strong>Tenant:</strong> Submit requests, pay rent<br>
        <strong>Landlord:</strong> Manage tenants, view payments
    </p>
</div>
""", unsafe_allow_html=True)

# Main content - Clear and Focused
st.markdown("<div class='main-card'>", unsafe_allow_html=True)

# Clear Header
st.markdown("<h1 class='main-header'>Tenant & Landlord System</h1>", unsafe_allow_html=True)
st.markdown("<p class='welcome-subtitle'>🏠 Murakaza neza! Simple platform for tenants and landlords</p>", unsafe_allow_html=True)

# Divider
st.markdown("---")

# Role Selection Cards
st.markdown("### 👥 Choose Your Role")
st.markdown("<div class='role-container'>", unsafe_allow_html=True)

# Tenant Card
st.markdown("""
<div class='role-card tenant'>
    <div class='role-icon'>👤</div>
    <h3 class='role-title'>Tenant</h3>
    <p class='role-desc'>Submit maintenance requests, pay rent, communicate with your landlord</p>
</div>
""", unsafe_allow_html=True)

# Landlord Card
st.markdown("""
<div class='role-card landlord'>
    <div class='role-icon'>🏢</div>
    <h3 class='role-title'>Landlord</h3>
    <p class='role-desc'>Manage tenants, handle requests, track payments, and communicate</p>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Current Selection
st.markdown("---")
if role == "Tenant":
    st.markdown("<div class='selection-badge'>✅ Currently Selected: Tenant - Access your personal dashboard</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='selection-badge'>✅ Currently Selected: Landlord - Access management dashboard</div>", unsafe_allow_html=True)

# Simple Stats
st.markdown("### 📊 Quick Overview")
st.markdown("<div class='stats-container'>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class='stat-card'>
        <h3 style='color: #062745; margin: 0;'>Tenants</h3>
        <p style='color: #ff0054; font-size: 1.5rem; font-weight: bold; margin: 5px 0 0 0;'>24</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='stat-card'>
        <h3 style='color: #062745; margin: 0;'>Requests</h3>
        <p style='color: #007CF0; font-size: 1.5rem; font-weight: bold; margin: 5px 0 0 0;'>5</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='stat-card'>
        <h3 style='color: #062745; margin: 0;'>Active</h3>
        <p style='color: #00C851; font-size: 1.5rem; font-weight: bold; margin: 5px 0 0 0;'>8</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Simple Footer
st.markdown("""
<div class='footer'>
    <p>🏠 <strong>Tenant & Landlord System</strong> | Simple • Efficient • Clear</p>
</div>
""", unsafe_allow_html=True)

# Show correct portal
if role == "Tenant":
    tenant_portal()
else:
    admin_portal()
