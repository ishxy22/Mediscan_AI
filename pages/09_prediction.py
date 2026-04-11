from __future__ import annotations
import streamlit as st
from utils.styles import load_styles, render_sidebar

st.set_page_config(
    page_title="MediScan AI - Prediction",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_styles()
render_sidebar()

import html
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import joblib
import pandas as pd

_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(_ROOT))

from utils.display_text import symptom_plain
from utils.prediction_history import log_prediction

_MODEL_DIR = _ROOT / "models"
_DATA_DIR = _ROOT / "data"

# Home remedies dictionary
HOME_REMEDIES = {
    "Malaria": "drink fluids, rest, use mosquito nets",
    "Typhoid": "boiled water, soft foods, rest",
    "Flu": "warm soup, steam inhalation, ginger tea, rest",
    "Fungal infection": "keep dry, loose clothes, maintain hygiene",
    "Diabetes": "reduce sugar, exercise, regular checkups",
    "Hypertension": "reduce salt, exercise, meditation",
    "Migraine": "dark quiet room, cold compress, hydration",
    "Pneumonia": "rest, steam inhalation, warm fluids, doctor visit",
    "Allergy": "avoid triggers, antihistamine, doctor consult",
    "Dengue": "rest, fluids, paracetamol, doctor immediately"
}


@st.cache_resource
def _load_classifier():
    path = _MODEL_DIR / "rf_model.pkl"
    if not path.is_file():
        raise FileNotFoundError("The health check model is not ready yet. Ask your teacher or run the training step.")
    return joblib.load(path)


@st.cache_resource
def _load_symptom_names():
    path = _MODEL_DIR / "symptoms_list.pkl"
    if not path.is_file():
        raise FileNotFoundError("Symptom list not found. Run the training step first.")
    names = joblib.load(path)
    if not isinstance(names, list):
        raise TypeError("Invalid symptom list file.")
    return names


@st.cache_data
def _load_precautions() -> pd.DataFrame:
    path = _DATA_DIR / "symptom_precaution.csv"
    if not path.is_file():
        raise FileNotFoundError("Precautions file not found.")
    df = pd.read_csv(path)
    df["Disease_key"] = df["Disease"].astype(str).str.strip()
    return df


def _precautions_for_disease(disease: str, prec_df: pd.DataFrame) -> list[str]:
    key = str(disease).strip()
    sub = prec_df[prec_df["Disease_key"] == key]
    if sub.empty:
        sub = prec_df[prec_df["Disease_key"].str.lower() == key.lower()]
    if sub.empty:
        return []
    row = sub.iloc[0]
    out: list[str] = []
    for col in ("Precaution_1", "Precaution_2", "Precaution_3", "Precaution_4"):
        if col not in row.index:
            continue
        val = row[col]
        if pd.isna(val):
            continue
        s = str(val).strip()
        if s:
            out.append(s)
    return out[:4]


def _get_risk_level(confidence: float) -> tuple[str, str]:
    """Get risk level text and color based on confidence."""
    if confidence >= 0.70:
        return "High Risk", "#da3633" # red
    elif confidence >= 0.40:
        return "Moderate Risk", "#d29922" # amber
    else:
        return "Low Risk", "#238636" # green

st.markdown('<p class="page-title" style="color: #ffffff;">Check My Symptoms</p>', unsafe_allow_html=True)
st.markdown('<p class="muted-text">Configure symptoms on the left, review in the center, and see the diagnosis on the right.</p>', unsafe_allow_html=True)

try:
    model = _load_classifier()
    symptom_columns = _load_symptom_names()
    precautions_df = _load_precautions()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()
except Exception as e:
    st.error("Something went wrong loading the app. Please try again later.")
    st.stop()

display_symptoms = [s.replace('_', ' ').title() for s in symptom_columns]
symptom_map = {s.replace('_', ' ').title(): s for s in symptom_columns}

# 3-column horizontal flow layout
col1, col_arr1, col2, col_arr2, col3 = st.columns([3, 0.5, 3, 0.5, 4])

with col1:
    st.markdown('<div class="prediction-panel" style="height: 100%; background:#1c2128; border:1px solid #30363d; border-radius:12px; padding:1.5rem;">', unsafe_allow_html=True)
    st.markdown('<h4><span style="color:#7c3aed; font-size: 10px; vertical-align: middle;">⬤</span> Configuration</h4>', unsafe_allow_html=True)
    selected_display = st.multiselect('Select Symptoms', display_symptoms)
    selected = [symptom_map[s] for s in selected_display]
    
    predict_clicked = False
    if st.button("Predict Diagnosis", type="primary", use_container_width=True):
        predict_clicked = True
    st.markdown('</div>', unsafe_allow_html=True)

