from fastapi import APIRouter

from {{cookiecutter.package_name}}.api.resources.rsrc_health import Health, Settings
from {{cookiecutter.package_name}}.core.settings import settings

# Creates the sub API router instance
router = APIRouter()


@router.get("/check", response_model=Health)
async def get_health_check_endpoint() -> Health:
    """
    Endpoint that checks the health of the {{cookiecutter.friendly_name}} server
    """

    # Returns the {{cookiecutter.friendly_name}} server status and version number to the client
    return Health(status="healthy", version=settings.PROJECT_VERSION)


@router.get("/settings", response_model=Settings)
async def get_health_settings_endpoint() -> Settings:
    """
    Endpoint that gets the {{cookiecutter.friendly_name}} server environment settings
    """

    # Returns the {{cookiecutter.friendly_name}} server environment settings to the client
    return Settings(settings=settings.dict_safe())
