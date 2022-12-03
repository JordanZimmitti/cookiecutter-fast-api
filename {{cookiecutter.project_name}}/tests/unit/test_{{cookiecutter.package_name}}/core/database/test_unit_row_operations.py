from unittest.mock import AsyncMock, MagicMock

from pytest import mark, raises
from sqlalchemy import Result, Row, ScalarResult, Select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from {{cookiecutter.package_name}}.core.database.row_operations import DatabaseRowOperations, ORMTable
from {{cookiecutter.package_name}}.exceptions import InternalServerError
from tests.mocks import error_mock


@mark.asyncio
async def test_add_row():
    """
    Tests the add_row function for completion. The add_row function
    should call the required methods without any errors
    """

    # Mocks the async-session class
    async_session_mock = AsyncMock(spec_set=AsyncSession)

    # Mocks the async_sessionmaker aenter function
    async def aenter_mock(_):
        return async_session_mock

    # Mocks the async_sessionmaker class
    session_maker_mock = MagicMock()
    session_maker_mock.__aenter__ = aenter_mock

    # Mocks the database-row-operations class
    database_row_operations_mock = MagicMock(spec=DatabaseRowOperations)
    database_row_operations_mock._session_maker = lambda: session_maker_mock

    # Invokes the add_row functon
    await DatabaseRowOperations.add_row(self=database_row_operations_mock, table=None)

    # Checks whether the required methods were called correctly
    assert async_session_mock.add.call_count == 1
    assert async_session_mock.flush.call_count == 1
    assert async_session_mock.commit.call_count == 1


@mark.asyncio
async def test_add_rows():
    """
    Tests the add_rows function for completion. The add_rows function
    should call the required methods without any errors
    """

    # Mocks the async-session class
    async_session_mock = AsyncMock(spec_set=AsyncSession)

    # Mocks the async_sessionmaker aenter function
    async def aenter_mock(_):
        return async_session_mock

    # Mocks the async_sessionmaker class
    session_maker_mock = MagicMock()
    session_maker_mock.__aenter__ = aenter_mock

    # Mocks the database-row-operations class
    database_row_operations_mock = MagicMock(spec=DatabaseRowOperations)
    database_row_operations_mock._session_maker = lambda: session_maker_mock

    # Invokes the add_rows functon
    await DatabaseRowOperations.add_rows(self=database_row_operations_mock, tables=[None])

    # Checks whether the required methods were called correctly
    assert async_session_mock.add_all.call_count == 1
    assert async_session_mock.flush.call_count == 1
    assert async_session_mock.commit.call_count == 1


@mark.asyncio
async def test_execute_query():
    """
    Tests the _execute_query function for completion. The _execute_query function
    should call the required methods without any errors
    """

    # Mocks the async-session class
    async_session_mock = AsyncMock(spec_set=AsyncSession)

    # Mocks the query class
    query_mock = MagicMock(spec_set=Select)

    # Invokes the _execute_query functon
    await DatabaseRowOperations._execute_query(async_session_mock, query_mock)

    # Checks whether the required methods were called correctly
    assert async_session_mock.execute.call_count == 1


@mark.asyncio
async def test_execute_query_error():
    """
    Tests the _execute_query function when an error occurs. The
    _execute_query function should raise an InternalServerError
    """

    # Mocks the async-session class
    async_session_mock = MagicMock(spec_set=AsyncSession)
    async_session_mock.execute = error_mock

    # Mocks the query class
    query_mock = MagicMock(spec_set=Select)

    # Checks whether the correct error was raised
    with raises(InternalServerError):
        await DatabaseRowOperations._execute_query(async_session_mock, query_mock)


@mark.asyncio
async def test_get_rows_all():
    """
    Tests the get_rows_all function for completion. The get_rows_all function
    should return a list of orm tables without any errors
    """

    # Mocks the orm-table class
    orm_table_mock = MagicMock(spec_set=ORMTable)

    # Mocks the data retrieved from the all function
    all_data_mock = [orm_table_mock]

    # Mocks the scalars function
    scalars_mock = MagicMock()
    scalars_mock.all = lambda: all_data_mock

    # Mocks the result class
    result_mock = MagicMock(spec_set=Result)
    result_mock.scalars = lambda: scalars_mock

    # Mocks the execute_query function
    async def execute_query_mock(*_):
        return result_mock

    # Mocks the database-row-operations class
    database_row_operations_mock = MagicMock(spec=DatabaseRowOperations)
    database_row_operations_mock._session_maker = lambda: AsyncMock(spec_set=AsyncSession)
    database_row_operations_mock._execute_query = execute_query_mock

    # Invokes the get_rows_all functon
    rows = await DatabaseRowOperations.get_rows_all(
        self=database_row_operations_mock, orm_table=orm_table_mock, query=MagicMock(spec_set=Select)
    )

    # Checks whether the rows were retrieved correctly
    assert rows == all_data_mock


