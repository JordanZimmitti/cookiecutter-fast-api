from starlette.testclient import TestClient

from {{cookiecutter.package_name}}.api.resources.rsrc_health import Health, Settings
from {{cookiecutter.package_name}}.core.settings import settings


def test_get_health_check_endpoint(client: TestClient):
    """
    Tests the get_health_check_endpoint function for completion. The get_health_check_endpoint
    function should return valid Health data without any errors

    :param client: A test client for hitting {{cookiecutter.friendly_name}} http requests
    """

    # Hits the endpoint and gets the response
    endpoint = f"{settings.API_PREFIX}/v1/health/check"
    response = client.get(endpoint)

    # Checks whether the response was retrieved correctly
    assert response.status_code == 200

    # Gets the health data
    raw_data = response.json()
    health_data = Health(**raw_data)

    # Checks whether the correct health data exists
    assert health_data.version == settings.PROJECT_VERSION
    assert health_data.status == "healthy"


def test_get_health_settings_endpoint(client: TestClient):
    """
    Tests the get_health_settings_endpoint function for completion. The
    get_health_settings_endpoint function should return valid Settings
    data without any errors

    :param client: A test client for hitting {{cookiecutter.friendly_name}} http requests
    """

    # Hits the endpoint and gets the response
    endpoint = f"{settings.API_PREFIX}/v1/health/settings"
    response = client.get(endpoint)

    # Checks whether the response was retrieved correctly
    assert response.status_code == 200

    # Gets the health data
    raw_data = response.json()
    settings_data = Settings(**raw_data)

    # Checks whether the correct settings data exists
    assert "{{cookiecutter.friendly_name}}" in settings_data.settings.get("PROJECT_NAME")
