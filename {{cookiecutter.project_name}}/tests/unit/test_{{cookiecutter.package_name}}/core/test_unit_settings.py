from {{cookiecutter.package_name}}.core.settings import settings


def test_settings_dict_safe():
    """
    Tests the settings class when environment settings should be shown.
    The settings class should return the environment setting without
    showing the protected settings in clear text
    """

    # Gets the {{cookiecutter.friendly_name}} environment settings hiding protected settings
    protected_settings = settings.dict_safe()

    # Checks whether the secret key was hidden
    secret_key = protected_settings.get("API_DB_PASSWORD")
    assert str(secret_key) == "**********"
