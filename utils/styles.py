import streamlit as st

def load_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

* {
    font-family: 'Inter', sans-serif;
    box-sizing: border-box;
}

.stApp {
    background-color: #0d1117;
    color: #c9d1d9;
}

section[data-testid="stSidebar"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    transform: none !important;
    min-width: 240px !important;
    max-width: 240px !important;
    background-color: #161b22 !important;
}

button[data-testid="collapsedControl"] {
    display: none !important;
}

div[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

[data-testid="stSidebarNav"] {
    display: none !important;
}

section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    color: #8b949e !important;
    background: transparent !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    margin: 2px 6px !important;
    border: 1px solid transparent !important;
    display: block !important;
    text-decoration: none !important;
    transition: background 0.2s ease, color 0.2s ease;
}

section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"]:hover {
    color: #ffffff !important;
    background: #21262d !important;
    border-color: #30363d !important;
    box-shadow: 0 0 10px rgba(124, 58, 237, 0.2) !important;
}

section[data-testid="stSidebar"] a[aria-current="page"] {
    color: #ffffff !important;
    background: #7c3aed !important;
    border-color: #9d5cf6 !important;
    box-shadow: 0 0 14px rgba(124, 58, 237, 0.45) !important;
    font-weight: 600 !important;
}

h1, h2, h3 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    letter-spacing: -0.5px !important;
}

p, li, label {
    font-family: 'Inter', sans-serif !important;
    color: #c9d1d9 !important;
}

.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
    border: 1px solid #30363d !important;
    background: transparent !important;
    color: #c9d1d9 !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background: #21262d !important;
    border-color: #7c3aed !important;
    color: #ffffff !important;
}

div[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    color: #ffffff !important;
    font-size: 2rem !important;
    font-weight: 600 !important;
}

div[data-testid="stMetricLabel"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.75rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    color: #8b949e !important;
}

.stTextInput > div > input,
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background-color: #0d1117 !important;
    border: 1px solid #30363d !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    border-radius: 6px !important;
}

.stDataFrame {
    background-color: #1c2128 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
}

.doctor-card {
    transition: all 0.2s ease;
    background: #1c2128;
    border-radius: 12px;
}
.doctor-card:hover {
    border-color: #7c3aed !important;
    box-shadow: 0 0 14px rgba(124, 58, 237, 0.3) !important;
    transform: translateY(-2px) !important;
}

.history-card {
    transition: all 0.2s ease;
    padding: 1rem;
}
.history-card:hover {
    background: #21262d !important;
}

footer { display: none !important; }
#MainMenu { display: none !important; }
header { display: none !important; }
</style>
""", unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown("""
<div style="padding:1.2rem 1rem 0.8rem 1rem;
            border-bottom:1px solid #21262d;
            margin-bottom:0.8rem;">
<span style="font-family:Inter,sans-serif;
             font-size:1.2rem;
             font-weight:700;
             color:#ffffff;
             letter-spacing:-0.3px;">
MediScan AI
</span>
</div>
""", unsafe_allow_html=True)

        st.page_link("app.py", label="Home", width="stretch")
        st.page_link("pages/dashboard.py", label="Dashboard", width="stretch")
        st.page_link("pages/09_prediction.py", label="Prediction", width="stretch")
        st.page_link("pages/10_chatbot.py", label="Chatbot", width="stretch")
        st.page_link("pages/patient_history.py", label="Patient History", width="stretch")
        st.page_link("pages/appointment.py", label="Appointment", width="stretch")
        st.page_link("pages/about.py", label="About", width="stretch")

        st.markdown("""
<div style="position:fixed;bottom:1.5rem;left:0;
            width:240px;padding:0 1.2rem;
            border-top:1px solid #21262d;padding-top:1rem;">
<span style="font-size:1.2rem;color:#8b949e;">☽</span>
</div>
""", unsafe_allow_html=True)

