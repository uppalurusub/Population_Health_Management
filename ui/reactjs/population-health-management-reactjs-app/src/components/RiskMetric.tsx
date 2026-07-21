interface Props {
  label: string;
  value: number | null;
}

export default function RiskMetric({ label, value }: Props) {
  const percentage = value == null ? null : Math.round(value * 100);
  return (
    <div className="metric-card">
      <span>{label}</span>
      <strong>{percentage == null ? "N/A" : `${percentage}%`}</strong>
      <div className="progress-track">
        <div className="progress-value" style={{ width: `${percentage ?? 0}%` }} />
      </div>
    </div>
  );
}