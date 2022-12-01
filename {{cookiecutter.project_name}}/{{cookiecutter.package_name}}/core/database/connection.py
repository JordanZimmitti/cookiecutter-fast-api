from logging import getLogger

from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import close_all_sessions, sessionmaker

from {{cookiecutter.package_name}}.core.settings import settings
from {{cookiecutter.package_name}}.exceptions import InternalServerError

# Gets {{cookiecutter.friendly_name}} server logger instance
logger = getLogger("{{cookiecutter.package_name}}.core.database.connection")


class DatabaseConnection:
    def __init__(self, display_name: str, db_uri: SecretStr):
        """
        Class that opens a connection to a particular database
        and handles various aspects of the connection

        :param display_name: The name of the database to display to the client
        :param db_uri: The database connection url
        """

        # Initializes inputted variables
        self._display_name = display_name
        self._db_uri = db_uri

        # Initializes class-created variables
        self._engine: AsyncEngine | None = None
        self._schema: str | None = self._get_schema()
        self._session_maker: sessionmaker | None = None

    @property
    def session_maker(self) -> sessionmaker:

        # Checks whether a session-maker instance exists
        if self._session_maker is None:
            logger.info("The database is not connected, was the connect function called?")
            raise InternalServerError()

        # Returns the session_maker instance
        return self._session_maker

    def connect(self):
        """
        Function that creates the async engine for querying
        the Database that stores test data
        """

        # Creates the connection engine to the database
        self._engine: AsyncEngine = create_async_engine(
            self._db_uri.get_secret_value(),
            pool_pre_ping=True,
            pool_size=settings.SQLALCHEMY_POOL_SIZE,
            max_overflow=settings.SQLALCHEMY_MAX_OVERFLOW,
            echo=settings.IS_ECHO_SQLALCHEMY_LOGS,
            connect_args={"server_settings": {"application_name": f"{settings.PROJECT_NAME}"}},
        )

        # Creates the session-maker for creating database sessions
        self._session_maker = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )

        # Logs that the database connection pool was successfully created
        logger.info(f"Created the {self._display_name} connection pool")

    async def disconnect(self):
        """
        Function that disconnects all sessions from the session-maker in memory as well as
        disposing all connection pool connections that are currently checked in
        """

        # Disconnects all active sessions and the connection pool
        close_all_sessions()
        await self._engine.dispose()

        # Logs that the database was disconnected successfully
        logger.info(f"Disposes the active {self._display_name} connections in the connection pool")

    def _get_schema(self) -> str | None:
        """
        Function that gets the database schema. This is the prefix
        that is used for querying different tables and views

        :return: Returns the database schema when the database type requires it
        """

        # When the database is a PostgreSQL database
        if self._db_uri.get_secret_value().startswith("postgres"):
            return settings.API_DB_SCHEMA.get_secret_value()

        # When the database is a SQLite database
        else:
            return None
