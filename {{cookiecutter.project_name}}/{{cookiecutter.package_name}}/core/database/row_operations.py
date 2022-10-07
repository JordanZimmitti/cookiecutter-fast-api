from logging import getLogger
from typing import Any, List, TypeVar

from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import Select

from {{cookiecutter.package_name}}.exceptions import InternalServerError

# Gets {{cookiecutter.friendly_name}} server logger instance
logger = getLogger("{{cookiecutter.package_name}}.core.database.row_operations")

# ORM model type-hinting
Model = TypeVar("Model")


class DatabaseRowOperations:
    def __init__(self, session_maker: sessionmaker):
        """
        Class that handles various aspects of
        database tables

        :param session_maker: A session-maker instance
        """

        # Initializes inputted variables
        self._session_maker = session_maker

    @staticmethod
    async def _execute_query(session: AsyncSession, query: Select) -> ChunkedIteratorResult:
        """
        Function that executes the query and gets the result. When the
        query cannot be executed an InternalServerError is raised

        :param session: The asynchronous session instance created for executing the query
        :param query: The query statement to execute

        :return: The result from the database
        """
        try:
            result: ChunkedIteratorResult = await session.execute(query)
            return result
        except Exception:
            logger.error("SQL-Alchemy session execution failed", exc_info=True)
            raise InternalServerError()

    async def add_row(self, table: Model):
        """
        Function that adds a row to an existing
        table within the database

        :param table: A table instance instantiated with new data to be added as a row
        """

        # Creates an async-session to add the new data into the table
        async with self._session_maker() as session:
            session: AsyncSession

            # Persists the new data to the table
            session.add(table)
            await session.flush()
            await session.commit()

    async def add_rows(self, tables: List[Model]):
        """
        Function that adds a list of rows to their respective
        existing table within the database

        :param tables: A list of table instances instantiated with new data to be added as a row
        """

        # Creates an async-session that adds the new data into each table in the list
        async with self._session_maker() as session:
            session: AsyncSession

            # Adds each table containing the new data to be persisted
            session.add_all(tables)

            # Persists the new data to each of the tables
            await session.flush()
            await session.commit()

    async def get_rows_all(self, model: Model, query: Select) -> List[Model]:
        """
        Function that executes the query and
        gets all the rows retrieved

        :param model: The database model used in the query
        :param query: The query statement to execute

        :return: A list of all rows retrieved from the database
        """

        # Creates an async-session to execute a query
        async with self._session_maker() as session:
            session: AsyncSession

            # Executes the query and returns all the rows
            result: ChunkedIteratorResult = await self._execute_query(session, query)
            row: List[model] = result.scalars().all()
            return row

    async def get_rows_first(self, model: Model, query: Select) -> Model | None:
        """
        Function that executes the query and gets the first
        row retrieved or none when no rows are retrieved

        :param model: The database model used in the query
        :param query: The query statement to execute

        :return: The first row retrieved from the database or None when no rows are retrieved
        """

        # Creates an async-session to execute a query
        async with self._session_maker() as session:
            session: AsyncSession

            # Executes the query and returns the first row from the query when it exists
            result = await self._execute_query(session, query)
            row: model | None = result.scalars().first()
            return row

    async def get_rows_one(self, model: Model, query: Select) -> Model:
        """
        Function that executes the query and gets the first row
        retrieved or raises an error when no rows are retrieved

        :param model: The database model used in the query
        :param query: The query statement to execute

        :return: The first row retrieved from the database or an error when no rows are retrieved
        """

        # Creates an async-session to execute a query
        async with self._session_maker() as session:
            session: AsyncSession

            # Executes the query and returns the first row from the query or raises an error
            try:
                result: ChunkedIteratorResult = await self._execute_query(session, query)
                row: model = result.scalars().one()
                return row
            except Exception:
                extra_info = {"query": str(query)}
                log_message = "A query was executed that expected a row returned back empty"
                logger.error(log_message, extra=extra_info)
                raise InternalServerError()

    async def get_rows_unique(self, query: Select, strategy: Any = None) -> ChunkedIteratorResult:
        """
        Function that executes the unique query and gets the
        chunked-iterator-result for data retrieval

        :param query: The query statement to execute
        :param strategy: The unique strategy used

        :return: The chunked-iterator-result of unique rows retrieved from the database
        """

        # Creates an async-session to execute a query
        async with self._session_maker() as session:
            session: AsyncSession

            # Executes the query and returns all the unique rows
            result: ChunkedIteratorResult = await self._execute_query(session, query)
            row = result.scalars().unique(strategy)
            return row
