import streamlit as st

def render_patient_stratification_form():
    with st.form("population_form"):
        st.subheader("Patient Information")
        col1, col2 = st.columns(2)
        with col1:
            patient_id = st.text_input("Patient ID", "PAT10001")
            patient_name = st.text_input("Patient Name", "John Doe")
            age = st.number_input("Age", min_value=0, max_value=120, value=68)
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])

        st.divider()
        st.subheader("Diagnoses")
        diagnoses = st.multiselect(
            "Diagnoses",
            ["Type 2 Diabetes", "Hypertension", "Chronic Kidney Disease Stage 3",
             "Hyperlipidemia", "Heart Failure", "Asthma", "COPD", "Stroke", "Cancer"],
            default=["Type 2 Diabetes", "Hypertension",
                     "Chronic Kidney Disease Stage 3", "Hyperlipidemia"],
        )

        st.subheader("Medications")
        medications = st.multiselect(
            "Medications",
            ["Metformin 500mg", "Lisinopril 20mg", "Atorvastatin 40mg",
             "Aspirin 81mg", "Insulin", "Losartan", "Amlodipine", "Warfarin"],
            default=["Metformin 500mg", "Lisinopril 20mg",
                     "Atorvastatin 40mg", "Aspirin 81mg"],
        )

        st.subheader("Allergies")
        allergies = st.multiselect(
            "Allergies", ["Penicillin", "Sulfa", "Latex", "Peanuts", "Seafood"],
            default=["Penicillin"],
        )

        st.divider()
        st.subheader("Vital Signs")
        c1, c2 = st.columns(2)
        with c1:
            systolic_bp = st.number_input("Systolic BP", value=158)
            diastolic_bp = st.number_input("Diastolic BP", value=96)
        with c2:
            heart_rate = st.number_input("Heart Rate", value=92)
            bmi = st.number_input("BMI", value=33.8, format="%.1f")

        st.divider()
        st.subheader("Laboratory Results")
        c1, c2 = st.columns(2)
        with c1:
            hba1c = st.number_input("HbA1c", value=8.4)
            cholesterol = st.number_input("Cholesterol", value=235)
            ldl = st.number_input("LDL", value=155)
        with c2:
            hdl = st.number_input("HDL", value=38)
            triglycerides = st.number_input("Triglycerides", value=245)
            creatinine = st.number_input("Creatinine", value=1.9)

        st.divider()
        st.subheader("Lifestyle")
        smoker = st.checkbox("Smoker", value=True)
        alcohol_use = st.checkbox("Alcohol Use", value=False)
        exercise_frequency = st.slider("Exercise Frequency / Week", 0, 7, 1)

        st.divider()
        st.subheader("Social Determinants")
        employment_status = st.selectbox(
            "Employment Status", ["Employed", "Retired", "Unemployed", "Student"], index=1
        )
        education_level = st.selectbox(
            "Education Level", ["Primary", "High School", "Graduate", "Post Graduate"], index=1
        )
        housing_stability = st.selectbox(
            "Housing Stability", ["Stable", "Temporary", "Homeless"]
        )
        transportation_access = st.checkbox("Transportation Access", value=True)

        st.divider()
        st.subheader("Healthcare Utilization")
        c1, c2 = st.columns(2)
        with c1:
            hospital_visits = st.number_input("Hospital Visits (Last Year)", value=5)
            emergency_visits = st.number_input("Emergency Visits (Last Year)", value=3)
        with c2:
            admissions = st.number_input("Admissions (Last Year)", value=2)
            readmissions = st.number_input("Readmissions (Last Year)", value=1)

        submit = st.form_submit_button("🔍 Analyze Patient", use_container_width=True)

    payload = {
        "patient_id": patient_id, "patient_name": patient_name, "age": age, "gender": gender,
        "diagnoses": diagnoses, "medications": medications, "allergies": allergies,
        "vital_signs": {"systolic_bp": systolic_bp, "diastolic_bp": diastolic_bp,
                        "heart_rate": heart_rate, "bmi": bmi},
        "labs": {"hba1c": hba1c, "cholesterol": cholesterol, "ldl": ldl,
                 "hdl": hdl, "triglycerides": triglycerides, "creatinine": creatinine},
        "lifestyle": {"smoker": smoker, "alcohol_use": alcohol_use,
                      "exercise_frequency_per_week": exercise_frequency},
        "social_determinants": {
            "employment_status": employment_status, "education_level": education_level,
            "housing_stability": housing_stability,
            "transportation_access": transportation_access,
        },
        "utilization_history": {
            "hospital_visits_last_year": hospital_visits,
            "emergency_visits_last_year": emergency_visits,
            "admissions_last_year": admissions,
            "readmissions_last_year": readmissions,
        },
    }
    return submit, payload
