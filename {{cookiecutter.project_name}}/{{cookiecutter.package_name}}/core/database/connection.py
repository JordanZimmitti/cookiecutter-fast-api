from logging import getLogger

from pydantic import SecretStr
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import close_all_sessions

from {{cookiecutter.package_name}}.core.settings import settings
from {{cookiecutter.package_name}}.exceptions import InternalServerError

# Gets the {{cookiecutter.friendly_name}} server logger instance
logger = getLogger("{{cookiecutter.package_name}}.core.database.connection")


class DatabaseConnection:
    def __init__(self, display_name: str, db_uri: SecretStr):
        """
        Class that opens a connection to a particular database
        and handles various aspects of the connection

        :param display_name: The name of the database to display to the client
        :param db_uri: The connection uri of the database
        """

        # Initializes the given variables
        self._display_name = display_name
        self._db_uri = db_uri

        # Initializes class-created variables
        self._engine: AsyncEngine | None = None
        self._session_maker: async_sessionmaker[AsyncSession] | None = None

    @property
    def session_maker(self) -> async_sessionmaker[AsyncSession]:
        """
        Property that gets the async sessionmaker. The async sessionmaker is used to
        create new database sessions and execute row operations on a database table

        :return: The sqlalchemy async sessionmaker
        """

        # Checks whether a session-maker instance exists
        if self._session_maker is None:
            logger.error("The database is not connected, was the connect function called?")
            raise InternalServerError()

        # Returns the session-maker instance
        return self._session_maker

    def connect(self):
        """
        Function that creates the async engine for handling the connection pool to the database.
        The engine is used to instantiate the async sessionmaker and handles the underlying
        connection when a new async session is created
        """

        # Creates the async engine for the database
        self._engine = create_async_engine(
            self._db_uri.get_secret_value(),
            pool_pre_ping=True,
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

        # Disconnects all active sessions and the connection pool
        close_all_sessions()
        await self._engine.dispose()

        # Logs that the database was disconnected successfully
        logger.info(f"Disposes the active {self._display_name} connections in the connection pool")
