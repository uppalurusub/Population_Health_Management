from datetime import datetime
import time


from app.config.settings import (
    settings,
    usage_capture,
    INPUT_PRICE_PER_1M,
    OUTPUT_PRICE_PER_1M,
)


logger = settings.get_logger()

from app.implementation.population_impl import (
    PopulationHealthImplementation
)

from app.schemas.request_model import PatientRequest
from app.memory.population_memory import population_memory

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
            start_time = datetime.now()
            start_ts = time.perf_counter()

            logger.info(
                f"Stratification request received "
                f"for patient={request.patient_id}"
            )

            with mlflow.start_run(
                run_name=
                f"Population_Health_Management_Stratify_Patient_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            ):
                mlflow.log_param("start_time", start_time.isoformat())
                mlflow.set_tag("source", "FastAPI")
                mlflow.set_tag("endpoint", "monitoring/analyze")
                mlflow.set_tag("llm_provider", "OpenRouter")

                

                with usage_capture() as usage:
                    response = await self.impl.stratify_patient(
                        request
                    )

                execution_time = time.perf_counter() - start_ts
                usage_values = usage.as_dict()

                # Log configuration and actual usage separately.
                mlflow.log_param("llm_model", usage_values["model"])
                mlflow.log_param(
                    "input_price_per_1m_usd", INPUT_PRICE_PER_1M
                )
                mlflow.log_param(
                    "output_price_per_1m_usd", OUTPUT_PRICE_PER_1M
                )
                mlflow.log_param("input", request)
                mlflow.log_param("output", response)
                mlflow.log_param("execution_time", execution_time)

                metric_names = (
                    "input_tokens",
                    "output_tokens",
                    "total_tokens",
                    "input_cost_usd",
                    "output_cost_usd",
                    "total_cost_usd",
                    "llm_call_count",
                    "usage_reported_call_count",
                )
                for metric_name in metric_names:
                    mlflow.log_metric(
                        metric_name,
                        float(usage_values[metric_name])
                    )

                mlflow.log_metric(
                    "execution_time_seconds",
                    round(execution_time, 4)
                )

                mlflow.set_tag("llm_usage_source", usage_values["source"])
                mlflow.log_param("end_time", datetime.now().isoformat())

                logger.info(
                    "LLM usage captured: "
                    f"model={usage_values['model']}, "
                    f"input_tokens={usage_values['input_tokens']}, "
                    f"output_tokens={usage_values['output_tokens']}, "
                    f"total_tokens={usage_values['total_tokens']}, "
                    f"input_cost_usd={usage_values['input_cost_usd']:.15f}, "
                    f"output_cost_usd={usage_values['output_cost_usd']:.15f}, "
                    f"total_cost_usd={usage_values['total_cost_usd']:.15f}, "
                    f"llm_call_count={usage_values['llm_call_count']}, "
                    f"usage_reported_call_count="
                    f"{usage_values['usage_reported_call_count']}"
                )

                if usage_values["usage_reported_call_count"] == 0:
                    logger.warning(
                        "No token usage was reported by the AutoGen model "
                        "client. Check that MonitoringImplementation uses "
                        "settings.get_model_client() and that the provider "
                        "returns usage metadata."
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