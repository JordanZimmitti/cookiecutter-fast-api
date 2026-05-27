from inspect import unwrap
from unittest.mock import MagicMock

from pydantic import SecretStr, ValidationInfo

from {{cookiecutter.package_name}}.core.settings import Settings, settings


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


def test_create_api_db_migrations_connection_string_no_user_or_password():
    """
    Tests the create_api_db_migrations_connection_string function when no migration
    user or password is provided. The create_api_db_migrations_connection_string
    function should return None without any errors
    """

    # Mocks the validation-info class
    values_mock = MagicMock(spec=ValidationInfo)
    values_mock.data = {"API_DB_USER_MIGRATIONS": None, "API_DB_PASSWORD_MIGRATIONS": None}

    # Invokes the create_api_db_migrations_connection_string function
    connection_string = unwrap(Settings.create_api_db_migrations_connection_string)(
        _=None, values=values_mock
    )

    # Checks whether the connection string was retrieved correctly
    assert connection_string is None


def test_create_api_db_migrations_connection_string_user_or_password():
    """
    Tests the create_api_db_migrations_connection_string function when a migration
    user or password is provided. The create_api_db_migrations_connection_string
    function should return the string without any errors
    """

    # Mocks the validation-info class
    values_mock = MagicMock(spec=ValidationInfo)
    values_mock.data = {
        "API_DB_DRIVER": SecretStr("api-db-driver"),
        "API_DB_HOST": SecretStr("api-db-host"),
        "API_DB_PORT": SecretStr("1234"),
        "API_DB_DB": SecretStr("api-db-name"),
        "API_DB_USER_MIGRATIONS": SecretStr("api-db-user-migrations"),
        "API_DB_PASSWORD_MIGRATIONS": SecretStr("api-db-password-migrations"),
    }

    # Invokes the create_api_db_migrations_connection_string function
    connection_string = unwrap(Settings.create_api_db_migrations_connection_string)(
        _=None, values=values_mock
    )

    # Checks whether the connection string was retrieved correctly
    assert connection_string == (
        "api-db-driver://api-db-user-migrations:api-db-password-migrations@api-db-host:1234/api-db-name"
    )
