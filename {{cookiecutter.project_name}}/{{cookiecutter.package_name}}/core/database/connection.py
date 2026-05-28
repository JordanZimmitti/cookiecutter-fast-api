from typing import Any

from google.cloud.sql.connector import Connector, IPTypes, create_async_connector
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from {{cookiecutter.package_name}}.core.settings import settings
from {{cookiecutter.package_name}}.exceptions import InternalServerError
from {{cookiecutter.package_name}}.services.logger import get_api_logger

# Gets the {{cookiecutter.friendly_name}} server logger instance
logger = get_api_logger("{{cookiecutter.package_name}}.core.database.connection")


class DatabaseConnection:
    def __init__(self, display_name: str, db_uri: SecretStr):
        """
        Class that opens a connection to a particular database
        and handles various aspects of the connection

        :param display_name: The name of the database to display to the client
        :param db_uri: The connection uri of the database
        """

        # Creates the given fields
        self._display_name = display_name
        self._db_uri = db_uri

        # Initializes the class-created variables
        self._connector: Connector | None = None
        self._engine: AsyncEngine | None = None
        self._session_maker: async_sessionmaker[AsyncSession] | None = None

    @property
    def engine(self) -> AsyncEngine:
        """
        Property that gets the async engine. The async engine is the core database management system
        of sqlalchemy and should only be used directly when no other solution provided can be used

        :return: The async engine instance
        """

        # Checks whether an engine instance exists
        if self._engine is None:
            message = "The database is not connected, was the connect function called?"
            logger.critical(message)
            raise InternalServerError()

        # Returns the async engine instance
        return self._engine

    @property
    def session_maker(self) -> async_sessionmaker[AsyncSession]:
        """
        Property that gets the async sessionmaker. The async sessionmaker is used to
        create new database sessions and execute row operations on a database table.
        The async sessionmaker should only be used directly when a solution is not
        provided through the RowOperations class

        :return: The sqlalchemy async sessionmaker
        """

        # Checks whether a session-maker instance exists
        if self._session_maker is None:
            message = "The database is not connected, was the connect function called?"
            logger.critical(message)
            raise InternalServerError()

        # Returns the session-maker instance
        return self._session_maker

    async def connect(self):
        """
        Function that creates the async engine for handling the connection pool to the database.
        The engine is used to instantiate the async sessionmaker and handles the underlying
        connection when a new async session is created
        """

        # Gets the native database URI
        db_uri = self._db_uri.get_secret_value()

        # Gets a Cloud SQL URI and creator When the database type is set to cloud
        creator = None
        if settings.API_DB_TYPE == "cloud":

            # Gets the Cloud SQL database URI
            db_uri = f"{settings.API_DB_DRIVER.get_secret_value()}://"

            # Gets a Cloud SQL creator
            self._connector = await create_async_connector()
            creator = self._get_cloud_sql_creator

        # Creates the async engine for the database
        self._engine = create_async_engine(
            url=db_uri,
            async_creator=creator,
            pool_pre_ping=True,
            pool_timeout=settings.SQLALCHEMY_POOL_TIMEOUT,
            pool_size=settings.SQLALCHEMY_POOL_SIZE,
            max_overflow=settings.SQLALCHEMY_MAX_OVERFLOW,
            echo=settings.IS_ECHO_SQLALCHEMY_LOGS,
            connect_args={"server_settings": {"application_name": f"{settings.PROJECT_NAME}"}},
        )

        # Creates the async sessionmaker for creating database sessions
        self._session_maker = async_sessionmaker(self._engine, expire_on_commit=False)

        # Logs that the database connection pool was successfully created
        logger.info(f"Created the {self._display_name} connection pool")

    async def disconnect(self):
        """
        Function that disconnects all sessions from the async sessionmaker that are in memory
        as well as disposing all connection pool connections that are currently checked in
        """

        # Disconnects the cloud connector when its used
        if settings.API_DB_TYPE == "cloud" and self._connector:
            await self._connector.close_async()

        # Disconnects all active sessions and the connection pool
        if self._engine:
            await self._engine.dispose()

        # Logs that the database was disconnected successfully
        logger.info(f"Disposes the active {self._display_name} connections in the connection pool")

    async def _get_cloud_sql_creator(self) -> Any:
        """
        Function that gets a creator for creating
        connections to a Cloud SQL instance

        :return a Cloud SQL creator
        """

        # Creates the creator for creating connections to a Cloud SQL instance
        creator = None
        if self._connector:
            creator = await self._connector.connect_async(
                enable_iam_auth=True,
                instance_connection_string=settings.API_DB_CLOUD_INSTANCE.get_secret_value(),
                driver=settings.API_DB_CLOUD_DRIVER.get_secret_value(),
                user=settings.API_DB_USER.get_secret_value(),
                db=settings.API_DB_DB.get_secret_value(),
                ip_type=IPTypes.PRIVATE if settings.API_DB_CLOUD_IS_PRIVATE else IPTypes.PUBLIC,
            )

        # Returns a Cloud SQL creator
        return creator
