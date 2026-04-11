from __future__ import annotations

import re
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st
st.set_page_config(page_title="MediScan AI", layout="wide")
st.switch_page("pages/10_chatbot.py")


from utils.display_text import symptom_plain
from utils.prediction_history import log_prediction
from utils.styles import get_medical_dashboard_css

_ROOT = Path(__file__).resolve().parent.parent
_MODEL_DIR = _ROOT / "models"
_DATA_DIR = _ROOT / "data"

OPENING_MESSAGE = (
    "Hi! Tell me how you are feeling and I will try to help. "
    "For example: I have fever and headache since 2 days."
)
DISCLAIMER = "Remember: This is not medical advice. Please consult a doctor."


@st.cache_resource
def _load_classifier():
    path = _MODEL_DIR / "rf_model.pkl"
    if not path.is_file():
        raise FileNotFoundError("The health check model is not ready yet.")
    return joblib.load(path)


@st.cache_resource
def _load_symptom_names():
    path = _MODEL_DIR / "symptoms_list.pkl"
    if not path.is_file():
        raise FileNotFoundError("Symptom list not found.")
    names = joblib.load(path)
    if not isinstance(names, list):
        raise TypeError("Invalid symptom list.")
    return names


@st.cache_data(show_spinner=False)
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
    return out


def _normalize_message(text: str) -> tuple[str, set[str]]:
    """Lowercase text; treat underscores like spaces so 'skin_rash' and 'skin rash' match."""
    t = text.lower().replace("_", " ")
    blob = " " + re.sub(r"[^a-z0-9]+", " ", t) + " "
    blob = re.sub(r"\s+", " ", blob)
    words = {w for w in blob.split() if w}
    return blob, words


_AMBIGUOUS_LAST = frozenset({"pain", "ache", "skin"})

_COLLOQUIAL_SYMPTOM_MAP: tuple[tuple[str, str], ...] = (
    ("feverish", "high_fever"),
    ("fever", "high_fever"),
    ("cold feet", "chills"),
    ("tired", "fatigue"),
    ("headache", "headache"),
    ("stomach pain", "stomach_pain"),
    ("vomiting", "vomiting"),
    ("cold", "chills"),
    ("cough", "cough"),
    ("body ache", "muscle_wasting"),
)


def _colloquial_map_application_order() -> list[tuple[str, str]]:
    phrases = [(p, c) for p, c in _COLLOQUIAL_SYMPTOM_MAP if " " in p]
    words = [(p, c) for p, c in _COLLOQUIAL_SYMPTOM_MAP if " " not in p]
    phrases.sort(key=lambda x: -len(x[0]))
    words.sort(key=lambda x: -len(x[0]))
    return phrases + words


def _apply_colloquial_symptom_map(text: str) -> tuple[str, list[str]]:
    t = re.sub(r"\s+", " ", text.lower().strip().replace("_", " "))
    canonical_hits: list[str] = []
    for phrase, canon in _colloquial_map_application_order():
        pat = re.compile(r"\b" + re.escape(phrase) + r"\b", re.IGNORECASE)
        if pat.search(t):
            canonical_hits.append(canon)
            t = pat.sub(canon.replace("_", " "), t)
    return t, list(dict.fromkeys(canonical_hits))


def _match_symptoms_against_vocab(text: str, symptoms_list: list[str]) -> list[str]:
    """Match using spaced phrases (underscores in data names become spaces for compare)."""
    blob, words = _normalize_message(text)
    hits: list[str] = []
    padded = f" {blob.strip()} "

    for s in symptoms_list:
        phrase_spaced = s.replace("_", " ").lower().strip()
        parts = [p for p in phrase_spaced.split() if p]
        if not parts:
            continue

        phrase_in_text = f" {phrase_spaced} " in padded
        all_tokens_present = all(p in words for p in parts)

        if phrase_in_text or all_tokens_present:
            hits.append(s)
            continue

        if len(parts) == 1:
            p = parts[0]
            if len(p) >= 3 and p in words:
                hits.append(s)
            continue

        matched = [p for p in parts if p in words]
        if len(matched) >= 2:
            hits.append(s)
        elif len(matched) == 1:
            p = matched[0]
            if p == parts[-1] and p not in _AMBIGUOUS_LAST:
                hits.append(s)

    return list(dict.fromkeys(hits))


