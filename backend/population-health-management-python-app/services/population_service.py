from utils.logger import logger

from implementation.population_impl import (
    PopulationHealthImplementation
)

from models.request_model import PatientRequest
from memory.population_memory import population_memory

import mlflow
from datetime import datetime

mlflow.set_tracking_uri(
    "http://localhost:5000"
)

mlflow.set_experiment(
    "Population_Health_Management_Interface"
)

class PopulationHealthService:

    def __init__(self):

        logger.info(
            "Initializing PopulationHealthService"
        )

        self.impl = PopulationHealthImplementation()

        logger.success(
            "PopulationHealthService initialized successfully"
        )

    async def stratify_patient(
        self,
        request: PatientRequest
    ):
        """
        Perform patient stratification
        """

        try:

            logger.info(
                f"Stratification request received "
                f"for patient={request.patient_id}"
            )

            with mlflow.start_run(
                run_name=
                f"Population_Health_Management_Stratify_Patient_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            ):
                mlflow.log_param(
                    "input_text",
                    request
                )

                response = await self.impl.stratify_patient(
                    request
                )

                mlflow.log_param(
                    "response",
                    response
                )

                mlflow.set_tag(
                    "source",
                    "FastAPI"
                )

                mlflow.set_tag(
                    "endpoint",
                    "population-health/stratify"
                )

            logger.success(
                f"Stratification completed "
                f"for patient={request.patient_id}"
            )

            return response

        except Exception as ex:

            logger.exception(
                f"Error during stratification: {str(ex)}"
            )

            raise ex

    async def get_patient_history(
        self,
        patient_id: str
    ):
        """
        Get patient historical analyses
        """

        try:

            logger.info(
                f"Fetching patient history "
                f"for patient={patient_id}"
            )

            history = await self.impl.get_patient_history(
                patient_id
            )

            logger.success(
                f"Patient history retrieved "
                f"for patient={patient_id}"
            )

            return {
                "success": True,
                "patient_id": patient_id,
                "history": history,
                "count": len(history)
            }

        except Exception as ex:

            logger.exception(
                f"Error fetching history: {str(ex)}"
            )

            return {
                "success": False,
                "patient_id": patient_id,
                "history": [],
                "count": 0,
                "message": str(ex)
            }

    async def get_population_summary(
        self
    ):
        """
        Population-level analytics
        """

        try:

            logger.info(
                "Generating population summary"
            )

            summary = await self.impl.get_population_summary()

            logger.success(
                "Population summary generated"
            )

            return {
                "success": True,
                "data": summary
            }

        except Exception as ex:

            logger.exception(
                f"Population summary failed: {str(ex)}"
            )

            return {
                "success": False,
                "message": str(ex)
            }

    async def get_high_risk_patients(
        self,
        threshold: float = 0.7
    ):
        """
        Get high-risk patients above threshold
        """

        try:

            logger.info(
                f"Fetching high-risk patients "
                f"threshold={threshold}"
            )

            patients = population_memory.get_high_risk_patients(
                threshold
            )

            logger.success(
                f"Retrieved {len(patients)} "
                f"high-risk patients"
            )

            return {
                "success": True,
                "count": len(patients),
                "patients": patients
            }

        except Exception as ex:

            logger.exception(
                f"Failed to retrieve high-risk patients: "
                f"{str(ex)}"
            )

            return {
                "success": False,
                "patients": [],
                "count": 0,
                "message": str(ex)
            }

    async def get_segment_distribution(
        self
    ):
        """
        Get population segment distribution
        """

        try:

            logger.info(
                "Fetching segment distribution"
            )

            distribution = (
                population_memory.get_segment_distribution()
            )

            logger.success(
                "Segment distribution generated"
            )

            return {
                "success": True,
                "distribution": distribution
            }

        except Exception as ex:

            logger.exception(
                f"Segment distribution failed: {str(ex)}"
            )

            return {
                "success": False,
                "distribution": {},
                "message": str(ex)
            }

    async def clear_memory(
        self
    ):
        """
        Clear population memory
        """

        try:

            logger.warning(
                "Clearing population memory"
            )

            self.impl.population_memory.clear_memory()

            logger.success(
                "Population memory cleared"
            )

            return {
                "success": True,
                "message": "Population memory cleared successfully"
            }

        except Exception as ex:

            logger.exception(
                f"Memory clear failed: {str(ex)}"
            )

            return {
                "success": False,
                "message": str(ex)
            }