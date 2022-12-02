from logging import getLogger
from typing import Any, List, TypeVar

from sqlalchemy import Result, ScalarResult, Select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from {{cookiecutter.package_name}}.exceptions import InternalServerError

# Gets {{cookiecutter.friendly_name}} server logger instance
logger = getLogger("{{cookiecutter.package_name}}.core.database.row_operations")

# ORM table type-hinting
ORMTable = TypeVar("ORMTable")


class DatabaseRowOperations:
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        """
        Class that handles executing various queries
        on a database table

        :param session_maker: An async-session-maker instance
        """

        # Initializes given variables
        self._session_maker = session_maker

    @staticmethod
    async def _execute_query(session: AsyncSession, query: Select) -> Result:
        """
        Function that executes the query and gets the result. When the
        query cannot be executed an InternalServerError is raised

        :param session: The asynchronous session instance created for executing the query
        :param query: The query statement to execute

        :return: The result from the database
        """
        try:
            result = await session.execute(query)
            return result
        except Exception as exc:
            logger.error("SQL-Alchemy session execution failed", exc_info=exc)
            raise InternalServerError()

    async def add_row(self, table: ORMTable):
        """
        Function that adds a row to an existing
        table within the database

        :param table: A table instance instantiated with new data to be added as a row
        """

        # Creates an async-session to add the new data into the table
        async with self._session_maker() as session:

            # Persists the new data to the table
            session.add(table)
            await session.flush()
            await session.commit()

    async def add_rows(self, tables: List[ORMTable]):
        """
        Function that adds a list of rows to their respective
        existing tables within the database

        :param tables: A list of table instances instantiated with new data to be added as a row
        """

        # Creates an async-session that adds the new data into each table in the list
        async with self._session_maker() as session:

            # Adds each table containing the new data to be persisted
            session.add_all(tables)

            # Persists the new data to each of the tables
            await session.flush()
            await session.commit()

    async def get_rows_all(self, orm_table: ORMTable, query: Select) -> List[ORMTable]:
        """
        Function that executes the query and
        gets all the rows retrieved

        :param orm_table: The database ORM table used in the query
        :param query: The query statement to execute

        :return: A list of all rows retrieved from the database
        """

        # Creates an async-session to execute a query
        async with self._session_maker() as session:

            # Executes the query and returns all the rows
            result = await self._execute_query(session, query)
            row: List[orm_table] = list(result.scalars().all())
            return row

    async def get_rows_first(self, orm_table: ORMTable, query: Select) -> ORMTable | None:
        """
        Function that executes the query and gets the first
        row retrieved or none when no rows are retrieved

        :param orm_table: The database ORM table used in the query
        :param query: The query statement to execute

        :return: The first row retrieved from the database or None when no rows are retrieved
        """

        # Creates an async-session to execute a query
        async with self._session_maker() as session:

            # Executes the query and returns the first row from the query when it exists
            result = await self._execute_query(session, query)
            row: orm_table | None = result.scalars().first()
            return row

    async def get_rows_one(self, orm_table: ORMTable, query: Select) -> ORMTable:
        """
        Function that executes the query and gets the first row
        retrieved or raises an error when no rows are retrieved

        :param orm_table: The database ORM table used in the query
        :param query: The query statement to execute

        :return: The first row retrieved from the database or an error when no/multiple are retrieved
        """

        # Creates an async-session to execute a query
        async with self._session_maker() as session:

            # Executes the query and returns the first row from the query or raises an error
            try:
                result = await self._execute_query(session, query)
                row: orm_table = result.scalars().one()
                return row
            except Exception:
                extra_info = {"query": str(query)}
                log_message = "A single row query came back empty or with multiple rows"
                logger.error(log_message, extra=extra_info)
                raise InternalServerError()

    async def get_rows_unique(self, query: Select, strategy: Any = None) -> ScalarResult:
        """
        Function that executes the unique query and gets the
        scalar-result for data retrieval

        :param query: The query statement to execute
        :param strategy: The unique strategy used

        :return: The scalar-result of unique rows retrieved from the database
        """

        # Creates an async-session to execute a query
        async with self._session_maker() as session:

            # Executes the query and returns all the unique rows
            result = await self._execute_query(session, query)
            row = result.scalars().unique(strategy)
            return row
