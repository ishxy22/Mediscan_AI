import streamlit as st
from utils.styles import load_styles, render_sidebar

st.set_page_config(
    page_title="MediScan AI - Home",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_styles()
render_sidebar()

# Top section
st.markdown('<div class="hero-title" style="margin-top: 2rem;">MediScan AI</div>', unsafe_allow_html=True)
st.markdown('<p class="muted-text" style="text-align: center; font-size: 1.2rem; margin-bottom: 3rem;">AI-powered health insights — for awareness only, not medical advice</p>', unsafe_allow_html=True)

# Stats row
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card" style="text-align: center;">
        <div class="metric-number" style="font-size: 2.5rem; color: #ffffff; font-weight: 500;">41</div>
        <div class="section-title" style="color: #8b949e; font-size: 0.8rem; margin:0;">TOTAL DISEASES</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card" style="text-align: center;">
        <div class="metric-number" style="font-size: 2.5rem; color: #ffffff; font-weight: 500;">131</div>
        <div class="section-title" style="color: #8b949e; font-size: 0.8rem; margin:0;">TOTAL SYMPTOMS</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card" style="text-align: center;">
        <div class="metric-number" style="font-size: 2.5rem; color: #ffffff; font-weight: 500;">94%</div>
        <div class="section-title" style="color: #8b949e; font-size: 0.8rem; margin:0;">MODEL ACCURACY</div>
    </div>
    """, unsafe_allow_html=True)

# Feature cards section
st.markdown('<h2 style="text-align: center; color: #ffffff; margin: 3rem 0 2rem 0; font-weight: 700;">What can I do for you?</h2>', unsafe_allow_html=True)

# 2x2 grid of feature cards
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

# Card 1: Check My Symptoms
with row1_col1:
    st.markdown("""
    <div class="feature-card" style="height: 100%; display: flex; flex-direction: column;">
        <div style="margin-bottom: 1rem;">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#7c3aed" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
        </div>
        <div style="font-weight: 600; font-size: 1.25rem; color: #ffffff; margin-bottom: 0.5rem; font-family: 'Inter', sans-serif;">Check My Symptoms</div>
        <div class="muted-text" style="margin-bottom: 1.5rem;">Select your symptoms and get instant disease insights</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Check Symptoms", key="home_symptoms", use_container_width=True, type="primary"):
        st.switch_page('pages/09_prediction.py')

# Card 2: Ask AI Assistant
with row1_col2:
    st.markdown("""
    <div class="feature-card" style="height: 100%; display: flex; flex-direction: column;">
        <div style="margin-bottom: 1rem;">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#7c3aed" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/><line x1="8" y1="16" x2="8" y2="16"/><line x1="16" y1="16" x2="16" y2="16"/></svg>
        </div>
        <div style="font-weight: 600; font-size: 1.25rem; color: #ffffff; margin-bottom: 0.5rem; font-family: 'Inter', sans-serif;">Ask AI Assistant</div>
        <div class="muted-text" style="margin-bottom: 1.5rem;">Chat naturally about how you feel</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Start Chat", key="home_chatbot", use_container_width=True, type="primary"):
        st.switch_page('pages/10_chatbot.py')

# Card 3: Book Appointment
with row2_col1:
    st.markdown("""
    <div class="feature-card" style="height: 100%; display: flex; flex-direction: column; margin-top: 1rem;">
        <div style="margin-bottom: 1rem;">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#7c3aed" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
        </div>
        <div style="font-weight: 600; font-size: 1.25rem; color: #ffffff; margin-bottom: 0.5rem; font-family: 'Inter', sans-serif;">Book Appointment</div>
        <div class="muted-text" style="margin-bottom: 1.5rem;">Schedule with a specialist doctor</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Book Now", key="home_appointment", use_container_width=True, type="primary"):
        st.switch_page('pages/appointment.py')

# Card 4: My Dashboard
with row2_col2:
    st.markdown("""
    <div class="feature-card" style="height: 100%; display: flex; flex-direction: column; margin-top: 1rem;">
        <div style="margin-bottom: 1rem;">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#7c3aed" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
        </div>
        <div style="font-weight: 600; font-size: 1.25rem; color: #ffffff; margin-bottom: 0.5rem; font-family: 'Inter', sans-serif;">My Dashboard</div>
        <div class="muted-text" style="margin-bottom: 1.5rem;">Track your health history and profile</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Dashboard", key="home_dashboard", use_container_width=True, type="primary"):
        st.switch_page('pages/dashboard.py')

# Bottom info box
st.markdown("""
<div class="info-box" style="margin-top: 3rem; text-align: center;">
    <p class="muted-text mono-text" style="margin: 0;">This app is for educational purposes only. Always consult a qualified medical professional for diagnosis and treatment.</p>
</div>
""", unsafe_allow_html=True)
