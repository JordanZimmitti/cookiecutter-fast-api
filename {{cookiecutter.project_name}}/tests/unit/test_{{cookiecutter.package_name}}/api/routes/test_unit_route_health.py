from unittest.mock import MagicMock

from pytest import mark

from {{cookiecutter.package_name}}.api.resources.rsrc_health import HealthModel, SettingsModel
from {{cookiecutter.package_name}}.api.routes import health
from {{cookiecutter.package_name}}.api.routes.health import get_health_check_endpoint, get_health_settings_endpoint


@mark.asyncio
async def test_get_health_check_endpoint(mocker):
    """
    Tests the get_health_check_endpoint function for completion. The get_health_check_endpoint
    function should return a valid HealthModel instance without any errors

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mocks and overrides the health-model class
    health_model_mock = MagicMock(spec=HealthModel)
    mocker.patch.object(health, "HealthModel", health_model_mock)

    # Checks whether a health-model instance was instantiated
    await get_health_check_endpoint()
    assert health_model_mock.called


@mark.asyncio
async def test_get_health_settings_endpoint(mocker):
    """
    Tests the get_health_settings_endpoint function for completion. The get_health_settings_endpoint
    function should return a valid SettingsModel instance without any errors

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mocks and overrides the settings-model class
    settings_model_mock = MagicMock(spec=SettingsModel)
    mocker.patch.object(health, "SettingsModel", settings_model_mock)

    # Checks whether a settings-model instance was instantiated
    await get_health_settings_endpoint()
    assert settings_model_mock.called
