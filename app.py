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
        background-image: linear-gradient(rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.15)), 
                          url('https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/landlord.png');
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
        min-height: 100vh;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* ================================
       SIDEBAR STYLING - GLASS MORPHISM
       ================================ */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.85) !important;
        color: #0b2545 !important;
        font-weight: bold;
        padding: 25px;
        border-radius: 20px;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

    /* ================================
       MAIN CARD (GLASS MORPHISM EFFECT)
       ================================ */
    .main-card {
        background: rgba(255, 255, 255, 0.92);
        padding: 50px;
        border-radius: 30px;
        margin: 40px auto;
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        text-align: center;
        max-width: 900px;
    }

    /* ================================
       ANIMATED HEADER
       ================================ */
    .animated-header {
        background: linear-gradient(135deg, #ff0054, #7928CA, #007CF0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 4rem !important;
        font-weight: 900 !important;
        margin-bottom: 10px !important;
        text-shadow: none !important;
        animation: fadeInUp 1s ease-out;
    }

    .welcome-subtitle {
        color: #062745 !important;
        font-size: 1.6rem !important;
        margin-bottom: 40px !important;
        font-weight: 500;
        animation: fadeInUp 1s ease-out 0.2s both;
    }

    /* ================================
       FEATURE CARDS GRID
       ================================ */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 25px;
        margin: 40px 0;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 30px 25px;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 2px solid transparent;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(135deg, #ff0054, #7928CA);
    }
    
    .feature-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        border-color: #ff0054;
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 20px;
        display: block;
    }
    
    .feature-title {
        color: #062745 !important;
        font-weight: 800 !important;
        font-size: 1.4rem !important;
        margin-bottom: 15px !important;
    }
    
    .feature-desc {
        color: #666 !important;
        font-size: 1rem !important;
        line-height: 1.6;
    }

    /* ================================
       ANIMATIONS
       ================================ */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    /* ================================
       BUTTON DESIGN - MODERN
       ================================ */
    .stButton>button {
        background: linear-gradient(135deg, #ff0054, #e60047) !important;
        color: white !important;
        border-radius: 50px;
        padding: 16px 35px;
        font-weight: 700;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 8px 20px rgba(255, 0, 84, 0.3);
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 25px rgba(255, 0, 84, 0.4);
        animation: pulse 1s infinite;
    }

    /* ================================
       INPUT FIELDS - MODERN
       ================================ */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>div {
        border-radius: 15px !important;
        padding: 16px 20px !important;
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
        transform: scale(1.02);
    }

    /* ================================
       SELECTION INDICATOR
       ================================ */
    .selection-badge {
        background: linear-gradient(135deg, #ff0054, #7928CA);
        color: white !important;
        padding: 12px 25px;
        border-radius: 25px;
        font-weight: 700;
        display: inline-block;
        margin: 20px 0;
        box-shadow: 0 5px 15px rgba(255, 0, 84, 0.3);
    }

    /* ================================
       STATS CARDS
       ================================ */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }
    
    .stat-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #ff0054;
    }

    /* ================================
       FOOTER STYLING
       ================================ */
    .footer {
        text-align: center;
        margin-top: 50px;
        padding: 25px;
        color: #062745 !important;
        font-size: 1rem;
        opacity: 0.9;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }

    /* ================================
       RESPONSIVE DESIGN
       ================================ */
    @media (max-width: 768px) {
        .animated-header {
            font-size: 2.5rem !important;
        }
        .features-grid {
            grid-template-columns: 1fr;
        }
    }

    </style>
    """, unsafe_allow_html=True)

local_css()

# Sidebar menu with enhanced design
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 30px;">
    <h2 style="color: #062745; margin-bottom: 5px;">🏠</h2>
    <h3 style="color: #062745; margin: 0;">System Menu</h3>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
role = st.sidebar.selectbox("**Hitamo uruhande rwawe:**", ["Tenant", "Admin"])
st.sidebar.markdown("---")

# Quick help section in sidebar
st.sidebar.markdown("""
<div style="background: rgba(255, 0, 84, 0.1); padding: 15px; border-radius: 15px; margin-top: 20px;">
    <h4 style="color: #062745; margin: 0 0 10px 0;">💡 Quick Help</h4>
    <p style="color: #062745; font-size: 0.9rem; margin: 0;">
        <strong>Tenant:</strong> Submit requests, pay rent, communicate<br>
        <strong>Admin:</strong> Manage properties, view reports, handle requests
    </p>
