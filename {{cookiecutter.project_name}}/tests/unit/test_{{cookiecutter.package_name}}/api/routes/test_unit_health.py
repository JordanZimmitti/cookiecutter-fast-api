from unittest.mock import MagicMock

from pytest import mark

from {{cookiecutter.package_name}}.api.resources.rsrc_health import Health, Settings
from {{cookiecutter.package_name}}.api.routes import health
from {{cookiecutter.package_name}}.api.routes.health import get_health_check_endpoint, get_health_settings_endpoint


@mark.asyncio
async def test_get_health_check_endpoint(mocker):
    """
    Tests the get_health_check_endpoint function for completion. The get_health_check_endpoint
    function should return a valid Health instance without any errors

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mocks and overrides the health class
    health_mock = MagicMock(spec=Health)
    mocker.patch.object(health, "Health", health_mock)

    # Checks whether a health instance was instantiated
    await get_health_check_endpoint()
    assert health_mock.called


@mark.asyncio
async def test_get_health_settings_endpoint(mocker):
    """
    Tests the get_health_settings_endpoint function for completion. The
    get_health_settings_endpoint function should return a valid Settings
    instance without any errors

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mocks and overrides the settings class
    settings_mock = MagicMock(spec=Settings)
    mocker.patch.object(health, "Settings", settings_mock)

    # Checks whether a settings instance was instantiated
    await get_health_settings_endpoint()
    assert settings_mock.called
