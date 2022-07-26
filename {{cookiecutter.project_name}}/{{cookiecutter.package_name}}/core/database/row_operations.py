from logging import getLogger
from typing import Any, AsyncIterator, Callable, List, TypeVar

from sqlalchemy import Delete, Result, ScalarResult, Select, Update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from {{cookiecutter.package_name}}.exceptions import InternalServerError

# Gets {{cookiecutter.friendly_name}} server logger instance
logger = getLogger("{{cookiecutter.package_name}}.core.database.row_operations")

# Row-Operations type-hinting
ORMTable = TypeVar("ORMTable")
ReturnType = TypeVar("ReturnType")


class RowResult:
    def __init__(self, result: Result, is_scalar: bool):
        """
        Class that handles retrieving a row
        from the executed query result

        :param result: The executed query result
        :param is_scalar: Whether the object should be filtered through a scalar
        """

        # Initializes given variables
        self._is_scalar = is_scalar
        self._result: ScalarResult | Result = result.scalars() if is_scalar else result

    def first(self, return_type: ReturnType) -> ReturnType | None:
        """
        Function that gets the first row retrieved
        or none when no rows are retrieved

        :param return_type: The return-type the query

        :return: The first row retrieved or none when no rows are retrieved
        """

        # Returns the first row retrieved or none when no rows are retrieved
        row: return_type | None = self._result.first()
        return row

    def one(self, return_type: ReturnType) -> ReturnType:
        """
        Function that gets the first row retrieved or
        raises an error when no rows are retrieved

        :param return_type: The return-type the query

        :return: The first row retrieved or an error when no rows are retrieved
        """

        # Returns the first row retrieved or an error when no rows are retrieved
        try:
            row: return_type = self._result.one()
            return row
        except Exception as exc:
            message = "A single row query came back empty or with multiple rows"
            logger.error(message)
            logger.debug(message, exc_info=exc)
            raise InternalServerError()


class RowResults:
    def __init__(self, result: Result, is_scalar: bool):
        """
        Class that handles retrieving a list of
        rows from the executed query result

        :param result: The executed query result
        :param is_scalar: Whether the object should be filtered through a scalar
        """

        # Initializes given variables
        self._is_scalar = is_scalar
        self._unique_result = result.unique
        self._result: ScalarResult | Result = result.scalars() if is_scalar else result

    def all(self, return_type: ReturnType) -> List[ReturnType]:
        """
        Function that gets a list of
        all the rows retrieved

        :param return_type: The return-type the query

        :return: A list of all the rows retrieved
        """

        # Returns a list of all the rows retrieved
        rows: List[return_type] = list(self._result.all())
        return rows

    def fetch(self, return_type: ReturnType, size: int) -> List[ReturnType]:
        """
        Function that fetches a subset of
        all the rows retrieved

        :param return_type: The return-type the query
        :param size: The size of the subset of rows to retrieve

        :return: A subset of all the rows retrieved
        """

        # Returns a subset of all the rows retrieved
        rows: List[return_type] = list(self._result.fetchmany(size))
        return rows

    def unique(self, strategy: Callable[[Any], Any] = None) -> "RowResults":
        """
        Function that gets a row-result
        instance of unique rows

        :param strategy: The unique strategy used

        :return: A row-result instance of unique rows
        """

        # Returns a row-result instance of unique rows
        unique_result = self._unique_result(strategy)
        row_result = RowResults(unique_result, self._is_scalar)
        return row_result


class DatabaseRowOperations:
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        """
        Class that handles executing various
        queries on a database table

        :param session_maker: An async-session-maker instance
        """

        # Initializes given variables
        self._session_maker = session_maker

    @staticmethod
    async def _commit_session(session: AsyncSession):
        """
        Function that flushes and commits the given session. When the session
        cannot be flushed and committed an InternalServerError is raised

        :param session: The asynchronous session instance to commit
        """

        # Attempts to commit the session
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
        Function that adds a
        database table row

        :param table: A table instance instantiated with new data to be added as a row
        """

        # Persists the new data to the table
        async with self._session_maker() as session:
            session.add(table)
            await self._commit_session(session)

    async def add_rows(self, tables: List[ORMTable]):
        """
        Function that adds a list
        of database table rows

        :param tables: A list of table instances instantiated with new data to be added as a row
        """

        # Persists the new data to each of the tables
        async with self._session_maker() as session:
            session.add_all(tables)
            await self._commit_session(session)

    async def query_row(
        self, statement: Delete | Select | Update, is_commit: bool = False, is_scalar: bool = True
    ) -> RowResult:
        """
        Function that queries the database using the given statement. The given
        query statement is expected to retrieve a single row from the database

        :param statement: The query statement to execute
        :param is_commit: Whether the executed query statement should be committed
        :param is_scalar: Whether the object should be filtered through a scalar

        :return: A row-result instance
        """

        # Executes the query and gets the result
        result = await self._execute_query(statement, is_commit)

        # Returns the row result
        row_result = RowResult(result, is_scalar)
        return row_result

    async def query_rows(
        self, statement: Delete | Select | Update, is_commit: bool = False, is_scalar: bool = True
    ) -> RowResults:
        """
        Function that queries the database using the given statement. The given
        query statement is expected to retrieve multiple rows from the database

        :param statement: The query statement to execute
        :param is_commit: Whether the executed query statement should be committed
        :param is_scalar: Whether the object should be filtered through a scalar

        :return: A row-results instance
        """

        # Executes the query and gets the result
        result = await self._execute_query(statement, is_commit)

        # Returns the row result
        row_results = RowResults(result, is_scalar)
        return row_results

    async def stream_rows(
        self, return_type: ReturnType, statement: Select, batch: int, is_scalar: bool = True
    ) -> AsyncIterator[List[ReturnType]]:
        """
        Function that streams rows from the database using the given select statement. The number
        of rows given from the batch number will be yielded until all rows from the select query
        statement are retrieved

        :param return_type: The return-type the query
        :param statement: The query select statement to execute
        :param batch: The number of rows to retrieve per chunk
        :param is_scalar: Whether the object should be filtered through a scalar

        :return: A chunk all the rows retrieved
        """
        try:
            async with self._session_maker() as session:
                stream_result = await session.stream(statement)
                result = stream_result.scalars() if is_scalar else stream_result
                while True:
                    rows: List[return_type] = list(await result.fetchmany(batch))
                    if not rows:
                        break
                    yield rows
        except Exception as exc:
            message = "SQL-Alchemy session streaming failed"
            logger.error(message)
            logger.debug(message, exc_info=exc)
            raise InternalServerError()

    async def _execute_query(self, statement: Delete | Select | Update, is_commit: bool) -> Result:
        """
        Function that executes the query and gets the result. When the
        query cannot be executed an InternalServerError is raised

        :param statement: The query statement to execute
        :param is_commit: Whether the executed query statement should be committed

        :return: The result from the database
        """

        # Attempts to execute the query
        try:
            async with self._session_maker() as session:
                result = await session.execute(statement)
                if is_commit:
                    await self._commit_session(session)
                return result
        except Exception as exc:
            message = "SQL-Alchemy session execution failed"
            logger.error(message)
            logger.debug(message, exc_info=exc)
            raise InternalServerError()
