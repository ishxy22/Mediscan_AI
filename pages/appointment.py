from __future__ import annotations

import streamlit as st
from utils.styles import load_styles, render_sidebar
import random

st.set_page_config(
    page_title="Book Appointment - Health Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_styles()
render_sidebar()

from datetime import datetime, timedelta
from pathlib import Path

# Doctor database
DOCTORS_DB = {
    "General Physician": [
        {
            "name": "Dr. Sarah Johnson",
            "qualification": "MBBS, MD (General Medicine)",
            "experience": "12 years",
            "rating": 4.8,
            "fee": 500
        },
        {
            "name": "Dr. Michael Chen", 
            "qualification": "MBBS, DNB (Family Medicine)",
            "experience": "8 years",
            "rating": 4.6,
            "fee": 450
        },
        {
            "name": "Dr. Emily Williams",
            "qualification": "MBBS, MRCP (UK)",
            "experience": "15 years", 
            "rating": 4.9,
            "fee": 600
        }
    ],
    "Dermatologist": [
        {
            "name": "Dr. Lisa Anderson",
            "qualification": "MBBS, MD (Dermatology)",
            "experience": "10 years",
            "rating": 4.7,
            "fee": 800
        },
        {
            "name": "Dr. Robert Martinez",
            "qualification": "MBBS, DVD (Dermatology)",
            "experience": "7 years",
            "rating": 4.5,
            "fee": 700
        }
    ],
    "Cardiologist": [
        {
            "name": "Dr. James Wilson",
            "qualification": "MBBS, MD (Cardiology), DM (Cardiology)",
            "experience": "18 years",
            "rating": 4.9,
            "fee": 1200
        },
        {
            "name": "Dr. Maria Garcia",
            "qualification": "MBBS, FACC (Cardiology)",
            "experience": "14 years",
            "rating": 4.8,
            "fee": 1000
        }
    ],
    "Neurologist": [
        {
            "name": "Dr. David Thompson",
            "qualification": "MBBS, MD (Neurology), DM (Neurology)",
            "experience": "20 years",
            "rating": 4.9,
            "fee": 1500
        },
        {
            "name": "Dr. Jennifer Lee",
            "qualification": "MBBS, DNB (Neurology)",
            "experience": "11 years",
            "rating": 4.6,
            "fee": 1200
        }
    ],
    "Pulmonologist": [
        {
            "name": "Dr. Richard Brown",
            "qualification": "MBBS, MD (Pulmonary Medicine)",
            "experience": "16 years",
            "rating": 4.7,
            "fee": 1000
        },
        {
            "name": "Dr. Patricia Davis",
            "qualification": "MBBS, DTCD (Pulmonology)",
            "experience": "9 years",
            "rating": 4.5,
            "fee": 900
        }
    ],
    "Gastroenterologist": [
        {
            "name": "Dr. Thomas Miller",
            "qualification": "MBBS, MD (Gastroenterology), DM (Gastro)",
            "experience": "22 years",
            "rating": 4.8,
            "fee": 1400
        },
        {
            "name": "Dr. Nancy Taylor",
            "qualification": "MBBS, DNB (Gastroenterology)",
            "experience": "13 years",
            "rating": 4.6,
            "fee": 1200
        }
    ]
}


def _render_star_rating(rating: float) -> str:
    """Render star rating display."""
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    
    stars = "★" * full_stars
    if half_star:
        stars += "★"
    stars += "☆" * empty_stars
    
    return f'<span style="color: #f59e0b;">{stars}</span> <span class="muted-text">({rating})</span>'


def _generate_booking_id() -> str:
    """Generate a random 6-digit booking ID."""
    return str(random.randint(100000, 999999))

st.markdown('<p class="page-title" style="color: #ffffff;">Book Appointment</p>', unsafe_allow_html=True)
st.markdown('<p class="muted-text">Schedule your consultation with our expert doctors.</p>', unsafe_allow_html=True)

# Initialize session state
if "appointment_data" not in st.session_state:
    st.session_state.appointment_data = {}

if "booking_confirmed" not in st.session_state:
    st.session_state.booking_confirmed = False

# Section 1: Select Specialty
st.markdown('<div class="section-title">Select Specialty</div>', unsafe_allow_html=True)

specialties = list(DOCTORS_DB.keys())
cols = st.columns(3)

for i, specialty in enumerate(specialties):
    with cols[i % 3]:
        is_selected = st.session_state.appointment_data.get("specialty") == specialty
        
        selected_style = "border-color: #7c3aed !important; box-shadow: 0 0 14px rgba(124, 58, 237, 0.4) !important;" if is_selected else ""
        border_color = "#7c3aed" if is_selected else "#30363d"
        
        st.markdown(f"""
        <div class="doctor-card" style="cursor: pointer; border: 2px solid {border_color}; text-align: center; {selected_style}; padding: 2rem;">
            <div style="font-weight: 600; color: #ffffff; font-family: 'Inter', sans-serif;">{specialty}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"Select {specialty}", key=f"spec_{i}", use_container_width=True):
            st.session_state.appointment_data["specialty"] = specialty
            st.session_state.appointment_data.pop("doctor", None)  # Reset doctor selection
            st.rerun()

# Section 2: Select Doctor
if "specialty" in st.session_state.appointment_data:
    selected_specialty = st.session_state.appointment_data["specialty"]
    doctors = DOCTORS_DB[selected_specialty]
    
    st.markdown('<div class="section-title" style="margin-top: 2rem;">Select Doctor</div>', unsafe_allow_html=True)
    
    doc_cols = st.columns(2)
    for i, doctor in enumerate(doctors):
        with doc_cols[i % 2]:
            is_doc_selected = st.session_state.appointment_data.get("doctor") == doctor
            doc_selected_style = "border-color: #7c3aed !important; box-shadow: 0 0 14px rgba(124, 58, 237, 0.4) !important;" if is_doc_selected else ""
            
            st.markdown(f"""
            <div class="doctor-card" style="{doc_selected_style}">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <h4 style="margin: 0 0 0.5rem 0; color: #ffffff; font-family: 'Inter', sans-serif;">{doctor['name']}</h4>
                        <p class="muted-text" style="margin: 0.25rem 0; font-size: 0.9rem;">{doctor['qualification']}</p>
                        <p class="muted-text" style="margin: 0.25rem 0; font-size: 0.9rem;">Experience: {doctor['experience']}</p>
                        <p style="margin: 0.25rem 0; font-size: 0.9rem;">{_render_star_rating(doctor['rating'])}</p>
                        <p class="mono-text" style="margin: 0.5rem 0 0 0; font-weight: 600; color: #a78bfa;">Consultation Fee: ${doctor['fee']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Select {doctor['name']}", key=f"doc_{i}", use_container_width=True):
                st.session_state.appointment_data["doctor"] = doctor
                st.rerun()

# Section 3: Book Slot
if "doctor" in st.session_state.appointment_data:
    st.markdown('<div class="section-title" style="margin-top: 2rem;">Book Slot</div>', unsafe_allow_html=True)
    
    # Date picker (only future dates)
    min_date = datetime.today() + timedelta(days=1)
    max_date = datetime.today() + timedelta(days=30)
    
    selected_date = st.date_input(
        "Select Date",
        min_value=min_date,
        max_value=max_date,
        value=min_date,
        format="YYYY-MM-DD"
    )
    
    # Time slots
    time_slots = ["10:00 AM", "11:00 AM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM"]
    
    st.markdown("<p style='color: white; margin-top: 1rem;'>Select Time Slot:</p>", unsafe_allow_html=True)
    slot_cols = st.columns(3)
    
    for i, slot in enumerate(time_slots):
        with slot_cols[i % 3]:
            is_selected = st.session_state.appointment_data.get("time_slot") == slot
            
            button_type = "primary" if is_selected else "secondary"
            if st.button(slot, key=f"slot_{i}", type=button_type, use_container_width=True):
                st.session_state.appointment_data["time_slot"] = slot
                st.session_state.appointment_data["date"] = selected_date
                st.rerun()

# Section 4: Patient Details
if "time_slot" in st.session_state.appointment_data:
    st.markdown('<div class="section-title" style="margin-top: 2rem;">Patient Details</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name", placeholder="Enter your full name")
            age = st.number_input("Age", min_value=1, max_value=120, value=25)
            
        with col2:
            phone = st.text_input("Phone Number", placeholder="+1 98765 43210")
        
        reason = st.text_area(
            "Reason for Visit", 
            placeholder="Please describe your symptoms or reason for consultation...",
            height=100
        )
        
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
        # Validation
        if st.button("Confirm Appointment", type="primary", use_container_width=True):
            if not all([name, age, phone, reason]):
                st.error("Please fill in all required fields.")
            elif len(phone) < 10:
                st.error("Please enter a valid phone number.")
            else:
                # Generate booking confirmation
                booking_id = _generate_booking_id()
                doctor = st.session_state.appointment_data["doctor"]
                date = st.session_state.appointment_data["date"]
                time_slot = st.session_state.appointment_data["time_slot"]
                
                # Store booking
                booking_data = {
                    "booking_id": booking_id,
                    "doctor": doctor["name"],
                    "specialty": st.session_state.appointment_data["specialty"],
                    "date": date.strftime("%Y-%m-%d"),
                    "time": time_slot,
                    "patient_name": name,
                    "age": age,
                    "phone": phone,
                    "reason": reason,
                    "fee": doctor["fee"]
                }
                
                if "bookings" not in st.session_state:
                    st.session_state.bookings = []
                
                st.session_state.bookings.append(booking_data)
                st.session_state.booking_confirmed = True
                st.session_state.current_booking = booking_data
                st.rerun()

# Show booking confirmation
if st.session_state.booking_confirmed and "current_booking" in st.session_state:
    booking = st.session_state.current_booking
    
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#238636" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 1rem;"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
        <h2 style="color: #238636; margin-bottom: 1rem;">Appointment Confirmed!</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background:#0d2818; border:1px solid #238636; box-shadow:0 0 20px rgba(35,134,54,0.2); border-radius:12px; padding:2rem; text-align:center; margin: 0 auto; max-width: 600px;">
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; font-weight: 700; color: #3fb950; margin-bottom: 1rem;">
            Booking ID: {booking['booking_id']}
        </div>
        <div class="muted-text" style="margin-bottom: 0.5rem;"><strong style="color: white; font-family: 'Inter', sans-serif;">Doctor:</strong> <span style="color: #c9d1d9; font-family: 'Inter', sans-serif;">{booking['doctor']}</span></div>
        <div class="muted-text" style="margin-bottom: 0.5rem;"><strong style="color: white; font-family: 'Inter', sans-serif;">Date:</strong> <span style="color: #c9d1d9; font-family: 'Inter', sans-serif;">{booking['date']}</span></div>
        <div class="muted-text" style="margin-bottom: 0.5rem;"><strong style="color: white; font-family: 'Inter', sans-serif;">Time:</strong> <span style="color: #c9d1d9; font-family: 'Inter', sans-serif;">{booking['time']}</span></div>
        <div class="muted-text" style="margin-bottom: 1rem;"><strong style="color: white; font-family: 'Inter', sans-serif;">Consultation Fee:</strong> <span class="mono-text" style="color: #a78bfa;">${booking['fee']}</span></div>
        <div style="font-family: 'Inter', sans-serif; color: #238636; font-weight: 600; margin-top: 1rem;">
            Your appointment is confirmed. Please arrive 10 minutes early.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
    if st.button("Book Another Appointment", use_container_width=True, type="primary"):
        # Reset for new booking
        st.session_state.appointment_data = {}
        st.session_state.booking_confirmed = False
        st.session_state.current_booking = None
        st.rerun()

