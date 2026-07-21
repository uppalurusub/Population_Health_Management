# Population Health Management System

An AI-powered **Population Health Management System** that performs intelligent patient risk stratification, population analytics, chronic disease assessment, and personalized healthcare recommendations using a Multi-Agent architecture built with **AutoGen**, **FastAPI**, and **React**.

---

# Project Architecture

```
Population_Health_Management
│
├── backend
│   └── population-health-management-python-app
│
├── ui
│   ├── Streamlit App
│   └── ReactJS Application
│
└── requirements.txt
```

---

# Features

## Patient Risk Stratification

- AI-driven patient risk assessment
- Risk score calculation
- Chronic disease evaluation
- Lifestyle risk analysis
- Social determinant analysis
- Healthcare utilization assessment
- Personalized recommendations

---

## Population Analytics

- Population Summary
- High Risk Population
- Population Segmentation
- Risk Distribution
- Disease Burden Analysis
- Care Gap Identification

---

## AI Multi-Agent Workflow

The backend utilizes multiple AI agents responsible for specialized healthcare analysis.

Example responsibilities include:

- Population Risk Agent
- Clinical Assessment Agent
- Lifestyle Analysis Agent
- Social Determinants Agent
- Recommendation Agent
- Summary Agent

---

# Technology Stack

## Backend

- Python 3.11+
- FastAPI
- AutoGen 0.7.5
- Pydantic
- Async Programming
- REST APIs

---

## Frontend

- React 19
- TypeScript
- Vite
- Axios
- React Markdown

---

# Backend Architecture

```
Client

   │

FastAPI Router

   │

Service Layer

   │

Implementation Layer

   │

AutoGen Agents

   │

Conversation Memory

   │

Response
```

---

# Project Structure

```
backend/

population-health-management-python-app/

│

├── agents/
│     population_agents.py
│
├── config/
│     llm_config.py
│
├── implementation/
│     population_impl.py
│
├── memory/
│     population_memory.py
│
├── models/
│     request_model.py
│     response_model.py
│
├── routers/
│     population_router.py
│
├── services/
│     population_service.py
│
├── utils/
│     logger.py
│
└── main.py
```

---

# React Frontend Structure

```
src/

├── api/
│     httpClient.ts
│     populationHealthApi.ts
│
├── components/
│     PatientStratificationForm.tsx
│     StratificationResult.tsx
│     RiskMetric.tsx
│     MarkdownContent.tsx
│
├── data/
│     samplePatients.ts
│
├── styles/
│
├── types/
│
├── App.tsx
└── main.tsx
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>

cd Population_Health_Management
```

---

# Backend Setup

Navigate to backend.

```bash
cd backend/population-health-management-python-app
```

Create virtual environment.

```bash
python -m venv venv
```

Activate environment.

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies.

```bash
pip install -r ../../requirements.txt
```

Configure environment variables.

Example:

```env
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4
```

---

# Run Backend

```bash
uvicorn main:app --reload
```

Backend runs at

```
http://localhost:8000
```

---

# API Documentation

Swagger

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# Frontend Setup

Navigate to React application.

```bash
cd ui/reactjs/population-health-management-reactjs-app
```

Install packages.

```bash
npm install
```

Run application.

```bash
npm run dev
```

Frontend

```
http://localhost:5173
```

---

# REST API Endpoints

## Root

```
GET /
```

Returns application status.

---

## Health

```
GET /health
```

Health check endpoint.

---

## API Information

```
GET /info
```

Returns application information and architecture.

---

## Patient Stratification

```
POST /population-health/stratify
```

Performs comprehensive patient risk stratification.

---

## Patient History

```
GET /population-health/history/{patient_id}
```

Returns historical patient analyses.

---

## Population Summary

```
GET /population-health/population-summary
```

Returns population-level analytics.

---

## High Risk Patients

```
GET /population-health/high-risk-patients
```

Query Parameter

```
threshold=0.7
```

Returns patients above the specified risk threshold.

---

## Segment Distribution

```
GET /population-health/segment-distribution
```

Returns distribution of patient segments.

---

# Sample Request

```json
{
  "patient_id": "P1001",
  "patient_name": "John Doe",
  "age": 62,
  "gender": "Male",
  "diagnoses": [
    "Diabetes",
    "Hypertension"
  ],
  "medications": [
    "Metformin",
    "Lisinopril"
  ],
  "allergies": [],
  "vital_signs": {
    "systolic_bp": 145,
    "diastolic_bp": 92,
    "heart_rate": 84,
    "bmi": 31.2
  },
  "labs": {
    "hba1c": 8.1,
    "cholesterol": 230
  }
}
```

---

# Expected Workflow

```
Patient Information

        │

Clinical Assessment

        │

Lifestyle Evaluation

        │

Social Determinants

        │

Healthcare Utilization

        │

Risk Stratification

        │

Population Segmentation

        │

Recommendations

        │

Final AI Summary
```

---

# Frontend Features

- Patient Stratification Form
- Sample Patient Data
- Risk Metrics Dashboard
- Markdown AI Response Rendering
- Population Risk Visualization
- Responsive User Interface
- REST API Integration

---

# Logging

Application logs are stored in

```
logs/

healthcare.log

error.log
```

---

# Future Enhancements

- Dashboard Analytics
- Predictive Risk Models
- Real-Time Population Monitoring
- FHIR Integration
- Electronic Health Record (EHR) Integration
- ML-Based Risk Prediction
- Role-Based Access Control (RBAC)
- Docker Deployment
- Kubernetes Deployment
- Azure Cloud Deployment

---

# Tech Stack Summary

| Layer | Technology |
|----------|------------|
| Frontend | React 19 |
| Language | TypeScript |
| UI Build | Vite |
| HTTP Client | Axios |
| Backend | FastAPI |
| AI Framework | AutoGen 0.7.5 |
| Validation | Pydantic |
| Architecture | Multi-Agent |
| API | REST |
| Logging | Python Logging |

---

# License

This project is intended for educational, research, and healthcare AI demonstration purposes.