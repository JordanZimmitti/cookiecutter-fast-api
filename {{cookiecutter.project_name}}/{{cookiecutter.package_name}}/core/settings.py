from copy import deepcopy
from dataclasses import field
from pathlib import Path
from typing import Any, Dict, List, Literal, cast
from urllib.parse import quote

from pydantic import SecretStr, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # The name of the host the project is running on
    HOSTNAME: str = "localhost"

    # The name of the project
    PROJECT_NAME: str = "{{cookiecutter.friendly_name}}"

    # The description of the project
    PROJECT_DESCRIPTION: str = "{{cookiecutter.project_description}}"

    # The API version of the project
    PROJECT_VERSION: str = "local"

    # The Open API version to use
    OPENAPI_API_VERSION: str = "3.1.1"

    # The namespace that the API can be accessed from
    NAMESPACE: str = "http://localhost"

    # The API prefix
    API_PREFIX: str = "/api"

    # The open-api swagger documentation url
    DOCS_URL: str = "/api/docs"

    # The address and port that the api can be accessed from
    LISTEN_ADDRESS: str = "localhost"
    LISTEN_PORT: int = 2000

    # The directory where the log files will be generated, their max size, and how many to keep
    LOG_FILE_DIRECTORY: str = "logs"
    LOG_FILE_MAX_BYTES: int = 1_048_576 * 10  # 10 MB
    LOG_FILE_BACKUP_COUNT: int = 3

    # Whether to add a color to the log line based on the log-level
    IS_SHOW_LOG_LEVEL_COLORS: bool = False

    # The log-level used when the server is running
    LOG_LEVEL: str = "INFO"

    # Whether fast-api debug tracebacks should be returned on errors
    IS_FAST_API_DEBUG: bool = False

    # Cors Origins used
    BACKEND_CORS_ORIGINS: List[str] = field(
        default_factory=lambda: [
            "http://127.0.0.1:2000",
            "http://localhost:2000",
        ]
    )

    # The minimum response size to compress using gzip
    GZIP_MINIMUM_SIZE_BYTES: int = 1000

    # The event loop implementation: [auto|asyncio|uvloop]
    UVICORN_LOOP: str = "uvloop"

    # The HTTP protocol implementation: [auto|h11|httptools]
    UVICORN_HTTP: str = "httptools"

    # The application web-interface [auto|asgi3|asgi2|wsgi]
    UVICORN_INTERFACE: str = "asgi3"

    # Number of uvicorn processes
    UVICORN_CONCURRENCY: int = 1

    # Number of threads per uvicorn process
    UVICORN_CONNECTIONS: int = 1000

    # Number of requests an uvicorn process can handle
    UVICORN_MAX_REQUESTS: int = 10000

    # A number 0...jitter to add to the max-requests
    UVICORN_MAX_REQUESTS_JITTER: int = 10000

    # The number of seconds to wait for requests on a keep-alive connection
    UVICORN_KEEP_ALIVE: int = 10  # 10 seconds

    # After receiving a restart signal, workers have this much time to finish serving requests
    UVICORN_GRACEFUL_TIMEOUT: int = 60  # 1 minute

    # Number of minutes an uvicorn process can start up for before the process is restarted
    UVICORN_TIMEOUT: int = 60  # 1 minute

    # Echo sqlalchemy logs for advanced debugging
    IS_ECHO_SQLALCHEMY_LOGS: bool = False

    # How many database connections to temporarily create when the connection pool is full
    SQLALCHEMY_MAX_OVERFLOW: int = 2

    # How many active database connections are available in the connection pool
    SQLALCHEMY_POOL_SIZE: int = 1

    # The number of seconds to wait before giving up on getting a connection from the pool
    SQLALCHEMY_POOL_TIMEOUT: int = 30

    # Recurring task period second specifications
    TASK_CLEANUP_PERIOD_SECONDS: int = 180  # three minutes

    # {{cookiecutter.friendly_name}} server redis metadata
    API_REDIS_DISPLAY_NAME: str = "{{cookiecutter.redis_cache_display_name}}"
    API_REDIS_DESCRIPTION: str = "{{cookiecutter.redis_cache_description}}"

    # {{cookiecutter.friendly_name}} server redis
    IS_API_REDIS_ENABLED: bool = False
    API_REDIS_PIPELINE_RETRY_NUMBER: int = 3
    API_REDIS_HOST: SecretStr = SecretStr("127.0.0.1")
    API_REDIS_PORT: SecretStr = SecretStr("6379")
    API_REDIS_PASSWORD: SecretStr = SecretStr("very-secure-password")
    API_REDIS_DECODE_RESPONSES: bool = True

    # {{cookiecutter.friendly_name}} server database metadata
    API_DB_DISPLAY_NAME: str = "{{cookiecutter.api_database_display_name}}"
    API_DB_DESCRIPTION: str = "{{cookiecutter.api_database_description}}"

    # {{cookiecutter.friendly_name}} server cloud database
    API_DB_CLOUD_DRIVER: SecretStr = SecretStr("asyncpg")
    API_DB_CLOUD_INSTANCE: SecretStr = SecretStr("")
    API_DB_CLOUD_IS_PRIVATE: bool = True

    # {{cookiecutter.friendly_name}} server database
    IS_API_DB_ENABLED: bool = False
    API_DB_QUERY_RETRY_NUMBER: int = 3
    API_DB_TYPE: Literal["native", "cloud"] = "native"
    API_DB_DRIVER: SecretStr = SecretStr("postgresql+asyncpg")
    API_DB_HOST: SecretStr = SecretStr("127.0.0.1")
    API_DB_PORT: SecretStr = SecretStr("5432")
    API_DB_DB: SecretStr = SecretStr("{{cookiecutter.package_name}}")
    API_DB_SCHEMA: SecretStr = SecretStr("public")
    API_DB_USER: SecretStr
    API_DB_PASSWORD: SecretStr
    API_DB_CONN_URI: SecretStr | None = None
    API_DB_USER_MIGRATIONS: SecretStr | None = None
    API_DB_PASSWORD_MIGRATIONS: SecretStr | None = None
    API_DB_CONN_URI_MIGRATIONS: SecretStr | None = None

    @field_validator("API_DB_CONN_URI", mode="before")
    def create_api_db_connection_string(cls, _, values: ValidationInfo) -> str:
        """
        Creates the api connection string based
        on a combination of other environment
        settings

        :param _: A parameter that is not used
        :param values: All available environment values in the settings class

        :return: A valid database connection string based on the environment values
        """

        # Returns the api database connection string
        data = cast(Dict[str, SecretStr], values.data)
        return cls.create_db_uri(
            data["API_DB_DRIVER"].get_secret_value(),
            quote(data["API_DB_HOST"].get_secret_value()),
            int(data["API_DB_PORT"].get_secret_value()),
            quote(data["API_DB_DB"].get_secret_value()),
            quote(data["API_DB_USER"].get_secret_value()),
            quote(data["API_DB_PASSWORD"].get_secret_value()),
        )

    @field_validator("API_DB_CONN_URI_MIGRATIONS", mode="before")
    def create_api_db_migrations_connection_string(cls, _, values: ValidationInfo) -> str | None:
        """
        Creates the api connection string based
        on a combination of other environment
        settings

        :param _: A parameter that is not used
        :param values: All available environment values in the settings class

        :return: A valid database connection string based on the environment values
        """

        # Checks whether the migration database user and password are set
        api_db_user_migrations: SecretStr | None = values.data.get("API_DB_USER_MIGRATIONS")
        api_db_password_migrations: SecretStr | None = values.data.get("API_DB_PASSWORD_MIGRATIONS")
        if not api_db_user_migrations or not api_db_password_migrations:
            return None

        # Returns the api database migrations connection string
        data = cast(Dict[str, SecretStr], values.data)
        return cls.create_db_uri(
            data["API_DB_DRIVER"].get_secret_value(),
            quote(data["API_DB_HOST"].get_secret_value()),
            int(data["API_DB_PORT"].get_secret_value()),
            quote(data["API_DB_DB"].get_secret_value()),
            quote(api_db_user_migrations.get_secret_value()),
            quote(api_db_password_migrations.get_secret_value()),
        )

    @classmethod
    def create_db_uri(
        cls, driver: str, hostname: str, port: int, database: str, username: str, password: str
    ):
        return f"{driver}://{username}:{password}@{hostname}:{port}/{database}"

    def dict_safe(self) -> Dict[str, Any]:
        """
        Function that hides protected
        environment variables

        :return: The dictionary with the protected environment settings hidden
        """

        # Creates a copy of the dictionary
        dict_copy = deepcopy(self.model_dump(mode="json"))
        return dict_copy

    model_config = SettingsConfigDict(env_file=Path(__file__).parent / "../../local/override.env")


# Instantiates the settings instance
# noinspection PyArgumentList
settings = Settings()
