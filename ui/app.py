import streamlit as st
import requests
import pandas as pd
import json

BASE_URL = "http://localhost:8000/population-health"

st.set_page_config(
    page_title="Population Health Management",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Population Health Management")

menu = st.sidebar.radio(
    "Select Module",
    [
        "Patient Stratification",
        "Patient History",
        "Population Summary",
        "High Risk Patients",
        "Segment Distribution",
        "Health Check",
        "Clear Memory"
    ]
)

def display_response(data):

    if isinstance(data, dict):

        for key, value in data.items():

            if isinstance(value, dict):

                st.subheader(key.replace("_"," ").title())
                display_response(value)

            elif isinstance(value, list):

                st.subheader(key.replace("_"," ").title())

                if len(value) > 0 and isinstance(value[0], dict):
                    st.dataframe(pd.DataFrame(value), use_container_width=True)
                else:
                    st.write(value)

            else:
                st.metric(
                    key.replace("_"," ").title(),
                    value
                )

    elif isinstance(data, list):

        if len(data) > 0:
            st.dataframe(pd.DataFrame(data), use_container_width=True)

    else:
        st.write(data)

if menu == "Patient Stratification":

    st.header("Patient Risk Stratification")

    with st.form("population_form"):

        st.subheader("Patient Information")

        col1, col2 = st.columns(2)

        with col1:
            patient_id = st.text_input(
                "Patient ID",
                "PAT10001"
            )

            patient_name = st.text_input(
                "Patient Name",
                "John Doe"
            )

            age = st.number_input(
                "Age",
                min_value=0,
                max_value=120,
                value=68
            )

        with col2:

            gender = st.selectbox(
                "Gender",
                [
                    "Male",
                    "Female",
                    "Other"
                ]
            )

        st.divider()

        st.subheader("Diagnoses")

        diagnoses = st.multiselect(
            "Diagnoses",
            [
                "Type 2 Diabetes",
                "Hypertension",
                "Chronic Kidney Disease Stage 3",
                "Hyperlipidemia",
                "Heart Failure",
                "Asthma",
                "COPD",
                "Stroke",
                "Cancer"
            ],
            default=[
                "Type 2 Diabetes",
                "Hypertension",
                "Chronic Kidney Disease Stage 3",
                "Hyperlipidemia"
            ]
        )

        st.subheader("Medications")

        medications = st.multiselect(
            "Medications",
            [
                "Metformin 500mg",
                "Lisinopril 20mg",
                "Atorvastatin 40mg",
                "Aspirin 81mg",
                "Insulin",
                "Losartan",
                "Amlodipine",
                "Warfarin"
            ],
            default=[
                "Metformin 500mg",
                "Lisinopril 20mg",
                "Atorvastatin 40mg",
                "Aspirin 81mg"
            ]
        )

        st.subheader("Allergies")

        allergies = st.multiselect(
            "Allergies",
            [
                "Penicillin",
                "Sulfa",
                "Latex",
                "Peanuts",
                "Seafood"
            ],
            default=["Penicillin"]
        )

        st.divider()

        st.subheader("Vital Signs")

        c1, c2 = st.columns(2)

        with c1:

            systolic_bp = st.number_input(
                "Systolic BP",
                value=158
            )

            diastolic_bp = st.number_input(
                "Diastolic BP",
                value=96
            )

        with c2:

            heart_rate = st.number_input(
                "Heart Rate",
                value=92
            )

            bmi = st.number_input(
                "BMI",
                value=33.8,
                format="%.1f"
            )

        st.divider()

        st.subheader("Laboratory Results")

        c1, c2 = st.columns(2)

        with c1:

            hba1c = st.number_input(
                "HbA1c",
                value=8.4
            )

            cholesterol = st.number_input(
                "Cholesterol",
                value=235
            )

            ldl = st.number_input(
                "LDL",
                value=155
            )

        with c2:

            hdl = st.number_input(
                "HDL",
                value=38
            )

            triglycerides = st.number_input(
                "Triglycerides",
                value=245
            )

            creatinine = st.number_input(
                "Creatinine",
                value=1.9
            )

        st.divider()

        st.subheader("Lifestyle")

        smoker = st.checkbox(
            "Smoker",
            value=True
        )

        alcohol_use = st.checkbox(
            "Alcohol Use",
            value=False
        )

        exercise_frequency = st.slider(
            "Exercise Frequency / Week",
            0,
            7,
            1
        )

        st.divider()

        st.subheader("Social Determinants")

        employment_status = st.selectbox(
            "Employment Status",
            [
                "Employed",
                "Retired",
                "Unemployed",
                "Student"
            ],
            index=1
        )

        education_level = st.selectbox(
            "Education Level",
            [
                "Primary",
                "High School",
                "Graduate",
                "Post Graduate"
            ],
            index=1
        )

        housing_stability = st.selectbox(
            "Housing Stability",
            [
                "Stable",
                "Temporary",
                "Homeless"
            ]
        )

        transportation_access = st.checkbox(
            "Transportation Access",
            value=True
        )

        st.divider()

        st.subheader("Healthcare Utilization")

        c1, c2 = st.columns(2)

        with c1:

            hospital_visits = st.number_input(
                "Hospital Visits (Last Year)",
                value=5
            )

            emergency_visits = st.number_input(
                "Emergency Visits (Last Year)",
                value=3
            )

        with c2:

            admissions = st.number_input(
                "Admissions (Last Year)",
                value=2
            )

            readmissions = st.number_input(
                "Readmissions (Last Year)",
                value=1
            )

        submit = st.form_submit_button("🔍 Analyze Patient")

    if submit:

        request_data = {

            "patient_id": patient_id,
            "patient_name": patient_name,
            "age": age,
            "gender": gender,

            "diagnoses": diagnoses,

            "medications": medications,

            "allergies": allergies,

            "vital_signs": {
                "systolic_bp": systolic_bp,
                "diastolic_bp": diastolic_bp,
                "heart_rate": heart_rate,
                "bmi": bmi
            },

            "labs": {
                "hba1c": hba1c,
                "cholesterol": cholesterol,
                "ldl": ldl,
                "hdl": hdl,
                "triglycerides": triglycerides,
                "creatinine": creatinine
            },

            "lifestyle": {
                "smoker": smoker,
                "alcohol_use": alcohol_use,
                "exercise_frequency_per_week": exercise_frequency
            },

            "social_determinants": {
                "employment_status": employment_status,
                "education_level": education_level,
                "housing_stability": housing_stability,
                "transportation_access": transportation_access
            },

            "utilization_history": {
                "hospital_visits_last_year": hospital_visits,
                "emergency_visits_last_year": emergency_visits,
                "admissions_last_year": admissions,
                "readmissions_last_year": readmissions
            }
        }

        with st.expander("Request JSON"):

            st.json(request_data)

    

        response = requests.post(
            f"{BASE_URL}/stratify",
            json=request_data
        )

        if response.status_code == 200:

            st.success("Analysis Completed")

            result = response.json()

            display_response(result)

        else:
            st.error(response.text)

elif menu == "Patient History":

    st.header("Patient History")

    patient_id = st.text_input(
        "Patient ID",
        "PAT10001"
    )

    if st.button("Get History"):

        response = requests.get(
            f"{BASE_URL}/history/{patient_id}"
        )

        if response.status_code == 200:
            display_response(response.json())
        else:
            st.error(response.text)

elif menu == "Population Summary":

    st.header("Population Summary")

    if st.button("Load Summary"):

        response = requests.get(
            f"{BASE_URL}/population-summary"
        )

        if response.status_code == 200:

            result = response.json()

            display_response(result)

        else:
            st.error(response.text)

elif menu == "High Risk Patients":

    st.header("High Risk Patients")

    threshold = st.slider(
        "Risk Threshold",
        0.0,
        1.0,
        0.7,
        0.05
    )

    if st.button("Fetch Patients"):

        response = requests.get(
            f"{BASE_URL}/high-risk-patients",
            params={"threshold": threshold}
        )

        if response.status_code == 200:

            result = response.json()

            if isinstance(result, list):
                st.dataframe(pd.DataFrame(result), use_container_width=True)
            else:
                display_response(result)

        else:
            st.error(response.text)

elif menu == "Segment Distribution":

    st.header("Population Segment Distribution")

    if st.button("Load Distribution"):

        response = requests.get(
            f"{BASE_URL}/segment-distribution"
        )

        if response.status_code == 200:

            result = response.json()

            if isinstance(result, dict):

                df = pd.DataFrame(
                    result.items(),
                    columns=["Segment", "Count"]
                )

                st.dataframe(df, use_container_width=True)

                st.bar_chart(df.set_index("Segment"))

            else:
                display_response(result)

        else:
            st.error(response.text)

elif menu == "Health Check":

    st.header("API Health")

    if st.button("Check"):

        response = requests.get(
            f"{BASE_URL}/health"
        )

        if response.status_code == 200:
            st.success(response.json())
        else:
            st.error(response.text)

elif menu == "Clear Memory":

    st.header("Clear Population Memory")

    st.warning("This will clear all stored population analysis.")

    if st.button("Clear Memory"):

        response = requests.delete(
            f"{BASE_URL}/clear-memory"
        )

        if response.status_code == 200:
            st.success(response.json())
        else:
            st.error(response.text)