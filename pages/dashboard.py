from __future__ import annotations

import csv
import io
import random
from collections import Counter
from datetime import datetime
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.styles import load_styles, render_sidebar

st.set_page_config(
    page_title="EDA Dashboard - Health Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_styles()
render_sidebar()


# Health tips database
HEALTH_TIPS = [
    "Drink at least 8 glasses of water daily to stay hydrated and maintain optimal body function.",
    "Aim for 7-9 hours of quality sleep each night to support immune system and mental health.",
    "Include 5 servings of fruits and vegetables in your daily diet for essential nutrients.",
    "Exercise for at least 30 minutes daily to maintain cardiovascular health and manage weight.",
    "Practice stress management techniques like meditation or deep breathing for mental wellness.",
    "Wash your hands frequently with soap for at least 20 seconds to prevent infections.",
    "Limit processed foods and added sugars to reduce inflammation and maintain healthy weight.",
    "Get regular health checkups even when you feel fine to catch potential issues early.",
    "Maintain good posture while sitting and working to prevent back and neck pain.",
    "Avoid smoking and limit alcohol consumption for better overall health and longevity."
]


def _get_risk_color(confidence: float) -> str:
    """Get risk color based on confidence percentage."""
    if confidence >= 0.70:
        return "#ef4444"  # Red for high risk
    elif confidence >= 0.40:
        return "#d29922"  # Orange for moderate risk
    else:
        return "#238636"  # Green for low risk


def _get_most_common_symptom(history: list) -> str:
    """Find most common symptom from all history entries using Counter."""
    if not history:
        return "None"
    
    all_symptoms = []
    for entry in history:
        symptoms = entry.get("symptoms", [])
        if isinstance(symptoms, list):
            all_symptoms.extend([s.strip().lower() for s in symptoms if s.strip()])
        elif isinstance(symptoms, str):
            symptoms_list = symptoms.split(", ")
            all_symptoms.extend([s.strip().lower() for s in symptoms_list if s.strip()])
    
    if not all_symptoms:
        return "None"
    
    # Use Counter to find most common
    symptom_counts = Counter(all_symptoms)
    most_common = symptom_counts.most_common(1)[0][0]
    return most_common.title()


def _calculate_profile_completion() -> float:
    """Calculate profile completion percentage."""
    profile = st.session_state.get("profile", {})
    
    fields = ["name", "age", "gender", "blood_group", "allergies"]
    completed = 0
    
    for field in fields:
        if profile.get(field):
            completed += 1
    
    return (completed / len(fields)) * 100

# Initialize session state
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'profile' not in st.session_state:
    st.session_state['profile'] = {}

# Header with title and reset button
head_col1, head_col2 = st.columns([4, 1])
with head_col1:
    st.markdown('<p class="page-title" style="color: #ffffff;">EDA Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="muted-text">Your personal health overview and insights.</p>', unsafe_allow_html=True)
with head_col2:
    if st.session_state.get('history'):
        st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
        if st.button("Reset Dashboard", use_container_width=True, type="secondary"):
            clear_prediction_history()
            st.session_state.history = []
            st.success("All prediction history cleared!")
            st.rerun()

history = st.session_state.get('history', [])

# Row 1: Metric Cards
st.markdown('<div class="section-title">Health Overview</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_checks = len(history)
    st.markdown(f"""
    <div class="metric-card" style="padding: 1.5rem; text-align: center;">
        <div class="metric-number" style="font-size: 2.2rem; color: #ffffff; font-weight: bold;">{total_checks}</div>
        <div style="font-family: 'Inter', sans-serif; color: #8b949e; font-size: 0.9rem; font-weight: 500; text-transform: uppercase;">Total Checks</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    most_common = _get_most_common_symptom(history)
    st.markdown(f"""
    <div class="metric-card" style="padding: 1.5rem; text-align: center;">
        <div class="metric-number" style="font-size: 1.5rem; color: #ffffff; font-weight: bold; min-height: 2.6rem; display: flex; align-items: center; justify-content: center;">{most_common}</div>
        <div style="font-family: 'Inter', sans-serif; color: #8b949e; font-size: 0.9rem; font-weight: 500; text-transform: uppercase;">Common Symptom</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    last_disease = history[-1]['disease'] if history else 'None'
    st.markdown(f"""
    <div class="metric-card" style="padding: 1.5rem; text-align: center;">
        <div class="metric-number" style="font-size: 1.5rem; color: #ffffff; font-weight: bold; min-height: 2.6rem; display: flex; align-items: center; justify-content: center;">{last_disease}</div>
        <div style="font-family: 'Inter', sans-serif; color: #8b949e; font-size: 0.9rem; font-weight: 500; text-transform: uppercase;">Last Disease</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    completion = _calculate_profile_completion()
    st.markdown(f"""
    <div class="metric-card" style="padding: 1.5rem; text-align: center;">
        <div class="metric-number" style="font-size: 2.2rem; color: #ffffff; font-weight: bold;">{completion:.0f}%</div>
        <div style="font-family: 'Inter', sans-serif; color: #8b949e; font-size: 0.9rem; font-weight: 500; text-transform: uppercase;">Profile Complete</div>
    </div>
    """, unsafe_allow_html=True)

# Row 2: 2 Charts side by side
st.markdown('<div class="section-title" style="margin-top: 2rem;">Analysis Charts</div>', unsafe_allow_html=True)
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown('<div class="result-card" style="background:#1c2128; border:1px solid #30363d; border-radius:12px; padding:1rem;">', unsafe_allow_html=True)
    st.markdown('<h4 style="margin-top:0;">Confidence Trend</h4>', unsafe_allow_html=True)
    if history:
        conf_data = [item['confidence'] for item in history]
        st.line_chart(conf_data, height=250, use_container_width=True)
    else:
        st.info("No data to display.")
    st.markdown('</div>', unsafe_allow_html=True)

with chart_col2:
    st.markdown('<div class="result-card" style="background:#1c2128; border:1px solid #30363d; border-radius:12px; padding:1rem;">', unsafe_allow_html=True)
    st.markdown('<h4 style="margin-top:0;">Diseases Predicted</h4>', unsafe_allow_html=True)
    if history:
        disease_counts = Counter([item['disease'] for item in history])
        st.bar_chart(pd.DataFrame.from_dict(disease_counts, orient='index'), height=250, use_container_width=True)
    else:
        st.info("No data to display.")
    st.markdown('</div>', unsafe_allow_html=True)

# Row 3: Full-width chart (Timeline of Symptoms Count)
st.markdown('<div class="result-card" style="margin-top: 1rem; background:#1c2128; border:1px solid #30363d; border-radius:12px; padding:1rem;">', unsafe_allow_html=True)
st.markdown('<h4 style="margin-top:0;">Symptoms per Check Over Time</h4>', unsafe_allow_html=True)
if history:
    symptom_counts = [len(item.get('symptoms', [])) for item in history]
    st.area_chart(symptom_counts, height=200, use_container_width=True)
else:
    st.info("No data to display.")
st.markdown('</div>', unsafe_allow_html=True)


# Row 4: Health Profile Form
st.markdown('<div class="section-title" style="margin-top: 2rem;">Health Profile</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div style="background:#1c2128; border:1px solid #30363d; border-radius:12px; padding:1.5rem;">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input(
            "Full Name", 
            value=st.session_state.profile.get("name", ""),
            placeholder="Enter your full name"
        )
        age = st.number_input(
            "Age", 
            min_value=1, 
            max_value=120, 
            value=int(st.session_state.profile.get("age", 25))
        )
    
    with col2:
        gender = st.selectbox(
            "Gender",
            options=["Select", "Male", "Female", "Other"],
            index=["Select", "Male", "Female", "Other"].index(
                st.session_state.profile.get("gender", "Select")
            )
        )
        
        blood_group = st.selectbox(
            "Blood Group",
            options=["Select", "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"],
            index=["Select", "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"].index(
                st.session_state.profile.get("blood_group", "Select")
            )
        )
    
    allergies = st.text_input(
        "Known Allergies",
        value=st.session_state.profile.get("allergies", ""),
        placeholder="e.g., Penicillin, Peanuts, Dust"
    )
    
    if st.button("Save Profile", type="primary", use_container_width=True):
        if name and age and gender not in ["Select"] and blood_group not in ["Select"]:
            st.session_state.profile = {
                "name": name,
                "age": age,
                "gender": gender,
                "blood_group": blood_group,
                "allergies": allergies
            }
            st.success("Profile saved successfully!")
            st.rerun()
        else:
            st.error("Please fill in all required fields (Name, Age, Gender, Blood Group)")
    
    st.markdown('</div>', unsafe_allow_html=True)


# Row 5: Health Tip of the Day
st.markdown('<div class="section-title" style="margin-top: 2rem;">Health Tip of the Day</div>', unsafe_allow_html=True)

today = datetime.now().day
tip_index = today % len(HEALTH_TIPS)
daily_tip = HEALTH_TIPS[tip_index]

st.markdown(f"""
<div style="background:#1c2128; border-left:3px solid #7c3aed; border-radius:0 12px 12px 0; padding:1rem 1.5rem;">
    <div style="font-size: 1.1rem; line-height: 1.6; color: #ffffff;">
        {daily_tip}
    </div>
</div>
""", unsafe_allow_html=True)

# Row 6: Download Report
st.markdown('<div class="section-title" style="margin-top: 2rem;">Download Report</div>', unsafe_allow_html=True)

if len(st.session_state['history']) > 0:
    df = pd.DataFrame(st.session_state['history'])
    csv_data = df.to_csv(index=False)
    st.download_button(
        label='Download Health Report',
        data=csv_data,
        file_name='health_report.csv',
        mime='text/csv'
    )
else:
    st.info('No data to download yet.')
