# -*- coding: utf-8 -*-
"""
Main app entry — enhanced with professional homepage design
"""
import streamlit as st
from tenant import tenant_portal
from admin import admin_portal
import os

st.set_page_config(
    page_title="Tenant Management System", 
    page_icon="🏠", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensure tenant_files folder exists
os.makedirs("tenant_files", exist_ok=True)

# Custom CSS for professional UI
def local_css():
    st.markdown("""
    <style>
    /* Main background */
    .stApp { 
        background: linear-gradient(135deg, #f8fafc 0%, #eef5ff 100%) !important; 
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #0b2545 0%, #1a365d 100%) !important; 
        color:white !important; 
        padding-top: 2rem;
    }
    
    /* Remove default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Card styling */
    .dashboard-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #e2e8f0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }
    
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    /* Hero section */
    .hero-container {
        background: linear-gradient(90deg, #0b63d6 0%, #0b2545 100%);
        border-radius: 20px;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
        color: white !important;
    }
    
    .hero-title {
        color: white !important;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
    }
    
    .hero-subtitle {
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 1.2rem !important;
        font-weight: 400 !important;
        max-width: 800px;
    }
    
    /* Feature icons */
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: #0b63d6;
    }
    
    /* Stats cards */
    .stats-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        text-align: center;
    }
    
    .stats-number {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0b2545;
        margin-bottom: 0.5rem;
    }
    
    .stats-label {
        color: #64748b;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(90deg, #0b63d6 0%, #0b80ff 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(11, 99, 214, 0.2) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(11, 99, 214, 0.3) !important;
        background: linear-gradient(90deg, #084ab0 0%, #0b63d6 100%) !important;
    }
    
    /* Input styling */
    .stTextInput>div>div>input, 
    .stSelectbox>div>div>select,
    .stSelectbox>div>div>div {
        border-radius: 12px !important;
        border: 1px solid #cbd5e1 !important;
        padding: 12px !important;
        background: white !important;
    }
    
    /* Headers */
    h1, h2, h3, .section-title {
        color: #0b2545 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
    }
    
    h1 { font-size: 2.5rem !important; }
    h2 { font-size: 2rem !important; }
    h3 { font-size: 1.5rem !important; }
    
    /* Text */
    p, span, label, .card-text {
        color: #475569 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        line-height: 1.6 !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .hero-title { font-size: 2rem !important; }
        .hero-subtitle { font-size: 1rem !important; }
    }
    
    /* Status indicators */
    .status-active {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #10b981;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-pending {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #f59e0b;
        border-radius: 50%;
        margin-right: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# Sidebar with enhanced design
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: white !important; font-size: 1.8rem;">🏠 TMS</h1>
        <p style="color: #94a3b8; font-size: 0.9rem;">Tenant Management System</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='background-color: #2d3748; height: 1px; border: none; margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    role = st.selectbox("Hitamo Uruhare", ["Tenant", "Admin"], key="role_select")
    
    st.markdown("<hr style='background-color: #2d3748; height: 1px; border: none; margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    # Add quick stats in sidebar
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 12px; margin-top: 2rem;">
        <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 0.5rem;">System Status</p>
        <p style="color: white; font-weight: 600;"><span class="status-active"></span> All Systems Operational</p>
    </div>
    """, unsafe_allow_html=True)

# Main content area
# Hero Section
st.markdown("""
<div class="hero-container">
    <h1 class="hero-title">🏠 Tenant Management System</h1>
    <p class="hero-subtitle">Streamlined property management solution for landlords and tenants. Manage leases, payments, maintenance requests, and communications in one secure platform.</p>
</div>
""", unsafe_allow_html=True)

# Dashboard stats (if admin) or welcome message (if tenant)
if role == "Admin":
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">42</div>
            <div class="stats-label">Active Tenants</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">98%</div>
            <div class="stats-label">On-time Payments</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">7</div>
            <div class="stats-label">Pending Requests</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">15</div>
            <div class="stats-label">Properties</div>
        </div>
        """, unsafe_allow_html=True)

# Main content based on role
if role == "Tenant":
    # Show tenant portal with enhanced UI
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <h3>📋 Tenant Portal</h3>
            <p>Access your lease information, submit maintenance requests, view payment history, and communicate with property management.</p>
            <p style="color: #0b63d6; font-weight: 600;">Please use the form below to access your account.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="dashboard-card">
            <h3>💡 Quick Tips</h3>
            <ul style="color: #475569; padding-left: 1.2rem;">
                <li>Keep your contact information updated</li>
                <li>Submit maintenance requests with photos</li>
                <li>Set up automatic payments for convenience</li>
                <li>Check announcements regularly</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    tenant_portal()
    
else:
    # Show admin portal with enhanced UI
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <h3>👨‍💼 Admin Portal</h3>
            <p>Manage all properties, tenants, leases, and financial records. Generate reports, process requests, and oversee operations.</p>
            <p style="color: #0b63d6; font-weight: 600;">Use the form below to access administrative functions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="dashboard-card">
            <h3>📊 Recent Activity</h3>
            <ul style="color: #475569; padding-left: 1.2rem;">
                <li><span class="status-pending"></span> 3 new tenant applications</li>
                <li><span class="status-active"></span> Lease renewals due: 5</li>
                <li><span class="status-active"></span> Maintenance completed: 12</li>
                <li><span class="status-pending"></span> Invoices pending: 2</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    admin_portal()

# Footer
st.markdown("""
<hr style="background-color: #e2e8f0; height: 1px; border: none; margin: 3rem 0 1rem 0;">
<div style="text-align: center; color: #64748b; font-size: 0.9rem; padding: 1rem;">
    <p>© 2023 Tenant Management System. All rights reserved.</p>
    <p style="font-size: 0.8rem; margin-top: 0.5rem;">v2.1.0 | Secure & Encrypted</p>
</div>
""", unsafe_allow_html=True)
