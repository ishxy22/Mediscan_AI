import streamlit as st
from utils.styles import load_styles, render_sidebar

st.set_page_config(
    page_title="About - Health Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_styles()
render_sidebar()

# Page heading
st.markdown('<p class="page-title" style="color: #ffffff;">About This App</p>', unsafe_allow_html=True)

# Main info card
st.markdown("""
<div style="background:#1c2128;border:1px solid #30363d;border-radius:12px;padding:1.5rem;margin-bottom:1rem;">
    <h3 style="color: #a78bfa; margin-top: 0;">What does it do?</h3>
    <p class="muted-text" style="margin-bottom: 0;">This is an AI-powered health awareness tool that helps users understand possible conditions based on symptoms. It provides educational insights and general health information to help you make informed decisions about seeking professional medical care.</p>
</div>
""", unsafe_allow_html=True)

# How to use it
st.markdown("""
<div style="background:#1c2128;border:1px solid #30363d;border-radius:12px;padding:1.5rem;margin-bottom:1rem;">
    <h3 style="color: #a78bfa; margin-top: 0;">How to use it</h3>
    <ol class="muted-text" style="line-height: 1.8; margin-bottom: 0;">
        <li><strong style="color: white; font-family: 'Inter', sans-serif;">Check My Symptoms</strong>: Select your symptoms from the comprehensive list to get AI-powered insights about possible health conditions.</li>
        <li><strong style="color: white; font-family: 'Inter', sans-serif;">AI Assistant</strong>: Chat naturally about how you're feeling using conversational language.</li>
        <li><strong style="color: white; font-family: 'Inter', sans-serif;">My Dashboard</strong>: Track your health history, view personal metrics, and monitor your symptom patterns over time.</li>
        <li><strong style="color: white; font-family: 'Inter', sans-serif;">Book Appointment</strong>: Schedule consultations with healthcare professionals when needed.</li>
        <li><strong style="color: white; font-family: 'Inter', sans-serif;">My Health History</strong>: View all your previous symptom checks and predictions in one place.</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# Important disclaimer
st.markdown("""
<div style="background:#1c2128;border:1px solid #da3633;box-shadow:0 0 12px rgba(218,54,51,0.2);border-radius:12px;padding:1.5rem;margin-bottom:1rem;">
    <h3 style="color: #ef4444; font-family: 'Inter', sans-serif; margin-top: 0;">Important Disclaimer</h3>
    <p style="color: #fca5a5; margin-bottom: 0; font-family: 'Inter', sans-serif;">This app is not a substitute for professional medical advice. Always consult a qualified doctor for diagnosis and treatment. The insights provided are for educational purposes only and should not be used to make medical decisions.</p>
</div>
""", unsafe_allow_html=True)

# Privacy section
st.markdown("""
<div style="background:#1c2128;border:1px solid #30363d;border-radius:12px;padding:1.5rem;margin-bottom:1rem;">
    <h3 style="color: #a78bfa; margin-top: 0;">Privacy</h3>
    <p class="muted-text">Your privacy is important to us. No personal data is stored permanently on servers.</p>
    <p class="muted-text" style="margin-bottom: 0;">All information is session-based and automatically cleared when you close your browser tab or clear your history. Your health data remains private and temporary during your session.</p>
</div>
""", unsafe_allow_html=True)

# Technology used
st.markdown("""
<div style="background:#1c2128;border:1px solid #30363d;border-radius:12px;padding:1.5rem;margin-bottom:1rem;">
    <h3 style="color: #a78bfa; margin-top: 0;">Technology Used</h3>
    <p class="muted-text" style="margin-bottom: 1.5rem;">This application is built with modern, reliable technologies:</p>
    <div>
        <span style="background:#21262d;border:1px solid #30363d;border-radius:6px;padding:4px 14px;margin:4px;font-family:'JetBrains Mono',monospace;font-size:0.85rem;display:inline-block;color:#c9d1d9;">Python</span>
        <span style="background:#21262d;border:1px solid #30363d;border-radius:6px;padding:4px 14px;margin:4px;font-family:'JetBrains Mono',monospace;font-size:0.85rem;display:inline-block;color:#c9d1d9;">Streamlit</span>
        <span style="background:#21262d;border:1px solid #30363d;border-radius:6px;padding:4px 14px;margin:4px;font-family:'JetBrains Mono',monospace;font-size:0.85rem;display:inline-block;color:#c9d1d9;">Scikit-learn</span>
        <span style="background:#21262d;border:1px solid #30363d;border-radius:6px;padding:4px 14px;margin:4px;font-family:'JetBrains Mono',monospace;font-size:0.85rem;display:inline-block;color:#c9d1d9;">Random Forest</span>
        <span style="background:#21262d;border:1px solid #30363d;border-radius:6px;padding:4px 14px;margin:4px;font-family:'JetBrains Mono',monospace;font-size:0.85rem;display:inline-block;color:#c9d1d9;">Pandas</span>
    </div>
</div>
""", unsafe_allow_html=True)
