from pytest import mark

from {{cookiecutter.package_name}}.api.resources.rsrc_health import Health, Settings
from {{cookiecutter.package_name}}.api.routes import health
from {{cookiecutter.package_name}}.api.routes.health import get_health_check_endpoint, get_health_settings_endpoint
from {{cookiecutter.package_name}}.core.settings import settings


@mark.asyncio
async def test_get_health_check_endpoint(mocker):
    """
    Tests the get_health_check_endpoint function for completion. The get_health_check_endpoint
    function should return valid Health data without any errors

    :param mocker: Fixture to mock specific functions for testing
    """

    # Creates a mock health object to return
    health_obj = Health(status="healthy", version="0.0.0")
    mocker.patch.object(health, "Health", return_value=health_obj)

    # Checks whether the correct health data exists
    return_data = await get_health_check_endpoint()
    assert return_data.version == "0.0.0"
    assert return_data.status == "healthy"


@mark.asyncio
async def test_get_health_settings_endpoint(mocker):
    """
    Tests the get_health_settings_endpoint function for completion. The
    get_health_settings_endpoint function should return valid Settings
    data without any errors

    :param mocker: Fixture to mock specific functions for testing
    """

    # Creates a mock settings object to return
    settings_obj = Settings(settings=settings.dict_safe())
    mocker.patch.object(health, "Settings", return_value=settings_obj)

    # Checks whether the correct settings data exists
    return_data = await get_health_settings_endpoint()
    assert "{{cookiecutter.friendly_name}}" in return_data.settings.get("PROJECT_NAME")
