from pydantic import SecretStr

from .connection import DatabaseConnection
from .row_operations import DatabaseRowOperations


class DatabaseManager:
    def __init__(self, display_name: str, description: str, db_uri: SecretStr):
        """
        Class that handles various
        database operations

        :param display_name: The name of the database to display to the client
        :param description: the description of the database
        :param db_uri: The database connection url
        """

        # Initializes inputted variables
        self._display_name = display_name
        self._description = description
        self._db_uri = db_uri

        # Instantiated class-created classes
        self._connection = DatabaseConnection(self._display_name, self._db_uri)

    @property
    def connection(self) -> DatabaseConnection:
        """
        Property that geta the database-connection instance for
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
        Property that gets the description
        of the database

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
        row_operations = DatabaseRowOperations(self._connection.session_maker)
        return row_operations
