import requests
import streamlit as st

from api.population_health_api import (
    stratify_patient, get_patient_history, get_population_summary,
    get_high_risk_patients, get_segment_distribution, health_check, clear_memory,
)
from components.request_form import render_patient_stratification_form
from components.response_view import display_response, display_segment_distribution
from components.sidebar import render_sidebar

st.set_page_config(page_title="Population Health Management", page_icon="🏥", layout="wide")
st.title("🏥 Population Health Management")
menu = render_sidebar()

def run_api(action, success_message=None):
    try:
        result = action()
        if success_message:
            st.success(success_message)
        return result
    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to the Population Health API. Verify that FastAPI is running on http://localhost:8000.")
    except requests.exceptions.Timeout:
        st.error("The API request timed out.")
    except requests.exceptions.HTTPError as exc:
        detail = exc.response.text if exc.response is not None else str(exc)
        st.error(f"API request failed: {detail}")
    except requests.exceptions.RequestException as exc:
        st.error(f"Request error: {exc}")
    return None

if menu == "Patient Stratification":
    st.header("Patient Risk Stratification")
    submit, request_data = render_patient_stratification_form()
    if submit:
        with st.expander("Request JSON"):
            st.json(request_data)
        with st.spinner("Analyzing patient..."):
            result = run_api(lambda: stratify_patient(request_data), "Analysis Completed")
        if result is not None:
            display_response(result)

elif menu == "Patient History":
    st.header("Patient History")
    patient_id = st.text_input("Patient ID", "PAT10001")
    if st.button("Get History"):
        result = run_api(lambda: get_patient_history(patient_id))
        if result is not None:
            display_response(result)

elif menu == "Population Summary":
    st.header("Population Summary")
    if st.button("Load Summary"):
        result = run_api(get_population_summary)
        if result is not None:
            display_response(result)

elif menu == "High Risk Patients":
    st.header("High Risk Patients")
    threshold = st.slider("Risk Threshold", 0.0, 1.0, 0.7, 0.05)
    if st.button("Fetch Patients"):
        result = run_api(lambda: get_high_risk_patients(threshold))
        if result is not None:
            display_response(result)

elif menu == "Segment Distribution":
    st.header("Population Segment Distribution")
    if st.button("Load Distribution"):
        result = run_api(get_segment_distribution)
        if result is not None:
            display_segment_distribution(result)

elif menu == "Health Check":
    st.header("API Health")
    if st.button("Check"):
        result = run_api(health_check)
        if result is not None:
            st.success("API is healthy.")
            display_response(result)