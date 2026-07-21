import streamlit as st

MENU_OPTIONS = [
    "Patient Stratification",
    "Patient History",
    "Population Summary",
    "High Risk Patients",
    "Segment Distribution",
    "Health Check",
    "Clear Memory",
]

def render_sidebar():
    with st.sidebar:
        st.title("🏥 Population Health")
        return st.radio("Select Module", MENU_OPTIONS)
