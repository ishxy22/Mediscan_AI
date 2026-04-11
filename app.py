import streamlit as st
from utils.styles import load_styles, render_sidebar

from pathlib import Path
import os

st.set_page_config(
    page_title="MediScan AI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_styles()
render_sidebar()

_ROOT = Path(__file__).resolve().parent

# Top section
st.markdown("""
<div style="text-align:center;padding:3rem 0 2rem 0;">
    <h1 style="font-family:'Inter',sans-serif;
               font-size:3.5rem;
               font-weight:800;
               color:#ffffff;
               letter-spacing:-2px;
               margin-bottom:0.5rem;
               line-height:1.1;">
        MediScan AI
    </h1>
    <p style="font-family:'Inter',sans-serif;
              font-size:1.1rem;
              color:#8b949e;
              font-weight:400;
              margin-top:0.5rem;
              letter-spacing:0.3px;">
        AI-powered health insights — for awareness only, 
        not medical advice
    </p>
</div>
""", unsafe_allow_html=True)

# Stats row
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
<div style="background:#1c2128;
            border:1px solid #30363d;
            border-radius:12px;
            padding:1.5rem;
            text-align:center;
            transition:all 0.2s ease;">
    <div style="font-family:'JetBrains Mono',monospace;
                font-size:2.5rem;
                font-weight:700;
                color:#ffffff;">41</div>
    <div style="font-family:'Inter',sans-serif;
                font-size:0.75rem;
                letter-spacing:1.5px;
                text-transform:uppercase;
                color:#8b949e;
                margin-top:0.3rem;">Total Diseases</div>
</div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
<div style="background:#1c2128;
            border:1px solid #30363d;
            border-radius:12px;
            padding:1.5rem;
            text-align:center;
            transition:all 0.2s ease;">
    <div style="font-family:'JetBrains Mono',monospace;
                font-size:2.5rem;
                font-weight:700;
                color:#ffffff;">131</div>
    <div style="font-family:'Inter',sans-serif;
                font-size:0.75rem;
                letter-spacing:1.5px;
                text-transform:uppercase;
                color:#8b949e;
                margin-top:0.3rem;">Total Symptoms</div>
</div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
<div style="background:#1c2128;
            border:1px solid #30363d;
            border-radius:12px;
            padding:1.5rem;
            text-align:center;
            transition:all 0.2s ease;">
    <div style="font-family:'JetBrains Mono',monospace;
                font-size:2.5rem;
                font-weight:700;
                color:#ffffff;">94%</div>
    <div style="font-family:'Inter',sans-serif;
                font-size:0.75rem;
                letter-spacing:1.5px;
                text-transform:uppercase;
                color:#8b949e;
                margin-top:0.3rem;">Model Accuracy</div>
</div>
    """, unsafe_allow_html=True)

# Feature cards section
st.markdown("""
<h2 style="font-family:'Inter',sans-serif;
           font-size:1.8rem;
           font-weight:700;
           color:#ffffff;
           text-align:center;
           margin:2rem 0 1.5rem 0;
           letter-spacing:-0.5px;">
    What can I do for you?
</h2>
""", unsafe_allow_html=True)

# 2x2 grid of feature cards
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

# Card 1: Check My Symptoms
with row1_col1:
    st.markdown("""
<div style="background:#1c2128;
            border:1px solid #30363d;
            border-radius:12px;
            padding:1.5rem;
            margin-bottom:0.5rem;
            transition:all 0.25s ease;">
    <div style="font-family:'Inter',sans-serif;
                font-size:1.1rem;
                font-weight:600;
                color:#ffffff;
                margin-bottom:0.4rem;">
        Check My Symptoms
    </div>
    <div style="font-family:'Inter',sans-serif;
                font-size:0.9rem;
                color:#8b949e;">
        Select your symptoms and get instant disease insights
    </div>
</div>
    """, unsafe_allow_html=True)
    if st.button("Check Symptoms", key="home_symptoms", use_container_width=True, type="primary"):
        st.switch_page('pages/09_prediction.py')

# Card 2: Ask AI Assistant
with row1_col2:
    st.markdown("""
<div style="background:#1c2128;
            border:1px solid #30363d;
            border-radius:12px;
            padding:1.5rem;
            margin-bottom:0.5rem;
            transition:all 0.25s ease;">
    <div style="font-family:'Inter',sans-serif;
                font-size:1.1rem;
                font-weight:600;
                color:#ffffff;
                margin-bottom:0.4rem;">
        Ask AI Assistant
    </div>
    <div style="font-family:'Inter',sans-serif;
                font-size:0.9rem;
                color:#8b949e;">
        Chat naturally about how you feel
    </div>
</div>
    """, unsafe_allow_html=True)
    if st.button("Start Chat", key="home_chatbot", use_container_width=True, type="primary"):
        st.switch_page('pages/10_chatbot.py')

# Card 3: Book Appointment
with row2_col1:
    st.markdown("""
<div style="background:#1c2128;
            border:1px solid #30363d;
            border-radius:12px;
            padding:1.5rem;
            margin-bottom:0.5rem;
            transition:all 0.25s ease;">
    <div style="font-family:'Inter',sans-serif;
                font-size:1.1rem;
                font-weight:600;
                color:#ffffff;
                margin-bottom:0.4rem;">
        Book Appointment
    </div>
    <div style="font-family:'Inter',sans-serif;
                font-size:0.9rem;
                color:#8b949e;">
        Schedule with a specialist doctor
    </div>
</div>
    """, unsafe_allow_html=True)
    if st.button("Book Now", key="home_appointment", use_container_width=True, type="primary"):
        st.switch_page('pages/appointment.py')

# Card 4: My Dashboard
with row2_col2:
    st.markdown("""
<div style="background:#1c2128;
            border:1px solid #30363d;
            border-radius:12px;
            padding:1.5rem;
            margin-bottom:0.5rem;
            transition:all 0.25s ease;">
    <div style="font-family:'Inter',sans-serif;
                font-size:1.1rem;
                font-weight:600;
                color:#ffffff;
                margin-bottom:0.4rem;">
        My Dashboard
    </div>
    <div style="font-family:'Inter',sans-serif;
                font-size:0.9rem;
                color:#8b949e;">
        Track your health history and profile
    </div>
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