@mark.asyncio
async def test_get_rows_all_no_scalar():
    """
    Tests the get_rows_all function when the result should not be filtered though a scalar.
    The get_rows_all function should return a list of sqlalchemy rows without any errors
    """

    # Mocks the row class
    row_mock = MagicMock(spec_set=Row)

    # Mocks the data retrieved from the all function
    all_data_mock = [row_mock]

    # Mocks the result class
    result_mock = MagicMock(spec_set=Result)
    result_mock.all.return_value = all_data_mock

    # Mocks the execute_query function
    async def execute_query_mock(*_):
        return result_mock

    # Mocks the database-row-operations class
    database_row_operations_mock = MagicMock(spec=DatabaseRowOperations)
    database_row_operations_mock._session_maker = lambda: AsyncMock(spec_set=AsyncSession)
    database_row_operations_mock._execute_query = execute_query_mock

    # Invokes the get_rows_all functon
    rows = await DatabaseRowOperations.get_rows_all(
        self=database_row_operations_mock,
        orm_table=row_mock,
        query=MagicMock(spec_set=Select),
        is_scalar=False,
    )

    # Checks whether the rows were retrieved correctly
    assert rows == all_data_mock


@mark.asyncio
async def test_get_rows_first():
    """
    Tests the get_rows_first function for completion. The get_rows_first function
    should return an orm table without any errors
    """

    # Mocks the orm-table class
    orm_table_mock = MagicMock(spec_set=ORMTable)

    # Mocks the data retrieved from the first function
    first_data_mock = orm_table_mock

    # Mocks the scalars function
    scalars_mock = MagicMock()
    scalars_mock.first = lambda: first_data_mock

    # Mocks the result class
    result_mock = MagicMock(spec_set=Result)
    result_mock.scalars = lambda: scalars_mock

    # Mocks the execute_query function
    async def execute_query_mock(*_):
        return result_mock

    # Mocks the database-row-operations class
    database_row_operations_mock = MagicMock(spec=DatabaseRowOperations)
    database_row_operations_mock._session_maker = lambda: AsyncMock(spec_set=AsyncSession)
    database_row_operations_mock._execute_query = execute_query_mock

    # Invokes the get_rows_first functon
    row = await DatabaseRowOperations.get_rows_first(
        self=database_row_operations_mock, orm_table=orm_table_mock, query=MagicMock(spec_set=Select)
    )

    # Checks whether the row was retrieved correctly
    assert row == first_data_mock


@mark.asyncio
async def test_get_rows_first_no_scalar():
    """
    Tests the get_rows_first function when the result should not be filtered though a scalar.
    The get_rows_first function should return a sqlalchemy row without any errors
    """

    # Mocks the row class
    row_mock = MagicMock(spec_set=Row)

    # Mocks the data retrieved from the first function
    first_data_mock = row_mock

    # Mocks the result class
    result_mock = MagicMock(spec_set=Result)
    result_mock.first.return_value = first_data_mock

    # Mocks the execute_query function
    async def execute_query_mock(*_):
        return result_mock

    # Mocks the database-row-operations class
    database_row_operations_mock = MagicMock(spec=DatabaseRowOperations)
    database_row_operations_mock._session_maker = lambda: AsyncMock(spec_set=AsyncSession)
    database_row_operations_mock._execute_query = execute_query_mock

    # Invokes the get_rows_first functon
    row = await DatabaseRowOperations.get_rows_first(
        self=database_row_operations_mock,
        orm_table=row_mock,
        query=MagicMock(spec_set=Select),
        is_scalar=False,
    )

    # Checks whether the row was retrieved correctly
    assert row == first_data_mock


@mark.asyncio
async def test_get_rows_one():
    """
    Tests the get_rows_one function for completion. The get_rows_one function
    should return an orm table without any errors
    """

    # Mocks the orm-table class
    orm_table_mock = MagicMock(spec_set=ORMTable)

    # Mocks the data retrieved from the one function
    one_data_mock = orm_table_mock

    # Mocks the scalars function
    scalars_mock = MagicMock()
    scalars_mock.one = lambda: one_data_mock

    # Mocks the result class
    result_mock = MagicMock(spec_set=Result)
    result_mock.scalars = lambda: scalars_mock

    # Mocks the execute_query function
    async def execute_query_mock(*_):
        return result_mock

    # Mocks the database-row-operations class
    database_row_operations_mock = MagicMock(spec=DatabaseRowOperations)
    database_row_operations_mock._session_maker = lambda: AsyncMock(spec_set=AsyncSession)
    database_row_operations_mock._execute_query = execute_query_mock

    # Invokes the get_rows_first functon
    row = await DatabaseRowOperations.get_rows_one(
        self=database_row_operations_mock, orm_table=orm_table_mock, query=MagicMock(spec_set=Select)
    )

    # Checks whether the row was retrieved correctly
    assert row == one_data_mock


