from contextlib import asynccontextmanager

from fastapi import FastAPI
from utils.logger import logger

from routers.population_router import router as population_router


# --------------------------------------------------
# Application Lifecycle Events
# --------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info(
        "Starting Population Health Management API..."
    )

    logger.success(
        "Population Health Management API started successfully"
    )

    yield

    logger.warning(
        "Shutting down Population Health Management API..."
    )

    logger.success(
        "Population Health Management API shutdown completed"
    )


# --------------------------------------------------
# FastAPI App
# --------------------------------------------------

app = FastAPI(
    title="Population Health Management System",
    description="AutoGen 0.7.5 Multi-Agent Population Health Management API",
    version="1.0.0",
    lifespan=lifespan
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Register Routers
# --------------------------------------------------

app.include_router(
    population_router
)

# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get(
    "/",
    tags=["Root"]
)
async def root():

    logger.info(
        "Root endpoint accessed"
    )

    return {
        "application":
            "Population Health Management System",
        "version":
            "1.0.0",
        "status":
            "running"
    }


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get(
    "/health",
    tags=["Health"]
)
async def health_check():

    logger.info(
        "Health check endpoint accessed"
    )

    return {
        "status": "healthy",
        "service": "Population Health Management API"
    }


# --------------------------------------------------
# Swagger Info Endpoint
# --------------------------------------------------

@app.get(
    "/info",
    tags=["Info"]
)
async def api_info():

    return {
        "application":
            "Population Health Management System",

        "version":
            "1.0.0",

        "framework":
            "FastAPI",

        "agent_framework":
            "AutoGen 0.7.5",

        "architecture":
            "Router -> Service -> Implementation -> Agents -> Memory"
    }


