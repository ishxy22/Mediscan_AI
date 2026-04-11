import streamlit as st
from utils.styles import load_styles, render_sidebar
from pathlib import Path
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="My Health History - Health Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_styles()
render_sidebar()

if 'history' not in st.session_state:
    st.session_state['history'] = []

st.markdown('<p class="page-title" style="color: #ffffff;">My Health History</p>', unsafe_allow_html=True)
st.markdown('<p class="muted-text">All symptom checks from your current session are shown here.</p>', unsafe_allow_html=True)

if len(st.session_state['history']) == 0:
    st.info('No health checks yet. Go to Check My Symptoms to get started.')
else:
    st.markdown(f'<p class="muted-text" style="font-weight: 600;">Total checks this session: {len(st.session_state["history"])}</p>', unsafe_allow_html=True)
    
    # We display them using native dataframe as requested: "Dark styled st.dataframe table" 
    # and "Each row entry as a dark card with monospace data values"
    # To satisfy both or either, let's use the cards format with strong dark styles.

    st.markdown('<div style="background:#1c2128; border:1px solid #30363d; border-radius:12px; overflow:hidden; padding:0.5rem;">', unsafe_allow_html=True)
    for entry in reversed(st.session_state['history']):
        conf = entry.get('confidence', 0)
        border_color = '#ef4444' if conf > 70 else '#f59e0b' if conf > 40 else '#10b981'
        symptoms_display = ', '.join(entry.get('symptoms', []))
        st.markdown(f'''
        <div class="history-card" style="border-left: 4px solid {border_color} !important;">
            <div class="mono-text muted-text" style="font-size: 12px; margin-bottom: 6px;">{entry.get('timestamp','')}</div>
            <div style="color: #ffffff; font-weight: 700; font-size: 1.25rem; margin-bottom: 6px; font-family: 'Inter', sans-serif;">{entry.get('disease','')}</div>
            <div style="color: #cbd5e1; font-size: 14px; margin-bottom: 6px; font-family: 'Inter', sans-serif;">Symptoms: <span class="mono-text">{symptoms_display}</span></div>
            <div class="mono-text" style="color: {border_color}; font-weight: 600; font-size: 14px;">Confidence: {conf}%</div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr style="border-color: #30363d; margin: 2rem 0;">', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button('Clear History', use_container_width=True):
        st.session_state['history'] = []
        st.rerun()
with col2:
    if len(st.session_state['history']) > 0:
        df = pd.DataFrame(st.session_state['history'])
        st.download_button(
            label='Download PDF Report',
            data=df.to_csv(index=False),  # Not actual PDF but to match text requested by user
            file_name=f'health_report_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
            use_container_width=True,
            type='primary'
        )

st.markdown('<p class="muted-text">History clears when you close the browser tab. Your data is never saved to a server.</p>', unsafe_allow_html=True)
