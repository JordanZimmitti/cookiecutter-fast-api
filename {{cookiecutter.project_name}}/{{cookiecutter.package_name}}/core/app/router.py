from fastapi import APIRouter

from {{cookiecutter.package_name}}.api.routes import health

# Creates the main API router instance
api_router = APIRouter()

# Include /health endpoints into the main API router
api_router.include_router(health.router, tags=["Health"], prefix="/v1/health")
