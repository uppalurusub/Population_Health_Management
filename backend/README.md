# Population Health Management System

A production-ready **Population Health Management (PHM)** solution built using **FastAPI**, **Microsoft AutoGen 0.7.5**, and **LLM-powered Multi-Agent AI**.

The system performs intelligent patient stratification, risk assessment, care gap identification, intervention recommendation, and population analytics to support value-based healthcare and proactive care management.

---

# Features

- Multi-Agent AI powered by AutoGen 0.7.5
- Patient Population Stratification
- Clinical Risk Assessment
- Care Gap Analysis
- Personalized Intervention Recommendations
- Population-Level Analytics
- High-Risk Patient Identification
- Segment Distribution Analysis
- Patient History Management
- Memory-based Patient Tracking
- Structured REST APIs
- Swagger Documentation
- Loguru Logging
- MLflow Integration
- Modular FastAPI Architecture

---

# Architecture

```
                +----------------+
                | FastAPI Client |
                +--------+-------+
                         |
                         v
                +----------------+
                | Population API |
                +--------+-------+
                         |
                  Router Layer
                         |
                  Service Layer
                         |
              Implementation Layer
                         |
                AutoGen Multi-Agent
                         |
    +-----------+-----------+-----------+-----------+
    |           |           |           |           |
Data Agent  Segmentation Risk Agent Intervention Agent
                         |
                  Population Memory
                         |
                    Response Builder
```

---

# Project Structure

```
Population_Health_Management
│
├── app
│   ├── agents
│   │     population_agents.py
│   │
│   ├── config
│   │     llm_config.py
│   │     llm_models_config.py
│   │
│   ├── implementation
│   │     population_impl.py
│   │
│   ├── memory
│   │     population_memory.py
│   │
│   ├── models
│   │     request_model.py
│   │     response_model.py
│   │
│   ├── routers
│   │     population_router.py
│   │
│   ├── services
│   │     population_service.py
│   │
│   ├── utils
│   │     logger.py
│   │     json_utils.py
│   │     prompt_templates.py
│   │
│   └── main.py
│
├── logs
│
├── requirements.txt
│
├── mlflow.db
│
└── .env
```

---

# Multi-Agent Workflow

## 1. Data Agent

Responsibilities

- Analyze patient demographics
- Analyze diagnoses
- Review medications
- Review utilization history
- Generate clinical summary

Outputs

- Clinical Summary
- Chronic Conditions
- Utilization Findings

---

## 2. Segmentation Agent

Classifies patients into population groups.

Example Segments

- Healthy
- Preventive Care
- Chronic Disease
- High Risk
- Elderly Care
- Frequent Utilizer
- Complex Care

Outputs

- Segment Name
- Segment Reason

---

## 3. Risk Agent

Predicts patient risks.

Outputs

- Overall Risk Level
- Risk Score
- Readmission Risk
- Mortality Risk
- Cost Risk

---

## 4. Intervention Agent

Recommends personalized interventions.

Examples

- Lifestyle Coaching
- Preventive Screening
- Medication Review
- Specialist Referral
- Care Coordination
- Disease Management

---

# Population Analytics

The API provides analytics including

- Population Summary
- High-Risk Population
- Segment Distribution
- Patient History
- Memory Statistics

---

# REST APIs

## Base URL

```
http://localhost:8000
```

---

## Health Check

```
GET /health
```

Response

```json
{
  "status": "healthy",
  "service": "Population Health Management API"
}
```

---

## Application Info

```
GET /info
```

---

## Stratify Patient

```
POST /population-health/stratify
```

Sample Request

```json
{
  "patient_id": "PAT10001",
  "patient_name": "John Doe",
  "age": 67,
  "gender": "Male",
  "diagnoses": [
    "Hypertension",
    "Type 2 Diabetes"
  ],
  "medications": [
    "Metformin",
    "Lisinopril"
  ],
  "allergies": [
    "Penicillin"
  ],
  "vital_signs": {
    "systolic_bp": 150,
    "diastolic_bp": 95,
    "heart_rate": 92,
    "bmi": 31.8
  },
  "labs": {
    "hba1c": 8.4,
    "cholesterol": 240,
    "ldl": 170,
    "hdl": 38,
    "triglycerides": 210,
    "creatinine": 1.2
  },
  "lifestyle": {
    "smoker": true,
    "alcohol_use": false,
    "exercise_frequency_per_week": 1
  },
  "social_determinants": {
    "employment_status": "Retired",
    "education_level": "College",
    "housing_stability": "Stable",
    "transportation_access": true
  },
  "utilization_history": {
    "hospital_visits_last_year": 4,
    "emergency_visits_last_year": 2,
    "admissions_last_year": 2,
    "readmissions_last_year": 1
  }
}
```

