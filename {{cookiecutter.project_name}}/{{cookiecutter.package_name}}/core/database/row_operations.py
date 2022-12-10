from logging import getLogger
from typing import Any, List, TypeVar

from sqlalchemy import Result, ScalarResult, Select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from {{cookiecutter.package_name}}.exceptions import InternalServerError

# Gets {{cookiecutter.friendly_name}} server logger instance
logger = getLogger("{{cookiecutter.package_name}}.core.database.row_operations")

# Row-Operations type-hinting
ORMTable = TypeVar("ORMTable")
ReturnType = TypeVar("ReturnType")


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
            message = "SQL-Alchemy session execution failed"
            logger.error(message)
            logger.debug(message, exc_info=exc)
            raise InternalServerError()

    @staticmethod
    async def _commit_session(session: AsyncSession):
        """
        Function that flushes and commits the given session. When the session
        cannot be flushed and committed an InternalServerError is raised

        :param session: The asynchronous session instance to commit
        """
        try:
            await session.flush()
            await session.commit()
        except Exception as exc:
            message = "SQL-Alchemy session commit failed"
            logger.error(message)
            logger.debug(message, exc_info=exc)
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
            await self._commit_session(session)

    async def add_rows(self, tables: List[ORMTable]):
        """
        Function that adds a list of rows to their respective
        existing tables within the database

        :param tables: A list of table instances instantiated with new data to be added as a row
        """

        # Creates an async-session that adds the new data into each table in the list
        async with self._session_maker() as session:

            # Persists the new data to each of the tables
            session.add_all(tables)
            await self._commit_session(session)

    async def get_rows_all(
            self, return_type: ReturnType, query: Select, is_scalar: bool = True
    ) -> List[ReturnType]:
        """
        Function that executes the query and
        gets all the rows retrieved

        :param return_type: The return-type the query
        :param query: The query statement to execute
        :param is_scalar: Whether the object should be filtered through a scalar

        :return: A list of all rows retrieved from the database
        """

        # Creates an async-session to execute a query
        async with self._session_maker() as session:

            # Executes the query and returns all the rows
            result = await self._execute_query(session, query)
            if is_scalar:
                row: List[return_type] = list(result.scalars().all())
            else:
                row: List[return_type] = list(result.all())
            return row

    async def get_rows_first(
            self, return_type: ReturnType, query: Select, is_scalar: bool = True
    ) -> ReturnType | None:
        """
        Function that executes the query and gets the first
        row retrieved or none when no rows are retrieved

        :param return_type: The return-type the query
        :param query: The query statement to execute
        :param is_scalar: Whether the object should be filtered through a scalar

        :return: The first row retrieved from the database or None when no rows are retrieved
        """

        # Creates an async-session to execute a query
        async with self._session_maker() as session:

            # Executes the query and returns the first row from the query when it exists
            result = await self._execute_query(session, query)
            if is_scalar:
                row: return_type | None = result.scalars().first()
            else:
                row: return_type | None = result.first()
            return row

    async def get_rows_one(
            self, return_type: ReturnType, query: Select, is_scalar: bool = True
    ) -> ReturnType:
        """
        Function that executes the query and gets the first row
        retrieved or raises an error when no rows are retrieved

        :param return_type: The return-type the query
        :param query: The query statement to execute
        :param is_scalar: Whether the object should be filtered through a scalar

        :return: The first row retrieved from the database or an error when no/multiple are retrieved
        """

        # Creates an async-session to execute a query
        async with self._session_maker() as session:

            # Executes the query and returns the first row from the query or raises an error
            try:
                result = await self._execute_query(session, query)
                if is_scalar:
                    row: return_type = result.scalars().one()
                else:
                    row: return_type = result.one()
                return row
            except Exception:
                extra_info = {"query": str(query)}
                log_message = "A single row query came back empty or with multiple rows"
                logger.error(log_message, extra=extra_info)
                raise InternalServerError()

    async def get_rows_unique(
            self, query: Select, strategy: Any = None, is_scalar: bool = True
    ) -> ScalarResult:
        """
        Function that executes the unique query and gets the
        scalar-result for data retrieval

        :param query: The query statement to execute
        :param strategy: The unique strategy used
        :param is_scalar: Whether the object should be filtered through a scalar

        :return: The scalar-result of unique rows retrieved from the database
        """

        # Creates an async-session to execute a query
        async with self._session_maker() as session:

            # Executes the query and returns all the unique rows
            result = await self._execute_query(session, query)
            if is_scalar:
                row = result.scalars().unique(strategy)
            else:
                row = result.unique(strategy)
            return row
