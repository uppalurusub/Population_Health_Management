from pydantic import BaseModel, Field
from typing import List, Optional


class VitalSigns(BaseModel):
    systolic_bp: int = Field(..., description="Systolic Blood Pressure")
    diastolic_bp: int = Field(..., description="Diastolic Blood Pressure")
    heart_rate: int
    bmi: float


class LabResults(BaseModel):
    hba1c: Optional[float] = None
    cholesterol: Optional[float] = None
    ldl: Optional[float] = None
    hdl: Optional[float] = None
    triglycerides: Optional[float] = None
    creatinine: Optional[float] = None


class LifestyleFactors(BaseModel):
    smoker: bool = False
    alcohol_use: bool = False
    exercise_frequency_per_week: int = 0


class SocialDeterminants(BaseModel):
    employment_status: Optional[str] = None
    education_level: Optional[str] = None
    housing_stability: Optional[str] = None
    transportation_access: Optional[bool] = None


class UtilizationHistory(BaseModel):
    hospital_visits_last_year: int = 0
    emergency_visits_last_year: int = 0
    admissions_last_year: int = 0
    readmissions_last_year: int = 0


class PatientRequest(BaseModel):

    patient_id: str
    patient_name: str

    age: int
    gender: str

    diagnoses: List[str] = []
    medications: List[str] = []
    allergies: List[str] = []

    vital_signs: VitalSigns

    labs: Optional[LabResults] = None

    lifestyle: Optional[LifestyleFactors] = None

    social_determinants: Optional[SocialDeterminants] = None

    utilization_history: Optional[UtilizationHistory] = None