---

Sample Response

```json
{
  "success": true,
  "patient_id": "PAT10001",
  "patient_name": "John Doe",
  "population_segment": {
    "segment_name": "High Risk Chronic Care",
    "segment_description": "Multiple chronic diseases requiring coordinated care."
  },
  "risk_assessment": {
    "risk_level": "High",
    "risk_score": 0.88,
    "readmission_risk": 0.82,
    "mortality_risk": 0.33,
    "cost_risk": 0.91
  },
  "care_gaps": [
    {
      "category": "Diabetes",
      "description": "HbA1c above target",
      "priority": "High"
    }
  ],
  "interventions": [
    {
      "intervention_type": "Care Coordination",
      "recommendation": "Enroll in chronic disease management program.",
      "priority": "High"
    }
  ],
  "agent_findings": [
    {
      "agent_name": "Risk Agent",
      "findings": "High readmission risk identified."
    }
  ],
  "summary": "Patient classified as High Risk Chronic Care.",
  "message": "Population analysis completed successfully."
}
```

---

## Get Patient History

```
GET /population-health/history/{patient_id}
```

Example

```
GET /population-health/history/PAT10001
```

---

## Population Summary

```
GET /population-health/population-summary
```

---

## High-Risk Patients

```
GET /population-health/high-risk-patients?threshold=0.7
```

---

## Segment Distribution

```
GET /population-health/segment-distribution
```

---

## Clear Memory

```
DELETE /population-health/clear-memory
```

---

# Request Model

Patient demographics

- Patient ID
- Patient Name
- Age
- Gender

Clinical Information

- Diagnoses
- Medications
- Allergies

Vital Signs

- Blood Pressure
- Heart Rate
- BMI

Laboratory Results

- HbA1c
- Cholesterol
- LDL
- HDL
- Triglycerides
- Creatinine

Lifestyle Factors

- Smoking
- Alcohol
- Exercise

Social Determinants

- Employment
- Education
- Housing
- Transportation

Healthcare Utilization

- Hospital Visits
- Emergency Visits
- Admissions
- Readmissions

---

# Technologies

| Component | Technology |
|------------|------------|
| Language | Python 3.11+ |
| API | FastAPI |
| AI Agents | AutoGen 0.7.5 |
| LLM | OpenAI / Azure OpenAI Compatible |
| Validation | Pydantic |
| Logging | Loguru |
| Experiment Tracking | MLflow |
| Server | Uvicorn |

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

---

Windows

```bash
.venv\Scripts\activate
```

Linux

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create `.env`

```text
OPENAI_API_KEY=your_api_key

OPENAI_MODEL=gpt-4o-mini

OPENAI_BASE_URL=https://api.openai.com/v1
```

---

## Run Application

```bash
uvicorn app.main:app --reload
```

---

Swagger

```
http://localhost:8000/docs
```

---

ReDoc

```
http://localhost:8000/redoc
```

---

# Logging

Log files are stored under

```
logs/

healthcare.log

error.log
```

Loguru is used for

- API Requests
- Agent Execution
- Exceptions
- Population Analysis
- Risk Prediction
- Memory Operations

---

# MLflow

The project includes MLflow configuration for experiment tracking.

Example

```bash
mlflow ui
```

---

# Future Enhancements

- Predictive Risk Models
- Explainable AI (XAI)
- Real-Time Population Dashboard
- FHIR Integration
- HL7 Integration
- SMART on FHIR Support
- Care Plan Automation
- Social Risk Prediction
- Chronic Disease Forecasting
- Hospital Readmission Prediction
- Population Health KPIs
- Power BI Dashboard Export
- Vector Database for Patient Knowledge
- Multi-Hospital Population Analytics

---

# Use Cases

- Population Health Management
- Value-Based Care
- Chronic Disease Management
- Risk Stratification
- Preventive Healthcare
- Care Coordination
- Readmission Reduction
- Health Insurance Analytics
- Provider Network Optimization
- Public Health Monitoring

---

# License

This project is intended for educational, research, and enterprise healthcare solution development. Ensure compliance with HIPAA, GDPR, and applicable healthcare regulations before deploying in production.
