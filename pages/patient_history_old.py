from __future__ import annotations

import html
import io

import pandas as pd
import streamlit as st
st.set_page_config(page_title="MediScan AI", layout="wide")
st.switch_page("pages/patient_history.py")


from utils.prediction_history import SESSION_KEY, clear_prediction_history
from utils.styles import get_medical_dashboard_css

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background-color: #F0F4F8; }
h1, h2, h3 { color: #2D3748; font-weight: 700; }
p, li { color: #4A5568; }
.stButton > button {
    border-radius: 10px;
    padding: 10px 24px;
    font-weight: 600;
    width: 100%;
}
section[data-testid="stSidebar"] { background: #1E2A3A; }
section[data-testid="stSidebar"] * { color: #E2E8F0 !important; }
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="My Health History - Health Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(get_medical_dashboard_css(), unsafe_allow_html=True)
st.markdown('<p class="page-title">My Health History</p>', unsafe_allow_html=True)
st.markdown("Here is what you have checked **during this visit** in your browser.")

if 'history' not in st.session_state:
    st.session_state['history'] = []

rows: list[dict] = st.session_state['history']

if not rows:
    st.info("No health checks yet. Go to Check My Symptoms to get started.")
else:
    st.markdown('<div class="section-header">Your checks today</div>', unsafe_allow_html=True)
    for entry in reversed(st.session_state['history']):
        timestamp = entry.get('timestamp', '—')
        symptoms = entry.get('symptoms', [])
        disease = entry.get('disease', '—')
        confidence = entry.get('confidence', 0)
        
        # Format symptoms with spaces instead of underscores
        if isinstance(symptoms, list):
            symptoms_str = ', '.join([s.replace('_', ' ').title() for s in symptoms])
        else:
            symptoms_str = str(symptoms).replace('_', ' ').title()
        
        conf_txt = f"{confidence:.0%}" if confidence else "—"
        
        st.markdown(f"""
        <div class="history-card">
            <p style="margin:0;color:#718096;font-size:0.95rem;">{timestamp}</p>
            <p style="margin:0.4rem 0 0 0;"><strong>You mentioned:</strong> {symptoms_str}</p>
            <p style="margin:0.4rem 0 0 0;"><strong>Result shown:</strong> <strong style="color: #2D3748;">{disease}</strong> ({conf_txt} match strength)</p>
        </div>
        """, unsafe_allow_html=True)

col_a, col_b = st.columns(2)
with col_a:
    if st.button("Clear history", type="secondary"):
        clear_prediction_history()
        st.rerun()

export_df = pd.DataFrame(rows)
if export_df.empty:
    export_df = pd.DataFrame(
        columns=[
            "timestamp",
            "symptoms_entered",
            "predicted_disease",
            "confidence_score",
        ]
    )

buf = io.StringIO()
export_df.to_csv(buf, index=False)
csv_bytes = buf.getvalue().encode("utf-8")

with col_b:
    st.download_button(
        label="Download report",
        data=csv_bytes,
        file_name="my_health_report.csv",
        mime="text/csv",
        type="primary",
    )

st.caption("History clears when you close the tab or press Clear history. This app does not save your data on a server.")