@mark.asyncio
async def test_get_rows_one_no_scalar():
    """
    Tests the get_rows_one function when the result should not be filtered though a scalar.
    The get_rows_one function should return a sqlalchemy row without any errors
    """

    # Mocks the row class
    row_mock = MagicMock(spec_set=Row)

    # Mocks the data retrieved from the one function
    one_data_mock = row_mock

    # Mocks the result class
    result_mock = MagicMock(spec_set=Result)
    result_mock.one.return_value = one_data_mock

    # Mocks the execute_query function
    async def execute_query_mock(*_):
        return result_mock

    # Mocks the database-row-operations class
    database_row_operations_mock = MagicMock(spec=DatabaseRowOperations)
    database_row_operations_mock._session_maker = lambda: AsyncMock(spec_set=AsyncSession)
    database_row_operations_mock._execute_query = execute_query_mock

    # Invokes the get_rows_first functon
    row = await DatabaseRowOperations.get_rows_one(
        self=database_row_operations_mock,
        orm_table=row_mock,
        query=MagicMock(spec_set=Select),
        is_scalar=False,
    )

    # Checks whether the row was retrieved correctly
    assert row == one_data_mock


@mark.asyncio
async def test_get_rows_one_no_row():
    """
    Tests the get_rows_one function when no rows are returned. The get_rows_one
    function should raise an InternalServerError
    """

    # Mocks the orm-table class
    orm_table_mock = MagicMock(spec_set=ORMTable)

    # Mocks the one function
    def one_mock():
        raise InternalServerError()

    # Mocks the scalars function
    scalars_mock = MagicMock()
    scalars_mock.one = one_mock

    # Mocks the result class
    result_mock = MagicMock(spec_set=Result)
    result_mock.scalars = lambda: scalars_mock

    # Mocks the execute_query function
    async def execute_query_mock(*_):
        return result_mock

    # Mocks the database-row-operations class
    database_row_operations_mock = MagicMock(spec=DatabaseRowOperations)
    database_row_operations_mock._session_maker = lambda: AsyncMock(spec_set=AsyncSession)
    database_row_operations_mock._execute_query = execute_query_mock

    # Checks whether the correct error was raised
    with raises(InternalServerError):
        await DatabaseRowOperations.get_rows_one(
            self=database_row_operations_mock,
            orm_table=orm_table_mock,
            query=MagicMock(spec_set=Select)
        )


@mark.asyncio
async def test_get_rows_unique():
    """
    Tests the get_rows_unique function for completion. The get_rows_unique function
    should return a scalar-result without any errors
    """

    # Mocks the scalar-result class
    unique_scalar_result_mock = MagicMock(spec_set=ScalarResult)

    # Mocks the data retrieved from the unique function
    unique_data_mock = unique_scalar_result_mock

    # Mocks the scalars function
    scalars_mock = MagicMock()
    scalars_mock.unique = lambda _: unique_data_mock

    # Mocks the result class
    result_mock = MagicMock(spec_set=Result)
    result_mock.scalars = lambda: scalars_mock

    # Mocks the execute_query function
    async def execute_query_mock(*_):
        return result_mock

    # Mocks the database-row-operations class
    database_row_operations_mock = MagicMock(spec=DatabaseRowOperations)
    database_row_operations_mock._session_maker = lambda: AsyncMock(spec_set=AsyncSession)
    database_row_operations_mock._execute_query = execute_query_mock

    # Invokes the get_rows_unique functon
    result = await DatabaseRowOperations.get_rows_unique(
        self=database_row_operations_mock, query=MagicMock(spec_set=Select)
    )

    # Checks whether the row was retrieved correctly
    assert result == unique_scalar_result_mock


@mark.asyncio
async def test_get_rows_unique_no_scalar():
    """
    Tests the get_rows_unique function when the result should not be filtered though a scalar.
    The get_rows_unique function should return a result without any errors
    """

    # Mocks the result's unique function
    result_unique_mock = MagicMock()

    # Mocks the result class
    result_mock = MagicMock(spec_set=Result)
    result_mock.unique.return_value = result_unique_mock

    # Mocks the execute_query function
    async def execute_query_mock(*_):
        return result_mock

    # Mocks the database-row-operations class
    database_row_operations_mock = MagicMock(spec=DatabaseRowOperations)
    database_row_operations_mock._session_maker = lambda: AsyncMock(spec_set=AsyncSession)
    database_row_operations_mock._execute_query = execute_query_mock

    # Invokes the get_rows_unique functon
    result = await DatabaseRowOperations.get_rows_unique(
        self=database_row_operations_mock, query=MagicMock(spec_set=Select), is_scalar=False
    )

    # Checks whether the row was retrieved correctly
    assert result == result_unique_mock


def test_init():
    """
    Tests the DatabaseRowOperations init function for completion. The DatabaseRowOperations init
    function should instantiate a DatabaseRowOperations instance without any errors
    """

    # Mocks and overrides the async_sessionmaker function
    session_maker_mock = MagicMock(spec_set=async_sessionmaker[AsyncSession])

    # Define and instantiates the DatabaseRowOperations class
    db_connection = DatabaseRowOperations(session_maker=session_maker_mock)

    # Checks whether the DatabaseRowOperations class correctly instantiated
    assert db_connection._session_maker == session_maker_mock
