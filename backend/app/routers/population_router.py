from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    status
)

from app.config.settings import settings
logger = settings.get_logger()

from app.services.population_service import (
    PopulationHealthService
)

from app.schemas.request_model import (
    PatientRequest
)

from app.schemas.response_model import (
    PopulationHealthResponse
)

router = APIRouter(
    prefix="/population-health",
    tags=["Population Health Management"]
)

service = PopulationHealthService()


@router.post(
    "/stratify",
    response_model=PopulationHealthResponse,
    status_code=status.HTTP_200_OK
)
async def stratify_patient(
    request: PatientRequest
):
    """
    Perform patient stratification and risk assessment.
    """

    try:

        logger.info(
            f"Received stratification request "
            f"for patient={request.patient_id}"
        )

        response = await service.stratify_patient(
            request
        )

        logger.success(
            f"Stratification completed "
            f"for patient={request.patient_id}"
        )

        return response

    except Exception as ex:

        logger.exception(
            f"Stratification failed: {str(ex)}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )


@router.get(
    "/history/{patient_id}",
    status_code=status.HTTP_200_OK
)
async def get_patient_history(
    patient_id: str
):
    """
    Get patient analysis history.
    """

    try:

        logger.info(
            f"Fetching history "
            f"for patient={patient_id}"
        )

        result = await service.get_patient_history(
            patient_id
        )

        return result

    except Exception as ex:

        logger.exception(
            f"History retrieval failed: {str(ex)}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )


@router.get(
    "/population-summary",
    status_code=status.HTTP_200_OK
)
async def get_population_summary():
    """
    Population level analytics summary.
    """

    try:

        logger.info(
            "Generating population summary"
        )

        result = await service.get_population_summary()

        return result

    except Exception as ex:

        logger.exception(
            f"Population summary failed: {str(ex)}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )


@router.get(
    "/high-risk-patients",
    status_code=status.HTTP_200_OK
)
async def get_high_risk_patients(
    threshold: float = Query(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Risk score threshold"
    )
):
    """
    Get high-risk patient population.
    """

    try:

        logger.info(
            f"Fetching high-risk patients "
            f"with threshold={threshold}"
        )

        result = await service.get_high_risk_patients(
            threshold
        )

        return result

    except Exception as ex:

        logger.exception(
            f"High-risk retrieval failed: {str(ex)}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )


@router.get(
    "/segment-distribution",
    status_code=status.HTTP_200_OK
)
async def get_segment_distribution():
    """
    Get population segment distribution.
    """

    try:

        logger.info(
            "Fetching segment distribution"
        )

        result = await service.get_segment_distribution()

        return result

    except Exception as ex:

        logger.exception(
            f"Segment distribution failed: {str(ex)}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )




@router.get(
    "/health",
    status_code=status.HTTP_200_OK
)
async def health_check():
    """
    Health check endpoint.
    """

    logger.info(
        "Population Health API health check"
    )

    return {
        "status": "healthy",
        "service": "Population Health Management System"
    }