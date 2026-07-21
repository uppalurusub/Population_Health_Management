from pydantic import BaseModel
from typing import List, Optional, Dict


class RiskAssessment(BaseModel):
    risk_level: str
    risk_score: float

    readmission_risk: Optional[float] = None
    mortality_risk: Optional[float] = None
    chronic_disease_risk: Optional[float] = None
    cost_risk: Optional[float] = None


class PopulationSegment(BaseModel):
    segment_name: str
    segment_description: str


class CareGap(BaseModel):
    category: str
    description: str
    priority: str


class Intervention(BaseModel):
    intervention_type: str
    recommendation: str
    priority: str


class AgentFinding(BaseModel):
    agent_name: str
    findings: str


class PopulationHealthResponse(BaseModel):

    success: bool = True

    patient_id: str
    patient_name: str

    population_segment: PopulationSegment

    risk_assessment: RiskAssessment

    care_gaps: List[CareGap]

    interventions: List[Intervention]

    agent_findings: List[AgentFinding]

    summary: str

    message: str