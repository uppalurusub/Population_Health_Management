import os

from dotenv import load_dotenv

from app.config.settings import settings
logger = settings.get_logger()

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()


class PopulationAgents:

    def __init__(self):

        logger.info(
            "Initializing Population Health Agents..."
        )

        self.model_client = settings.get_model_client()

        logger.success(
            "{model} Model Client initialized successfully"
        )

        self.data_agent = AssistantAgent(
            name="DataAgent",
            model_client=self.model_client,
            system_message="""
You are a Healthcare Data Analysis Agent.

Responsibilities:
1. Analyze patient demographics.
2. Analyze diagnoses and medications.
3. Analyze vitals and laboratory results.
4. Identify chronic conditions.
5. Identify utilization patterns.

Return concise clinical insights.
"""
        )

        logger.success(
            "DataAgent initialized"
        )

        self.segmentation_agent = AssistantAgent(
            name="SegmentationAgent",
            model_client=self.model_client,
            system_message="""
You are a Population Segmentation Agent.

Classify patient into one segment:

1. Healthy Population
2. Preventive Care Population
3. Chronic Disease Population
4. High Risk Population
5. Frequent Utilizer Population
6. Elderly Care Population

Return:

Segment Name
Reasoning
"""
        )

        logger.success(
            "SegmentationAgent initialized"
        )

        self.risk_agent = AssistantAgent(
            name="RiskAgent",
            model_client=self.model_client,
            system_message="""
You are a Healthcare Risk Prediction Agent.

Analyze:

- Readmission Risk
- Mortality Risk
- Cost Risk
- Chronic Disease Progression Risk

Return JSON:

{
  "risk_level": "",
  "risk_score": 0.0,
  "readmission_risk": 0.0,
  "mortality_risk": 0.0,
  "cost_risk": 0.0
}
"""
        )

        logger.success(
            "RiskAgent initialized"
        )

        self.intervention_agent = AssistantAgent(
            name="InterventionAgent",
            model_client=self.model_client,
            system_message="""
You are a Population Health Intervention Agent.

Recommend:

1. Preventive interventions
2. Chronic disease interventions
3. Lifestyle modifications
4. Care management programs
5. Remote monitoring recommendations

Return structured recommendations.
"""
        )

        logger.success(
            "InterventionAgent initialized"
        )

        logger.success(
            "All Population Health Agents initialized successfully"
        )

    def get_data_agent(self):
        return self.data_agent

    def get_segmentation_agent(self):
        return self.segmentation_agent

    def get_risk_agent(self):
        return self.risk_agent

    def get_intervention_agent(self):
        return self.intervention_agent


population_agents = PopulationAgents()