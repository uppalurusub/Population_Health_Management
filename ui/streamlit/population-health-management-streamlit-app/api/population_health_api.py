import requests

BASE_URL = "http://localhost:8000/population-health"
TIMEOUT = 60000

def _handle(response):
    response.raise_for_status()
    return response.json()

def stratify_patient(payload):
    return _handle(requests.post(f"{BASE_URL}/stratify", json=payload, timeout=TIMEOUT))

def get_patient_history(patient_id):
    return _handle(requests.get(f"{BASE_URL}/history/{patient_id}", timeout=TIMEOUT))

def get_population_summary():
    return _handle(requests.get(f"{BASE_URL}/population-summary", timeout=TIMEOUT))

def get_high_risk_patients(threshold):
    return _handle(requests.get(
        f"{BASE_URL}/high-risk-patients",
        params={"threshold": threshold},
        timeout=TIMEOUT,
    ))

def get_segment_distribution():
    return _handle(requests.get(f"{BASE_URL}/segment-distribution", timeout=TIMEOUT))

def health_check():
    return _handle(requests.get(f"{BASE_URL}/health", timeout=TIMEOUT))

def clear_memory():
    return _handle(requests.delete(f"{BASE_URL}/clear-memory", timeout=TIMEOUT))