def extract_symptoms_from_text(text: str, symptoms_list: list[str]) -> list[str]:
    augmented, from_map = _apply_colloquial_symptom_map(text)
    vocab_ok = set(symptoms_list)
    from_map = [c for c in from_map if c in vocab_ok]
    from_heuristic = _match_symptoms_against_vocab(augmented, symptoms_list)

    merged: list[str] = []
    for c in from_map:
        if c not in merged:
            merged.append(c)
    for h in from_heuristic:
        if h not in merged:
            merged.append(h)
    return merged


def _plain_symptom_list(symptoms: list[str]) -> str:
    return ", ".join(symptom_plain(s) for s in symptoms)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background-color: #F0F4F8; }
h1, h2, h3 { color: #2D3748; font-weight: 700; }
p { color: #4A5568; }
div[data-testid="stChatMessage"] {
    background: white;
    border-radius: 12px;
    padding: 12px 16px;
    margin: 6px 0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    color: #2D3748;
}
div[data-testid="stChatInput"] > div {
    background: white;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
}
.stButton > button {
    background: white;
    color: #E53E3E;
    border: 1px solid #E53E3E;
    border-radius: 10px;
    padding: 10px 24px;
    font-weight: 600;
    width: 100%;
}
.stButton > button:hover {
    background: #FFF5F5;
}
section[data-testid="stSidebar"] { background: #1E2A3A; }
section[data-testid="stSidebar"] * { color: #E2E8F0 !important; }
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Friendly Health Chat - Health Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(get_medical_dashboard_css(), unsafe_allow_html=True)
st.markdown('<p class="page-title">Friendly health chat</p>', unsafe_allow_html=True)
st.markdown("<p class='card-description'>Write in your own words. I will listen and give gentle suggestions — not a diagnosis.</p>", unsafe_allow_html=True)

try:
    model = _load_classifier()
    symptom_columns = _load_symptom_names()
    precautions_df = _load_precautions()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()
except Exception:
    st.error("Something went wrong. Please try again later.")
    st.stop()

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [{"role": "assistant", "content": OPENING_MESSAGE}]

if st.sidebar.button("Start fresh chat"):
    st.session_state.chat_messages = [{"role": "assistant", "content": OPENING_MESSAGE}]
    st.rerun()

for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type how you feel…"):
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    detected = extract_symptoms_from_text(prompt, symptom_columns)
    n_matched = len(detected)
    plain_syms = _plain_symptom_list(detected)

    if n_matched < 2:
        response = (
            "I could not identify specific symptoms from what you described. Please try to be more specific. "
            "For example: I have had fever and headache for 2 days. Or use the Check My Symptoms page for more accurate results."
        )
    else:
        row = [1 if name in set(detected) else 0 for name in symptom_columns]
        X = pd.DataFrame([row], columns=symptom_columns)
        proba = model.predict_proba(X)[0]
        idx = int(proba.argmax())
        disease = str(model.classes_[idx])
        confidence = float(proba[idx])

        if confidence < 0.40:
            response = (
                f"I noticed these symptoms: **{plain_syms}**.\n\n"
                "I could not find a clear match. Please describe your symptoms in more detail "
                "or try **Check My Symptoms** in the menu instead.\n\n"
                f"{DISCLAIMER}"
            )
        else:
            tips = _precautions_for_disease(disease, precautions_df)
            tip_block = ""
            if tips:
                tip_block = "\n".join(f"- {t}" for t in tips[:4])
            else:
                tip_block = "- A health professional can give you the best next steps."

            response = (
                f"I noticed these symptoms: **{plain_syms}**.\n\n"
                f"From what you shared, **{disease}** is one thing people sometimes look into when they feel this way. "
                f"I am about **{confidence:.0%}** sure this fits the patterns in our simple reference — "
                "that is not the same as being sure about your body.\n\n"
                "**Ideas from our reference list (not personal medical advice):**\n"
                f"{tip_block}\n\n"
                f"{DISCLAIMER}"
            )
            log_prediction(
                symptoms_entered=plain_syms,
                predicted_disease=disease,
                confidence=confidence,
            )

    st.session_state.chat_messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
