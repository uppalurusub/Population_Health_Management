import { Bot, CheckCircle2, HeartPulse, ShieldAlert, Stethoscope } from "lucide-react";
import type { PopulationHealthResponse } from "../types/populationHealth";
import MarkdownContent from "./MarkdownContent";
import RiskMetric from "./RiskMetric";

export default function StratificationResult({ response }: { response: PopulationHealthResponse }) {
  const risk = response.risk_assessment;

  return (
    <div className="response-stack">
      <section className="success-card">
        <CheckCircle2 size={24} />
        <div><strong>{response.message}</strong><span>{response.patient_name} · {response.patient_id}</span></div>
      </section>

      <section className="result-card">
        <CardTitle icon={<HeartPulse size={20} />} title="Population Segment" />
        <h3>{response.population_segment.segment_name.replace(/^Segment Name:\s*/i, "")}</h3>
        <div className="readable-text">{response.population_segment.segment_description.replace(/^Segment Name:.*\n?/i, "")}</div>
      </section>

      <section className="result-card">
        <CardTitle icon={<ShieldAlert size={20} />} title="Risk Assessment" />
        <div className="risk-level-row"><span>Risk Level</span><strong className={`risk-pill ${risk.risk_level.toLowerCase()}`}>{risk.risk_level}</strong></div>
        <div className="metric-grid">
          <RiskMetric label="Overall Risk Score" value={risk.risk_score} />
          <RiskMetric label="Readmission Risk" value={risk.readmission_risk} />
          <RiskMetric label="Mortality Risk" value={risk.mortality_risk} />
          <RiskMetric label="Chronic Disease Risk" value={risk.chronic_disease_risk} />
          <RiskMetric label="Cost Risk" value={risk.cost_risk} />
        </div>
      </section>

      <section className="result-card">
        <CardTitle icon={<Stethoscope size={20} />} title="Care Gaps" />
        <div className="row-list">
          {response.care_gaps.map((gap, index) => (
            <div className="data-row" key={`${gap.category}-${index}`}>
              <div><strong>{gap.category}</strong><p>{gap.description}</p></div>
              <span className="priority-pill">{gap.priority}</span>
            </div>
          ))}
        </div>
      </section>

      <section className="result-card">
        <CardTitle icon={<HeartPulse size={20} />} title="Interventions" />
        <div className="row-list">
          {response.interventions.map((intervention, index) => (
            <article className="content-row" key={`${intervention.intervention_type}-${index}`}>
              <div className="content-row-header">
                <strong>{intervention.intervention_type}</strong>
                <span className="priority-pill">{intervention.priority}</span>
              </div>
              <MarkdownContent content={intervention.recommendation} />
            </article>
          ))}
        </div>
      </section>

      <section className="result-card">
        <CardTitle icon={<Bot size={20} />} title="Agent Findings" />
        <div className="agent-list">
          {response.agent_findings.map((agent, index) => (
            <article className="agent-card" key={`${agent.agent_name}-${index}`}>
              <div className="agent-card-title"><Bot size={18} /><strong>{agent.agent_name}</strong></div>
              <MarkdownContent content={agent.findings} />
            </article>
          ))}
        </div>
      </section>

      <section className="result-card">
        <CardTitle icon={<CheckCircle2 size={20} />} title="Analysis Summary" />
        <pre className="summary-text">{response.summary.trim()}</pre>
      </section>
    </div>
  );
}

function CardTitle({ icon, title }: { icon: React.ReactNode; title: string }) {
  return <div className="card-title">{icon}<h2>{title}</h2></div>;
}