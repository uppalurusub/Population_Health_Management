import type { PatientRequest } from "../types/populationHealth";
import { SAMPLE_PATIENTS } from "../data/samplePatients";

interface Props {
  value: PatientRequest;
  onChange: (value: PatientRequest) => void;
  onSubmit: () => void;
  loading: boolean;
}

const parseList = (value: string) =>
  value.split("\n").map((item) => item.trim()).filter(Boolean);

export default function PatientStratificationForm({ value, onChange, onSubmit, loading }: Props) {
  const setRoot = <K extends keyof PatientRequest>(key: K, next: PatientRequest[K]) =>
    onChange({ ...value, [key]: next });

  const setNested = <
    K extends "vital_signs" | "labs" | "lifestyle" | "social_determinants" | "utilization_history",
    F extends keyof PatientRequest[K]
  >(section: K, field: F, next: PatientRequest[K][F]) =>
    onChange({ ...value, [section]: { ...value[section], [field]: next } });

  return (
    <section className="form-panel">
      <div className="panel-heading">
        <div>
          <h2>Patient Request</h2>
          <p>POST /population-health/stratify</p>
        </div>
        <select
          aria-label="Load sample patient"
          defaultValue="lowRisk"
          onChange={(e) => onChange(SAMPLE_PATIENTS[e.target.value as keyof typeof SAMPLE_PATIENTS])}
        >
          <option value="sample">Sample patient</option>
          <option value="highRisk">High-risk patient</option>
          <option value="lowRisk">Low-risk patient</option>
        </select>
      </div>

      <div className="form-grid">
        <Field label="Patient ID" value={value.patient_id} onChange={(v) => setRoot("patient_id", v)} />
        <Field label="Patient Name" value={value.patient_name} onChange={(v) => setRoot("patient_name", v)} />
        <NumberField label="Age" value={value.age} onChange={(v) => setRoot("age", v)} />
        <Field label="Gender" value={value.gender} onChange={(v) => setRoot("gender", v)} />
      </div>

      <FormSection title="Clinical Profile">
        <TextArea label="Diagnoses (one per line)" value={value.diagnoses.join("\n")} onChange={(v) => setRoot("diagnoses", parseList(v))} />
        <TextArea label="Medications (one per line)" value={value.medications.join("\n")} onChange={(v) => setRoot("medications", parseList(v))} />
        <TextArea label="Allergies (one per line)" value={value.allergies.join("\n")} onChange={(v) => setRoot("allergies", parseList(v))} />
      </FormSection>

      <FormSection title="Vital Signs">
        <NumberField label="Systolic BP" value={value.vital_signs.systolic_bp} onChange={(v) => setNested("vital_signs", "systolic_bp", v)} />
        <NumberField label="Diastolic BP" value={value.vital_signs.diastolic_bp} onChange={(v) => setNested("vital_signs", "diastolic_bp", v)} />
        <NumberField label="Heart Rate" value={value.vital_signs.heart_rate} onChange={(v) => setNested("vital_signs", "heart_rate", v)} />
        <NumberField label="BMI" value={value.vital_signs.bmi} onChange={(v) => setNested("vital_signs", "bmi", v)} step="0.1" />
      </FormSection>

      <FormSection title="Labs">
        {(["hba1c", "cholesterol", "ldl", "hdl", "triglycerides", "creatinine"] as const).map((field) => (
          <NumberField key={field} label={field.toUpperCase()} value={value.labs[field]} onChange={(v) => setNested("labs", field, v)} step="0.1" />
        ))}
      </FormSection>

      <FormSection title="Lifestyle">
        <BooleanField label="Smoker" value={value.lifestyle.smoker} onChange={(v) => setNested("lifestyle", "smoker", v)} />
        <BooleanField label="Alcohol Use" value={value.lifestyle.alcohol_use} onChange={(v) => setNested("lifestyle", "alcohol_use", v)} />
        <NumberField label="Exercise / Week" value={value.lifestyle.exercise_frequency_per_week} onChange={(v) => setNested("lifestyle", "exercise_frequency_per_week", v)} />
      </FormSection>

      <FormSection title="Social Determinants">
        <Field label="Employment Status" value={value.social_determinants.employment_status} onChange={(v) => setNested("social_determinants", "employment_status", v)} />
        <Field label="Education Level" value={value.social_determinants.education_level} onChange={(v) => setNested("social_determinants", "education_level", v)} />
        <Field label="Housing Stability" value={value.social_determinants.housing_stability} onChange={(v) => setNested("social_determinants", "housing_stability", v)} />
        <BooleanField label="Transportation Access" value={value.social_determinants.transportation_access} onChange={(v) => setNested("social_determinants", "transportation_access", v)} />
      </FormSection>

      <FormSection title="Utilization History">
        <NumberField label="Hospital Visits" value={value.utilization_history.hospital_visits_last_year} onChange={(v) => setNested("utilization_history", "hospital_visits_last_year", v)} />
        <NumberField label="Emergency Visits" value={value.utilization_history.emergency_visits_last_year} onChange={(v) => setNested("utilization_history", "emergency_visits_last_year", v)} />
        <NumberField label="Admissions" value={value.utilization_history.admissions_last_year} onChange={(v) => setNested("utilization_history", "admissions_last_year", v)} />
        <NumberField label="Readmissions" value={value.utilization_history.readmissions_last_year} onChange={(v) => setNested("utilization_history", "readmissions_last_year", v)} />
      </FormSection>

      <button className="primary-button" disabled={loading} onClick={onSubmit}>
        {loading ? "Stratifying Patient..." : "Stratify Patient"}
      </button>
    </section>
  );
}

function FormSection({ title, children }: { title: string; children: React.ReactNode }) {
  return <fieldset><legend>{title}</legend><div className="form-grid">{children}</div></fieldset>;
}
function Field({ label, value, onChange }: { label: string; value: string; onChange: (value: string) => void }) {
  return <label><span>{label}</span><input value={value} onChange={(e) => onChange(e.target.value)} /></label>;
}
function NumberField({ label, value, onChange, step = "1" }: { label: string; value: number; onChange: (value: number) => void; step?: string }) {
  return <label><span>{label}</span><input type="number" step={step} value={value} onChange={(e) => onChange(Number(e.target.value))} /></label>;
}
function TextArea({ label, value, onChange }: { label: string; value: string; onChange: (value: string) => void }) {
  return <label className="wide-field"><span>{label}</span><textarea rows={4} value={value} onChange={(e) => onChange(e.target.value)} /></label>;
}
function BooleanField({ label, value, onChange }: { label: string; value: boolean; onChange: (value: boolean) => void }) {
  return <label><span>{label}</span><select value={String(value)} onChange={(e) => onChange(e.target.value === "true")}><option value="true">Yes</option><option value="false">No</option></select></label>;
}