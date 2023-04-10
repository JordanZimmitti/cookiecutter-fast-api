from fastapi import APIRouter

from {{cookiecutter.package_name}}.api.resources.rsrc_health import HealthModel, SettingsModel
from {{cookiecutter.package_name}}.core.settings import settings

# Creates the sub API router instance
router = APIRouter()


@router.get("/check", response_model=HealthModel)
async def get_health_check_endpoint() -> HealthModel:
    """
    Endpoint that checks the health of the {{cookiecutter.friendly_name}} server
    """

    # Returns the {{cookiecutter.friendly_name}} server status and version number to the client
    return HealthModel(status="healthy", version=settings.PROJECT_VERSION)


@router.get("/settings", response_model=SettingsModel)
async def get_health_settings_endpoint() -> SettingsModel:
    """
    Endpoint that gets the {{cookiecutter.friendly_name}} server environment settings
    """

    # Returns the {{cookiecutter.friendly_name}} server environment settings to the client
    return SettingsModel(settings=settings.dict_safe())
