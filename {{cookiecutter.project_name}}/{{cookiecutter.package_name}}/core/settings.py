from copy import deepcopy
from os.path import dirname, join
from typing import Any, Dict, List
from urllib.parse import quote

from pydantic import BaseSettings, SecretStr, validator
from pydantic.networks import AnyHttpUrl


class Settings(BaseSettings):

    # The name of the host the project is running on
    HOSTNAME: str = "localhost"

    # The name of the project
    PROJECT_NAME: str = "{{cookiecutter.friendly_name}}"

    # The description of the project
    PROJECT_DESCRIPTION: str = "{{cookiecutter.project_description}}"

    # The API version of the project
    PROJECT_VERSION: str = "0.1.0"

    # The namespace that the API can be accessed from
    NAMESPACE: str = "http://localhost"

    # The API prefix
    API_PREFIX: str = "/api"

    # The open-api swagger documentation url
    DOCS_URL: str = f"{API_PREFIX}/docs"

    # The port that the api can be accessed from
    LISTEN_PORT: int = 2000

    # The directory where the log files will be generated
    LOG_FILE_DIRECTORY: str = "logs"

    # The log-level used when the server is running
    LOG_LEVEL: str = "INFO"

    # Whether fast-api debug tracebacks should be returned on errors
    IS_FAST_API_DEBUG: bool = False

    # Cors Origins used
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        f"http://localhost:{LISTEN_PORT}",
        f"http://0.0.0.0:{LISTEN_PORT}",
        f"http://127.0.0.1:{LISTEN_PORT}",
        "http://localhost:3000",
        "http://0.0.0.0:3000",
        "http://127.0.0.1:3000",
    ]

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
    UVICORN_MAX_REQUESTS: int = 100

    # A number 0...jitter to add to the max-requests
    UVICORN_MAX_REQUESTS_JITTER: int = 100

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

    # {{cookiecutter.friendly_name}} server redis metadata
    API_REDIS_DISPLAY_NAME: str = "{{cookiecutter.redis_cache_display_name}}"
    API_REDIS_DESCRIPTION: str = "{{cookiecutter.redis_cache_description}}"

    # {{cookiecutter.friendly_name}} server redis
    IS_API_REDIS_ENABLED: bool = False
    API_REDIS_PIPELINE_RETRY_NUMBER: int = 3
    API_REDIS_HOST: SecretStr = "127.0.0.1"
    API_REDIS_PORT: SecretStr = "6379"
    API_REDIS_PASSWORD: SecretStr = "very-secure-password"
    API_REDIS_DECODE_RESPONSES: bool = True

    # {{cookiecutter.friendly_name}} server database metadata
    API_DB_DISPLAY_NAME: str = "{{cookiecutter.api_database_display_name}}"
    API_DB_DESCRIPTION: str = "{{cookiecutter.api_database_description}}"

    # {{cookiecutter.friendly_name}} server database
    IS_API_DB_ENABLED: bool = False
    API_DB_QUERY_RETRY_NUMBER: int = 3
    API_DB_DRIVER: SecretStr = "postgresql+asyncpg"
    API_DB_HOST: SecretStr = "127.0.0.1"
    API_DB_PORT: SecretStr = "5432"
    API_DB_DB: SecretStr = "{{cookiecutter.package_name}}"
    API_DB_SCHEMA: SecretStr = "public"
    API_DB_USER: SecretStr = "local_user"
    API_DB_PASSWORD: SecretStr = "very-secure-password"
    API_DB_CONN_URI: SecretStr = None

    @validator("API_DB_CONN_URI", pre=True)
    def create_api_db_connection_string(cls, _, values: Dict[str, SecretStr]) -> str:
        """
        Creates the api connection string based
        on a combination of other environment
        settings

        :param _: A parameter that is not used
        :param values: All available environment values in the settings class

        :return: A valid database connection string based on the environment values
        """

        # Returns the api database connection string
        return cls.create_db_uri(
            values.get("API_DB_DRIVER").get_secret_value(),
            quote(values.get("API_DB_HOST").get_secret_value()),
            int(values.get("API_DB_PORT").get_secret_value()),
            quote(values.get("API_DB_DB").get_secret_value()),
            quote(values.get("API_DB_USER").get_secret_value()),
            quote(values.get("API_DB_PASSWORD").get_secret_value()),
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
        dict_copy = deepcopy(self.dict())

        # Returns the dictionary with the protected environment settings hidden
        protected_keys = ["API_DB_CONN_STR"]
        for key in protected_keys:
            dict_copy[key] = "*********"
        return dict_copy

    class Config:
        env_prefix = ""
        env_file: str = join(dirname(__file__), "../../local/override.env")


# Instantiates the settings instance
settings = Settings()
