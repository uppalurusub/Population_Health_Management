import json
from datetime import datetime

from app.config.settings import settings
logger = settings.get_logger()

from app.agents.population_agents import population_agents
from app.memory.population_memory import population_memory

from app.schemas.request_model import PatientRequest

from app.schemas.response_model import (
    PopulationHealthResponse,
    PopulationSegment,
    RiskAssessment,
    CareGap,
    Intervention,
    AgentFinding
)


class PopulationHealthImplementation:

    def __init__(self):

        logger.info(
            "Initializing PopulationHealthImplementation"
        )

        self.data_agent = (
            population_agents.get_data_agent()
        )

        self.segmentation_agent = (
            population_agents.get_segmentation_agent()
        )

        self.risk_agent = (
            population_agents.get_risk_agent()
        )

        self.intervention_agent = (
            population_agents.get_intervention_agent()
        )

        logger.success(
            "PopulationHealthImplementation initialized"
        )

    async def stratify_patient(
        self,
        request: PatientRequest
    ) -> PopulationHealthResponse:

        try:

            logger.info(
                f"Starting population analysis "
                f"for patient={request.patient_id}"
            )

            patient_data = json.dumps(
                request.model_dump(),
                indent=2
            )

            # ==================================================
            # Data Agent
            # ==================================================

            logger.info(
                "Executing DataAgent"
            )

            data_result = await self.data_agent.run(
                task=f"""
Analyze the following patient data.

Return:
1. Clinical Summary
2. Chronic Conditions
3. Utilization Findings

Patient:

{patient_data}
"""
            )

            data_output = (
                data_result.messages[-1].content
            )

            logger.success(
                "DataAgent completed"
            )

            # ==================================================
            # Segmentation Agent
            # ==================================================

            logger.info(
                "Executing SegmentationAgent"
            )

            segmentation_result = (
                await self.segmentation_agent.run(
                    task=f"""
Patient Analysis:

{data_output}

Classify into one population segment.

Return:

Segment Name:
Reason:
"""
                )
            )

            segment_output = (
                segmentation_result.messages[-1].content
            )

            logger.success(
                "SegmentationAgent completed"
            )

            # ==================================================
            # Risk Agent
            # ==================================================

            logger.info(
                "Executing RiskAgent"
            )

            risk_result = await self.risk_agent.run(
                task=f"""
Patient Data:

{patient_data}

Segment:

{segment_output}

Return JSON:

{{
  "risk_level":"",
  "risk_score":0.0,
  "readmission_risk":0.0,
  "mortality_risk":0.0,
  "cost_risk":0.0
}}
"""
            )

            risk_output = (
                risk_result.messages[-1].content
            )

            logger.success(
                "RiskAgent completed"
            )

            try:

                risk_json = json.loads(
                    risk_output
                )

            except Exception:

                logger.warning(
                    "RiskAgent returned non-JSON. "
                    "Using default values."
                )

                risk_json = {
                    "risk_level": "Moderate",
                    "risk_score": 0.50,
                    "readmission_risk": 0.50,
                    "mortality_risk": 0.25,
                    "cost_risk": 0.40
                }

            # ==================================================
            # Intervention Agent
            # ==================================================

            logger.info(
                "Executing InterventionAgent"
            )

            intervention_result = (
                await self.intervention_agent.run(
                    task=f"""
Patient Data:

{patient_data}

Risk Assessment:

{risk_json}

Provide:

1. Care Gaps
2. Recommended Interventions
3. Priority Levels
"""
                )
            )

            intervention_output = (
                intervention_result.messages[-1].content
            )

            logger.success(
                "InterventionAgent completed"
            )

            # ==================================================
            # Build Response
            # ==================================================

            response = PopulationHealthResponse(

                success=True,

                patient_id=request.patient_id,
                patient_name=request.patient_name,

                population_segment=PopulationSegment(
                    segment_name=segment_output.split(
                        "\n"
                    )[0],
                    segment_description=segment_output
                ),

                risk_assessment=RiskAssessment(
                    risk_level=risk_json.get(
                        "risk_level",
                        "Moderate"
                    ),
                    risk_score=risk_json.get(
                        "risk_score",
                        0.50
                    ),
                    readmission_risk=risk_json.get(
                        "readmission_risk",
                        0.50
                    ),
                    mortality_risk=risk_json.get(
                        "mortality_risk",
                        0.25
                    ),
                    cost_risk=risk_json.get(
                        "cost_risk",
                        0.40
                    )
                ),

                care_gaps=[
                    CareGap(
                        category="General",
                        description="Review preventive care needs",
                        priority="Medium"
                    )
                ],

                interventions=[
                    Intervention(
                        intervention_type="Population Health",
                        recommendation=intervention_output,
                        priority="High"
                    )
                ],

                agent_findings=[

                    AgentFinding(
                        agent_name="DataAgent",
                        findings=data_output
                    ),

                    AgentFinding(
                        agent_name="SegmentationAgent",
                        findings=segment_output
                    ),

                    AgentFinding(
                        agent_name="RiskAgent",
                        findings=risk_output
                    ),

                    AgentFinding(
                        agent_name="InterventionAgent",
                        findings=intervention_output
                    )

                ],

                summary=f"""
Population Health Analysis Completed

Segment:
{segment_output}

Risk:
{risk_json.get('risk_level')}

Risk Score:
{risk_json.get('risk_score')}
""",

                message="Population health analysis completed successfully."
            )

            # ==================================================
            # Save To Memory
            # ==================================================

            logger.info(
                "Saving patient analysis to memory"
            )

            population_memory.save_patient_analysis(
                patient_id=request.patient_id,
                analysis=response.model_dump()
            )

            logger.success(
                f"Patient analysis stored "
                f"for {request.patient_id}"
            )

            return response

        except Exception as ex:

            logger.exception(
                f"Population analysis failed: {str(ex)}"
            )

            return PopulationHealthResponse(
                success=False,
                patient_id=request.patient_id,
                patient_name=request.patient_name,

                population_segment=PopulationSegment(
                    segment_name="Unknown",
                    segment_description="Analysis Failed"
                ),

                risk_assessment=RiskAssessment(
                    risk_level="Unknown",
                    risk_score=0.0
                ),

                care_gaps=[],
                interventions=[],
                agent_findings=[],

                summary="Population health analysis failed.",

                message=str(ex)
            )

    async def get_patient_history(
        self,
        patient_id: str
    ):

        logger.info(
            f"Fetching patient history "
            f"for {patient_id}"
        )

        return population_memory.get_patient_history(
            patient_id
        )

    async def get_population_summary(
        self
    ):

        logger.info(
            "Generating population summary"
        )

        return {
            "population_size":
                population_memory.get_population_size(),

            "high_risk_patients":
                population_memory.get_high_risk_patients(),

            "segment_distribution":
                population_memory.get_segment_distribution(),

            "generated_at":
                datetime.utcnow().isoformat()
        }