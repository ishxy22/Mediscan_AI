"""Append prediction rows to ``st.session_state`` for Patient History."""

from __future__ import annotations

from datetime import datetime

import streamlit as st

SESSION_KEY = "prediction_history"


def _ensure() -> None:
    if SESSION_KEY not in st.session_state:
        st.session_state[SESSION_KEY] = []


def log_prediction(
    *,
    symptoms_entered: str,
    predicted_disease: str,
    confidence: float,
) -> None:
    _ensure()
    st.session_state[SESSION_KEY].append(
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "symptoms_entered": symptoms_entered,
            "predicted_disease": predicted_disease,
            "confidence_score": confidence,
        }
    )


def clear_prediction_history() -> None:
    st.session_state[SESSION_KEY] = []
