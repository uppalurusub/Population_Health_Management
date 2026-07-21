export interface VitalSigns {
  systolic_bp: number;
  diastolic_bp: number;
  heart_rate: number;
  bmi: number;
}

export interface Labs {
  hba1c: number;
  cholesterol: number;
  ldl: number;
  hdl: number;
  triglycerides: number;
  creatinine: number;
}

export interface Lifestyle {
  smoker: boolean;
  alcohol_use: boolean;
  exercise_frequency_per_week: number;
}

export interface SocialDeterminants {
  employment_status: string;
  education_level: string;
  housing_stability: string;
  transportation_access: boolean;
}

export interface UtilizationHistory {
  hospital_visits_last_year: number;
  emergency_visits_last_year: number;
  admissions_last_year: number;
  readmissions_last_year: number;
}

export interface PatientRequest {
  patient_id: string;
  patient_name: string;
  age: number;
  gender: string;
  diagnoses: string[];
  medications: string[];
  allergies: string[];
  vital_signs: VitalSigns;
  labs: Labs;
  lifestyle: Lifestyle;
  social_determinants: SocialDeterminants;
  utilization_history: UtilizationHistory;
}

export interface PopulationSegment {
  segment_name: string;
  segment_description: string;
}

export interface RiskAssessment {
  risk_level: string;
  risk_score: number;
  readmission_risk: number;
  mortality_risk: number;
  chronic_disease_risk: number | null;
  cost_risk: number;
}

export interface CareGap {
  category: string;
  description: string;
  priority: string;
}

export interface Intervention {
  intervention_type: string;
  recommendation: string;
  priority: string;
}

export interface AgentFinding {
  agent_name: string;
  findings: string;
}

export interface PopulationHealthResponse {
  success: boolean;
  patient_id: string;
  patient_name: string;
  population_segment: PopulationSegment;
  risk_assessment: RiskAssessment;
  care_gaps: CareGap[];
  interventions: Intervention[];
  agent_findings: AgentFinding[];
  summary: string;
  message: string;
}