</div>
""", unsafe_allow_html=True)

# Main content with creative design
st.markdown("<div class='main-card'>", unsafe_allow_html=True)

# Animated Welcome Header
st.markdown("<h1 class='animated-header'>Tenant Management System</h1>", unsafe_allow_html=True)
st.markdown("<p class='welcome-subtitle'>🏠 Murakaza neza! Welcome to Your Smart Property Management Solution</p>", unsafe_allow_html=True)

# Divider with style
st.markdown("<hr style='border: none; height: 3px; background: linear-gradient(135deg, #ff0054, #7928CA); border-radius: 10px; margin: 30px 0;'>", unsafe_allow_html=True)

# Feature Cards Grid
st.markdown("### 🚀 What You Can Do")
st.markdown("<div class='features-grid'>", unsafe_allow_html=True)

# Feature 1
st.markdown("""
<div class='feature-card'>
    <div class='feature-icon'>📋</div>
    <h3 class='feature-title'>Tenant Portal</h3>
    <p class='feature-desc'>Submit maintenance requests, pay rent online, and communicate directly with property management team</p>
</div>
""", unsafe_allow_html=True)

# Feature 2
st.markdown("""
<div class='feature-card'>
    <div class='feature-icon'>👨‍💼</div>
    <h3 class='feature-title'>Admin Dashboard</h3>
    <p class='feature-desc'>Complete property management with tenant tracking, financial reports, and request handling</p>
</div>
""", unsafe_allow_html=True)

# Feature 3
st.markdown("""
<div class='feature-card'>
    <div class='feature-icon'>💬</div>
    <h3 class='feature-title'>Live Communication</h3>
    <p class='feature-desc'>Real-time messaging between tenants and property managers for quick issue resolution</p>
</div>
""", unsafe_allow_html=True)

# Feature 4
st.markdown("""
<div class='feature-card'>
    <div class='feature-icon'>📊</div>
    <h3 class='feature-title'>Analytics & Reports</h3>
    <p class='feature-desc'>Comprehensive insights into property performance, occupancy rates, and financial metrics</p>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Current Selection Highlight
st.markdown("---")
if role == "Tenant":
    st.markdown("<div class='selection-badge'>🎯 Currently Selected: Tenant Portal - Ready to access your personal dashboard</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='selection-badge'>🎯 Currently Selected: Admin Portal - Ready to manage properties and tenants</div>", unsafe_allow_html=True)

# Quick Stats Dashboard
st.markdown("### 📈 System Overview")
st.markdown("<div class='stats-container'>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class='stat-card'>
        <h3 style='color: #062745; margin: 0;'>24</h3>
        <p style='color: #666; margin: 5px 0 0 0;'>Active Tenants</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='stat-card'>
        <h3 style='color: #062745; margin: 0;'>5</h3>
        <p style='color: #666; margin: 5px 0 0 0;'>Pending Requests</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='stat-card'>
        <h3 style='color: #062745; margin: 0;'>8</h3>
        <p style='color: #666; margin: 5px 0 0 0;'>Properties</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class='stat-card'>
        <h3 style='color: #062745; margin: 0;'>98%</h3>
        <p style='color: #666; margin: 5px 0 0 0;'>Satisfaction</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class='footer'>
    <p>🏠 <strong>Tenant Management System Pro v2.0</strong> | Built with Streamlit | 
    <span style='color: #ff0054;'>© 2024 Property Management Solutions Rwanda</span></p>
    <p style='font-size: 0.9rem; margin-top: 10px;'>Efficient • Reliable • Modern</p>
</div>
""", unsafe_allow_html=True)

# Show correct portal
if role == "Tenant":
    tenant_portal()
else:
    admin_portal()
