from pydantic import SecretStr

from .connection import DatabaseConnection
from .row_operations import DatabaseRowOperations


class DatabaseManager:
    def __init__(self, display_name: str, description: str, db_uri: SecretStr):
        """
        Class that handles various
        database operations

        :param display_name: The name of the database to display to the client
        :param description: A short description about the database
        :param db_uri: The connection uri of the database
        """

        # Initializes the given variables
        self._display_name = display_name
        self._description = description
        self._db_uri = db_uri

        # Instantiates the database-manager classes
        self._connection = DatabaseConnection(display_name, db_uri)
        self._row_operations: DatabaseRowOperations | None = None

    @property
    def connection(self) -> DatabaseConnection:
        """
        Property that gets the database-connection instance for
        handling various aspects of the database connection

        :return: The database-connection instance
        """
        return self._connection

    @property
    def display_name(self) -> str:
        """
        Property that gets the name of the
        database to display to the client

        :return: The database display name
        """
        return self._display_name

    @property
    def description(self) -> str:
        """
        Property that gets a short description
        about the database

        :return: The database description
        """
        return self._description

    @property
    def row_operations(self) -> DatabaseRowOperations:
        """
        Property that instantiates a database-row-operations class
        for adding, deleting, getting, and updating rows

        :return: A database-row-operations instance
        """

        # Creates a database-row-operations instance when it does not exist
        if not self._row_operations:
            self._row_operations = DatabaseRowOperations(self._connection.session_maker)

        # Returns a database-row-operations instance
        return self._row_operations
