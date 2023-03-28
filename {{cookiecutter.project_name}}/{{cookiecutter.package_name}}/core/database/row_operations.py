from logging import getLogger
from typing import Any, AsyncIterator, Callable, List, Type, TypeVar, get_origin

from sqlalchemy import Delete, Result, ScalarResult, Select, TextClause, Update
from sqlalchemy.ext.asyncio import AsyncResult, AsyncSession, async_sessionmaker
from tenacity import retry, stop_after_attempt, wait_fixed

from {{cookiecutter.package_name}}.core.settings import settings
from {{cookiecutter.package_name}}.exceptions import InternalServerError

# Gets the {{cookiecutter.friendly_name}} server logger instance
logger = getLogger("{{cookiecutter.package_name}}.core.database.row_operations")

# Row-Operations type-hinting
ORMTable = TypeVar("ORMTable")
ReturnType = TypeVar("ReturnType")
Statement = Delete | Select | Update | TextClause


class RowResult:
    def __init__(self, result: Result, is_scalar: bool):
        """
        Class that handles retrieving a row
        from the executed query result

        :param result: The executed query result
        :param is_scalar: Whether the object should be filtered through a scalar
        """

        # Initializes the given variables
        self._is_scalar = is_scalar
        self._result: ScalarResult | Result = result.scalars() if is_scalar else result

    def first(self, return_type: Type[ReturnType]) -> ReturnType | None:
        """
        Function that gets the first row retrieved
        or none when no rows are retrieved

        :param return_type: The return-type of the query

        :return: The first row retrieved or none when no rows are retrieved
        """

        # Returns the first row retrieved or none when no rows are retrieved
        row: return_type | None = self._result.first()
        if row:
            _enforce_base_type(row, return_type)
        return row

    def one(self, return_type: Type[ReturnType]) -> ReturnType:
        """
        Function that gets the first row retrieved or
        raises an error when no rows are retrieved

        :param return_type: The return-type of the query

        :return: The first row retrieved or an error when no rows are retrieved
        """

        # Returns the first row retrieved or an error when no rows are retrieved
        try:
            row: return_type = self._result.one()
            if row:
                _enforce_base_type(row, return_type)
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

        # Initializes the given variables
        self._is_scalar = is_scalar
        self._unique_result = result.unique
        self._result: ScalarResult | Result = result.scalars() if is_scalar else result

    def all(self, return_type: Type[ReturnType]) -> List[ReturnType]:
        """
        Function that gets a list of
        all the rows retrieved

        :param return_type: The return-type of the query

        :return: A list of all the rows retrieved
        """

        # Returns a list of all the rows retrieved
        rows: List[return_type] = list(self._result.all())
        if rows:
            _enforce_base_type(rows[0], return_type)
        return rows

    def fetch(self, return_type: Type[ReturnType], size: int) -> List[ReturnType]:
        """
        Function that fetches a subset of
        all the rows retrieved

        :param return_type: The return-type of the query
        :param size: The size of the subset of rows to retrieve

        :return: A subset of all the rows retrieved
        """

        # Returns a subset of all the rows retrieved
        rows: List[return_type] = list(self._result.fetchmany(size))
        if rows:
            _enforce_base_type(rows[0], return_type)
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

        :param session_maker: An async sessionmaker instance
        """

        # Initializes the given variables
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

    @retry(stop=stop_after_attempt(settings.API_DB_QUERY_RETRY_NUMBER), wait=wait_fixed(1))
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

    @retry(stop=stop_after_attempt(settings.API_DB_QUERY_RETRY_NUMBER), wait=wait_fixed(1))
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

    @retry(stop=stop_after_attempt(settings.API_DB_QUERY_RETRY_NUMBER), wait=wait_fixed(1))
    async def query_row(
        self, statement: Statement, is_commit: bool = False, is_scalar: bool = True, **kwargs
    ) -> RowResult:
        """
        Function that queries the database using the given statement. The given
        query statement is expected to retrieve a single row from the database

        :param statement: The query statement to execute
        :param is_commit: Whether the executed query statement should be committed
        :param is_scalar: Whether the object should be filtered through a scalar
        :param kwargs: Any kwarg accepted in the :class:`AsyncSession` execute function

        :return: A row-result instance
        """

        # Executes the query and gets the result
        result = await self._execute_query(statement, is_commit, **kwargs)

        # Returns the row result
        row_result = RowResult(result, is_scalar)
        return row_result

    @retry(stop=stop_after_attempt(settings.API_DB_QUERY_RETRY_NUMBER), wait=wait_fixed(1))
    async def query_rows(
        self, statement: Statement, is_commit: bool = False, is_scalar: bool = True, **kwargs
    ) -> RowResults:
        """
        Function that queries the database using the given statement. The given
        query statement is expected to retrieve multiple rows from the database

        :param statement: The query statement to execute
        :param is_commit: Whether the executed query statement should be committed
        :param is_scalar: Whether the object should be filtered through a scalar
        :param kwargs: Any kwarg accepted in the :class:`AsyncSession` execute function

        :return: A row-results instance
        """

        # Executes the query and gets the result
        result = await self._execute_query(statement, is_commit, **kwargs)

        # Returns the row result
        row_results = RowResults(result, is_scalar)
        return row_results

    async def stream_rows(
        self,
        return_type: Type[ReturnType],
        statement: Select | TextClause,
        batch: int,
        is_scalar: bool = True,
        **kwargs
    ) -> AsyncIterator[List[ReturnType]]:
        """
        Function that streams rows from the database using the given select statement. The number
        of rows given from the batch number will be yielded until all rows from the select query
        statement are retrieved

        :param return_type: The return-type of the query
        :param statement: The query select statement to execute
        :param batch: The number of rows to retrieve per chunk
        :param is_scalar: Whether the object should be filtered through a scalar
        :param kwargs: Any kwarg accepted in the :class:`AsyncSession` execute function

        :return: A chunk all the rows retrieved
        """

        # Attempts to stream rows from the database
        async with self._session_maker() as session:
            stream_result = await self._start_stream(session, statement, is_scalar, **kwargs)
            while True:
                rows: List[return_type] = list(await stream_result.fetchmany(batch))
                if not rows:
                    break
                _enforce_base_type(rows[0], return_type)
                yield rows

    async def _execute_query(self, statement: Statement, is_commit: bool, **kwargs) -> Result:
        """
        Function that executes the query and gets the result. When the
        query cannot be executed an InternalServerError is raised

        :param statement: The query statement to execute
        :param is_commit: Whether the executed query statement should be committed
        :param kwargs: Any kwarg accepted in the :class:`AsyncSession` execute function

        :return: The result from the database
        """

        # Attempts to execute the query
        try:
            async with self._session_maker() as session:
                result = await session.execute(statement, **kwargs)
                if is_commit:
                    await self._commit_session(session)
                return result
        except Exception as exc:
            message = "SQL-Alchemy session execution failed"
            logger.error(message)
            logger.debug(message, exc_info=exc)
            raise InternalServerError()

    @retry(stop=stop_after_attempt(settings.API_DB_QUERY_RETRY_NUMBER), wait=wait_fixed(1))
    async def _start_stream(
        self, session: AsyncSession, statement: Select | TextClause, is_scalar: bool, **kwargs
    ) -> AsyncResult:
        """
        Function that starts the stream and gets the streaming result for streaming rows in batches.
        This function's main purpose is to get tenacity retries to work since retries do not work
        on generator functions

        :param session: An async session instance
        :param statement: The query select statement to execute
        :param is_scalar: Whether the object should be filtered through a scalar
        :param kwargs: Any kwarg accepted in the :class:`AsyncSession` execute function

        :return: An async streaming result
        """

        # Attempts to Start the stream and return the stream result
        try:
            result = await session.stream(statement, **kwargs)
            stream_result = result.scalars() if is_scalar else result
            return stream_result
        except Exception as exc:
            message = "SQL-Alchemy session streaming failed"
            logger.error(message)
            logger.debug(message, exc_info=exc)
            raise InternalServerError()


def _enforce_base_type(row_data: Any, return_type: Type[ReturnType]):
    """
    Function that checks whether the row data returned from the database matches the
    given return-type. When the types do not match an InternalServerError is raised

    :param row_data: The data retrieved from the database
    :param return_type: The return-type of the query
    """

    # Checks whether the row data returned from the database matches the given return-type
    origin_type = get_origin(return_type)
    instance_type = return_type if not origin_type else origin_type
    if not isinstance(row_data, instance_type):
        message = (
            f"the given row with a type of '{type(row_data)}'"
            f" is not an instance of the base type '{return_type}'"
        )
        logger.error(message)
        raise InternalServerError()
