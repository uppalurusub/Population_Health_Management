import { useState } from "react";
import { Activity } from "lucide-react";
import { stratifyPatient } from "./api/populationHealthApi";
import PatientStratificationForm from "./components/PatientStratificationForm";
import StratificationResult from "./components/StratificationResult";
import { SAMPLE_PATIENTS } from "./data/samplePatients";
import type { PatientRequest, PopulationHealthResponse } from "./types/populationHealth";

export default function App() {
  const [request, setRequest] = useState<PatientRequest>(SAMPLE_PATIENTS.lowRisk);
  const [response, setResponse] = useState<PopulationHealthResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    setLoading(true);
    setError("");
    setResponse(null);
    try {
      setResponse(await stratifyPatient(request));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to stratify patient.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <header className="hero">
        <div className="hero-icon"><Activity size={30} /></div>
        <div>
          <h1>Population Health Management</h1>
          <p>Patient stratification and risk assessment</p>
        </div>
      </header>

      <main className="page-grid">
        <PatientStratificationForm
          value={request}
          onChange={setRequest}
          onSubmit={handleSubmit}
          loading={loading}
        />
        <section className="results-column">
          {error && <div className="error-banner">{error}</div>}
          {response ? (
            <StratificationResult response={response} />
          ) : (
            <div className="empty-state">
              Submit patient information to view population segment, risk assessment,
              care gaps, interventions, and agent findings.
            </div>
          )}
        </section>
      </main>
    </div>
  );
}