with col_arr1:
    st.markdown('<div class="flow-arrow">→</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="prediction-panel" style="height: 100%; background:#1c2128; border:1px solid #30363d; border-radius:12px; padding:1.5rem;">', unsafe_allow_html=True)
    st.markdown('<h4>Selected Symptoms</h4>', unsafe_allow_html=True)
    if not selected_display:
        st.markdown('<p class="muted-text">No symptoms selected.</p>', unsafe_allow_html=True)
    else:
        tags_html = ""
        for i, symptom in enumerate(selected_display):
            active_style = "border-color:#ef4444 !important; box-shadow:0 0 8px rgba(239,68,68,0.4) !important;" if i == len(selected_display) - 1 else ""
            tags_html += f'<span class="tag-chip" style="background:#21262d; border:1px solid #30363d; border-radius:6px; padding:4px 12px; font-family:\'JetBrains Mono\', monospace; display:inline-block; margin:4px; {active_style}">{symptom}</span> '
        st.markdown(tags_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_arr2:
    st.markdown('<div class="flow-arrow">→</div>', unsafe_allow_html=True)

with col3:
    if predict_clicked:
        if not selected:
            st.warning("Please choose at least one symptom first.")
        else:
            selected_set = set(selected)
            row = [1 if name in selected_set else 0 for name in symptom_columns]
            X = pd.DataFrame([row], columns=symptom_columns)
            proba = model.predict_proba(X)[0]
            classes = model.classes_
            
            top_idx = proba.argsort()[-1]
            disease = str(classes[top_idx])
            confidence = float(proba[top_idx])
            risk_level, risk_color = _get_risk_level(confidence)
            precautions = _precautions_for_disease(disease, precautions_df)
            remedies = HOME_REMEDIES.get(disease, "Consult a doctor for personalized advice")
            
            # Draw result using native and minimal HTML to avoid text-rendering bugs
            st.markdown('<div class="prediction-panel active-result" style="height: 100%; background:#1c2128; border:1px solid #ef4444; box-shadow:0 0 20px rgba(239,68,68,0.25); border-radius:12px; padding:1.5rem;">', unsafe_allow_html=True)
            
            st.markdown('<h4 style="color: #8b949e; margin-bottom: 0;">Diagnosis Result</h4>', unsafe_allow_html=True)
            st.markdown(f'<div class="mono-text" style="font-size: 2.25rem; font-family: \'Inter\', sans-serif !important; color: #ffffff; font-weight: 700; margin: 0.5rem 0;">{disease}</div>', unsafe_allow_html=True)
            
            c1, c2 = st.columns([1, 1])
            with c1:
                st.markdown('<span class="muted-text">Confidence:</span>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<span class="mono-text" style="color: {risk_color}; font-weight: bold; font-size: 1.2rem; float: right;">{confidence:.0%}</span>', unsafe_allow_html=True)
            
            # Styled progress bar via HTML strictly on one line
            st.markdown(f'<div style="background-color: #30363d; border-radius: 4px; height: 8px; width: 100%; margin-bottom: 1.5rem;"><div style="background-color: {risk_color}; height: 100%; border-radius: 4px; width: {confidence*100}%;"></div></div>', unsafe_allow_html=True)
            
            # Risk Level Badge
            st.markdown(f'<div style="background: {risk_color}22; color: {risk_color}; border: 1px solid {risk_color}; padding: 0.25rem 0.75rem; border-radius: 20px; display: inline-block; margin-bottom: 1.2rem; font-weight: 600; font-size: 0.9rem;">{risk_level}</div>', unsafe_allow_html=True)
            
            st.markdown('**Precautions:**')
            prec_list = "".join([f"<li>{p}</li>" for p in precautions[:3]])
            st.markdown(f'<ul class="muted-text" style="margin-top: 0.2rem; margin-bottom: 1.2rem; padding-left: 1.2rem;">{prec_list}</ul>', unsafe_allow_html=True)
            
            st.markdown('**Home Remedies:**')
            st.markdown(f'<p class="muted-text" style="margin-top: 0.2rem;">{remedies}</p>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Log prediction
            symptoms_plain = ", ".join(symptom_plain(s) for s in selected)
            log_prediction(
                symptoms_entered=symptoms_plain,
                predicted_disease=disease,
                confidence=confidence,
            )
            
            # Save to session state
            if 'history' not in st.session_state:
                st.session_state['history'] = []
            st.session_state['history'].append({
                'timestamp': datetime.now().strftime('%d %b %Y, %I:%M %p'),
                'symptoms': selected_display,
                'disease': disease,
                'confidence': round(confidence * 100, 1)
            })
    else:
        st.markdown('<div class="prediction-panel" style="height: 100%; display: flex; align-items: center; justify-content: center; background:#1c2128; border:1px dashed #30363d; border-radius:12px; padding:1.5rem;">', unsafe_allow_html=True)
        st.markdown('<p class="muted-text">Waiting for input...</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<p class="muted-text" style="font-size: 0.875rem; margin-top: 2rem;">This is not medical advice. Always consult a qualified doctor.</p>', unsafe_allow_html=True)
