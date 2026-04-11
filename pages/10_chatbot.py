import streamlit as st
import joblib
import numpy as np
from pathlib import Path
from utils.styles import load_styles, render_sidebar

st.set_page_config(
    page_title="AI Assistant - Health Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_styles()
render_sidebar()

import os
from datetime import datetime
from pathlib import Path

# Load model and data
ROOT = Path(__file__).resolve().parent.parent
model = joblib.load(ROOT / 'models' / 'rf_model.pkl')
symptom_columns = joblib.load(ROOT / 'models' / 'symptoms_list.pkl')

# Symptom mapping dictionary
SYMPTOM_MAP = {
    'fever': 'high_fever', 'feverish': 'high_fever', 'temperature': 'high_fever',
    'cold': 'chills', 'chills': 'chills', 'shivering': 'chills',
    'headache': 'headache', 'head pain': 'headache', 'head ache': 'headache',
    'cough': 'cough', 'coughing': 'cough',
    'tired': 'fatigue', 'fatigue': 'fatigue', 'weakness': 'fatigue', 'weak': 'fatigue',
    'vomit': 'vomiting', 'vomiting': 'vomiting', 'nausea': 'vomiting',
    'stomach': 'stomach_pain', 'abdomen': 'stomach_pain', 'belly': 'stomach_pain',
    'body ache': 'muscle_wasting', 'muscle pain': 'muscle_wasting',
    'rash': 'skin_rash', 'itching': 'skin_rash', 'skin rash': 'skin_rash',
    'breathless': 'breathlessness', 'breathing': 'breathlessness',
    'diarrhea': 'diarrhoea', 'loose motion': 'diarrhoea',
    'yellow': 'yellowing_of_skin', 'jaundice': 'yellowing_of_skin',
    'joint pain': 'joint_pain', 'chest pain': 'chest_pain',
    'back pain': 'back_pain', 'appetite': 'loss_of_appetite',
    'weight loss': 'weight_loss', 'sweating': 'sweating', 'dizzy': 'dizziness'
}

def extract_symptoms(text):
    text = text.lower()
    matched = []
    for word, symptom in SYMPTOM_MAP.items():
        if word in text and symptom in symptom_columns:
            matched.append(symptom)
    return list(set(matched))

st.markdown('<p class="page-title" style="color: #ffffff;">AI Assistant</p>', unsafe_allow_html=True)
st.markdown("<p class='card-description'>Write in your own words. I will listen and give gentle suggestions — not a diagnosis.</p>", unsafe_allow_html=True)

# Initialize chat messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm here to help you understand your symptoms better. Please describe how you're feeling in your own words."}
    ]

# Get user input FIRST
user_input = st.chat_input("Type how you feel...")

# Process input immediately if received
if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Extract symptoms and generate reply
    matched = extract_symptoms(user_input)
    
    if len(matched) < 2:
        reply = 'I could not identify enough symptoms from what you described. Please be more specific. For example: I have had fever and headache for 2 days. Or use the Check My Symptoms page for better results.'
    else:
        row = [1 if s in matched else 0 for s in symptom_columns]
        import pandas as pd
        X = pd.DataFrame([row], columns=symptom_columns)
        proba = model.predict_proba(X)[0]
        top_idx = proba.argsort()[-1]
        disease = model.classes_[top_idx]
        confidence = round(float(proba[top_idx]) * 100, 1)
        risk = 'High Risk' if confidence > 70 else 'Moderate Risk' if confidence > 40 else 'Low Risk'
        reply = f'Based on what you described, here is what I found.<br><br><span style="color: #8b949e;">Most likely condition:</span> <b style="color: white; font-family: \'Inter\', sans-serif;">{disease}</b><br><span style="color: #8b949e;">Confidence:</span> <span class="mono-text" style="color: #e6edf3;">{confidence}%</span><br><span style="color: #8b949e;">Risk Level:</span> <span style="font-weight: 600;">{risk}</span><br><br><span style="color: #8b949e;">Symptoms I detected:</span> <span class="mono-text" style="color: #e6edf3;">{", ".join([s.replace("_", " ").title() for s in matched])}</span><br><br><div style="border-left: 3px solid #7c3aed; padding-left: 12px; margin-top: 12px; color: #8b949e;">This is not medical advice. Please consult a doctor.</div>'
        
        # Save to session state history
        if 'history' not in st.session_state:
            st.session_state['history'] = []
        st.session_state['history'].append({
            'timestamp': datetime.now().strftime('%d %b %Y, %I:%M %p'),
            'symptoms': [s.replace('_', ' ').title() for s in matched],
            'disease': disease,
            'confidence': confidence
        })

    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})

# Chat container
st.markdown('<div style="background:#0d1117; border:1px solid #21262d; border-radius:12px; padding:1rem; min-height:400px; margin-bottom:1rem;">', unsafe_allow_html=True)
chat_wrapper = st.container()
with chat_wrapper:
    # Display chat messages with custom HTML
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div style="background:#7c3aed; color:#fff; border-radius:18px 18px 4px 18px; padding:0.75rem 1rem; max-width:70%; margin-left:auto; font-family:\'Inter\', sans-serif; margin-bottom: 0.8rem;">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div style="display: flex; align-items: start; gap: 12px; margin-bottom: 0.8rem; max-width: 80%;">
                <div style="background:#7c3aed; color:#fff; width:32px; height:32px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:0.75rem; font-weight:600; font-family:\'Inter\', sans-serif; flex-shrink: 0;">AI</div>
                <div style="background:#1c2128; border:1px solid #30363d; border-radius:18px 18px 18px 4px; padding:0.75rem 1rem; color:#c9d1d9; font-family:\'Inter\', sans-serif; max-width: 100%;">{message["content"]}</div>
            </div>
            ''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Clear chat button
st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
if st.button("Clear Chat"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm here to help you understand your symptoms better. Please describe how you're feeling in your own words."}
    ]
    st.rerun()
