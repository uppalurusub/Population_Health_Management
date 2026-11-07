from typing import Dict, List, Optional
from datetime import datetime
from app.config.settings import settings
logger = settings.get_logger()


class PopulationMemory:

    def __init__(self):
        self.patient_memory: Dict = {}

        logger.info("PopulationMemory initialized")

    def save_patient_analysis(
        self,
        patient_id: str,
        analysis: Dict
    ) -> None:
        """
        Save latest analysis for a patient
        """

        logger.info(
            f"Saving analysis for patient: {patient_id}"
        )

        if patient_id not in self.patient_memory:
            self.patient_memory[patient_id] = []

        self.patient_memory[patient_id].append(
            {
                "timestamp": datetime.utcnow().isoformat(),
                "analysis": analysis
            }
        )

        logger.success(
            f"Analysis saved for patient: {patient_id}"
        )

    def get_patient_history(
        self,
        patient_id: str
    ) -> List[Dict]:

        logger.info(
            f"Fetching history for patient: {patient_id}"
        )

        return self.patient_memory.get(
            patient_id,
            []
        )

    def get_latest_analysis(
        self,
        patient_id: str
    ) -> Optional[Dict]:

        logger.info(
            f"Fetching latest analysis for patient: {patient_id}"
        )

        history = self.patient_memory.get(
            patient_id,
            []
        )

        if not history:
            logger.warning(
                f"No history found for patient: {patient_id}"
            )
            return None

        return history[-1]

    def update_risk_score(
        self,
        patient_id: str,
        risk_score: float
    ) -> bool:

        history = self.patient_memory.get(
            patient_id,
            []
        )

        if not history:
            logger.warning(
                f"No patient found: {patient_id}"
            )
            return False

        history[-1]["analysis"]["risk_score"] = risk_score

        logger.success(
            f"Risk score updated for patient: {patient_id}"
        )

        return True

    def get_population_size(self) -> int:

        size = len(self.patient_memory)

        logger.info(
            f"Population size: {size}"
        )

        return size

    def get_high_risk_patients(
        self,
        threshold: float = 0.7
    ) -> List[Dict]:

        logger.info(
            f"Retrieving patients with risk score >= {threshold}"
        )

        high_risk = []

        for patient_id, records in self.patient_memory.items():

            if not records:
                continue

            latest = records[-1]["analysis"]

            risk_score = latest.get(
                "risk_score",
                0
            )

            if risk_score >= threshold:
                high_risk.append(
                    {
                        "patient_id": patient_id,
                        "risk_score": risk_score,
                        "segment": latest.get(
                            "segment",
                            "Unknown"
                        )
                    }
                )

        logger.success(
            f"Found {len(high_risk)} high-risk patients"
        )

        return high_risk

    def get_segment_distribution(self) -> Dict:

        logger.info(
            "Calculating population segment distribution"
        )

        distribution = {}

        for _, records in self.patient_memory.items():

            if not records:
                continue

            segment = (
                records[-1]["analysis"]
                .get("segment", "Unknown")
            )

            distribution[segment] = (
                distribution.get(segment, 0) + 1
            )

        logger.success(
            "Segment distribution calculated"
        )

        return distribution

    def clear_memory(self) -> None:

        logger.warning(
            "Clearing Population Memory"
        )

        self.patient_memory.clear()

        logger.success(
            "Population Memory cleared"
        )


population_memory = PopulationMemory()