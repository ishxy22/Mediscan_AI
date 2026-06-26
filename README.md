# MediScan AI 🏥🤖

MediScan AI is an interactive, multi-page healthcare application built with Streamlit that leverages Machine Learning to predict potential diseases based on user-reported symptoms. It features an intelligent symptom analysis dashboard, automated precaution lookups, dynamic patient history management, a conversational AI health assistant, and clinic workflow tracking (appointments and analytics dashboards).

## 🚀 Key Features

* **Symptom-Based Disease Prediction (ML Engine):** Utilizes a Random Forest classifier trained on a structured dataset to evaluate binary vector representations of user-selected symptoms and deliver immediate predictive assessments.
* **Smart Health Analytics & Dashboard:** Dynamically parses logged records to display metrics, chart real-time clinical workflows, track disease trends via frequency counters, and output operational insights.
* **Conversational AI Chatbot:** Integrates an in-app health assistant to resolve medical queries, suggest generic guidance, and enhance patient engagement.
* **Automated Precaution & Severity Lookup:** Cross-references mapped predictions against backend database dictionaries to offer localized severity indicators and step-by-step health precautions.
* **Clinic Workflow Suite:** Incorporates specialized portals for booking mockup appointments and exploring comprehensive medical history logs across patient life cycles.

---

## 🛠️ Tech Stack & Libraries

* **Frontend Framework:** `Streamlit` (Multi-page stateful web architecture, fully customized using custom CSS pipelines)
* **Data Processing & Analytics:** `Pandas`, `Numpy`
* **Machine Learning & Persistence:** `Scikit-Learn` (Random Forest Classifier), `Joblib`
* **File Operations & Database Mocking:** `CSV`, `IO`, `Pathlib`

---

## 📂 Repository Architecture

```text
├── app.py                     # Application Entry Point & Configurator
├── requirements.txt           # Explicit Direct Dependency Manifest
├── assets/
│   └── style.css              # Custom Global CSS Theme & Branding Rules
├── data/
│   ├── dataset.csv            # Raw Machine Learning Training Matrix
│   ├── symptom_Description.csv# Disease Descriptions Lookup Database
│   ├── symptom_precaution.csv # Clinical Precaution Actions Database
│   └── symptom_severity.csv   # Individual Symptom Severity Weights Database
├── models/
│   ├── train.py               # Asynchronous Model Training & Vectorization Pipeline
│   ├── rf_model.pkl           # Persisted Trained Random Forest Weights
│   └── symptoms_list.pkl      # Pickled Array Vocabulary of Tokenized Symptoms
├── pages/
│   ├── home.py                # Dashboard Landing Hub & Quick Navigation
│   ├── about.py               # Clinic Background & Core Mission Profile
│   ├── appointment.py         # Mockup Appointment Scheduling Core
│   ├── dashboard.py           # Medical Analytics Engine & Charting Center
│   ├── patient_history.py     # Stateful Logs & Historical Case Tracking Records
│   ├── 09_prediction.py       # Core ML Vectorizer & Inference Predictor Page
│   └── 10_chatbot.py          # Conversational Health Assistant Portal
└── utils/
    ├── display_text.py        # String Parsing & Text-Formatting Utilities
    ├── prediction_history.py  # I/O System Helpers for Logging Patient Transactions
    └── styles.py              # Modular CSS Injector & Shared Sidebar Renderers

