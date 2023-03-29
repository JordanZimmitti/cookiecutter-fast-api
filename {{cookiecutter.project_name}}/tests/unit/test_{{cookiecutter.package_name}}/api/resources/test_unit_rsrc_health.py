from {{cookiecutter.package_name}}.api.resources.rsrc_health import HealthModel, SettingsModel


def test_health_model():
    """
    Tests the health pydantic model for completion. The health pydantic model
    should instantiate a new health instance without any errors
    """

    # Mocks the health data
    health_data = {"status": "status", "version": "version"}

    # Checks whether the health model was instantiated correctly
    health_model = HealthModel(**health_data)
    assert health_model.status == "status"
    assert health_model.version == "version"


def test_settings_model():
    """
    Tests the settings pydantic model for completion. The settings pydantic model
    should instantiate a new settings instance without any errors
    """

    # Mocks the settings data
    settings_data = {"settings": {"setting-key": "setting-value"}}

    # Checks whether the settings model was instantiated correctly
    settings_model = SettingsModel(**settings_data)
    assert settings_model.settings == {"setting-key": "setting-value"}
