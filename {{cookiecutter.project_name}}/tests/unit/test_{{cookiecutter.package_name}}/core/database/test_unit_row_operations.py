from typing import List
from unittest.mock import AsyncMock, MagicMock

from pytest import mark, raises
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from {{cookiecutter.package_name}}.core.database import row_operations
from {{cookiecutter.package_name}}.core.database.row_operations import (
    DatabaseRowOperations,
    RowResult,
    RowResults,
    _enforce_base_type,
)
from {{cookiecutter.package_name}}.exceptions import InternalServerError
from tests.mocks import error_mock


def test_enforce_base_type():
    """
    Tests the _enforce_base_type function when the row-data type matches the given
    return-type. The _enforce_base_type function should return without any errors
    """

    # Checks whether no error was raised
    _enforce_base_type(row_data="", return_type=str)


def test_enforce_base_type_not_same():
    """
    Tests the _enforce_base_type function when the row-data type does not match the given
    return-type. The _enforce_base_type function should raise an InternalServerError
    """

    # Checks whether the correct error was raised
    with raises(InternalServerError):
        _enforce_base_type(row_data={}, return_type=List)


@mark.asyncio
async def test_add_row():
    """
    Tests the add_row function for completion. The add_row function
    should call the required methods without any errors
    """

    # Mocks the async-session class
    async_session_mock = AsyncMock(spec_set=AsyncSession)

    # Mocks the _commit_session function
    commit_session_mock = AsyncMock()

    # Mocks the async_sessionmaker aenter function
    async def aenter_mock(_):
        return async_session_mock

    # Mocks the async_sessionmaker class
    session_maker_mock = MagicMock()
    session_maker_mock.__aenter__ = aenter_mock

    # Mocks the database-row-operations class
    database_row_operations_mock = MagicMock(spec=DatabaseRowOperations)
    database_row_operations_mock._session_maker = lambda: session_maker_mock
    database_row_operations_mock._commit_session = commit_session_mock

    # Invokes the add_row functon
    await DatabaseRowOperations.add_row.__wrapped__.__wrapped__(
        self=database_row_operations_mock, table=None
    )

    # Checks whether the required methods were called correctly
    assert async_session_mock.add.called
    assert commit_session_mock.called


@mark.asyncio
async def test_add_rows():
    """
    Tests the add_rows function for completion. The add_rows function
    should call the required methods without any errors
    """

    # Mocks the async-session class
    async_session_mock = AsyncMock(spec_set=AsyncSession)

    # Mocks the _commit_session function
    commit_session_mock = AsyncMock()

    # Mocks the async_sessionmaker aenter function
    async def aenter_mock(_):
        return async_session_mock

    # Mocks the async_sessionmaker class
    session_maker_mock = MagicMock()
    session_maker_mock.__aenter__ = aenter_mock

    # Mocks the database-row-operations class
    database_row_operations_mock = MagicMock(spec=DatabaseRowOperations)
    database_row_operations_mock._session_maker = lambda: session_maker_mock
    database_row_operations_mock._commit_session = commit_session_mock

    # Invokes the add_rows functon
    await DatabaseRowOperations.add_rows.__wrapped__.__wrapped__(
        self=database_row_operations_mock, tables=[None]
    )

    # Checks whether the required methods were called correctly
    assert async_session_mock.add_all.called
    assert commit_session_mock.called


@mark.asyncio
async def test_commit_session():
    """
    Tests the _commit_session function for completion. The _commit_session
    function should call the required methods without any errors
    """

    # Mocks the async-session class
    async_session_mock = AsyncMock(spec_set=AsyncSession)

    # Invokes the _commit_session functon
    await DatabaseRowOperations._commit_session(async_session_mock)

    # Checks whether the required methods were called correctly
    assert async_session_mock.flush.called
    assert async_session_mock.commit.called


@mark.asyncio
async def test_commit_session_error():
    """
    Tests the _commit_session function when an error occurs. The
    _commit_session function should raise an InternalServerError
    """

    # Mocks the async-session class
    async_session_mock = MagicMock(spec_set=AsyncSession)
    async_session_mock.flush = error_mock

    # Checks whether the correct error was raised
    with raises(InternalServerError):
        await DatabaseRowOperations._commit_session(async_session_mock)


@mark.asyncio
async def test_execute_query():
    """
    Tests the _execute_query function for completion. The _execute_query
    function should call the required methods without any errors
    """

    # Mocks the select class
    statement_mock = MagicMock(spec_set=Select)

    # Mocks the async-session class
    async_session_mock = AsyncMock(spec_set=AsyncSession)

    # Mocks the async_sessionmaker aenter function
    async def aenter_mock(_):
        return async_session_mock

    # Mocks the async_sessionmaker class
    session_maker_mock = MagicMock()
    session_maker_mock.__aenter__ = aenter_mock

    # Mocks the _commit_session function
    commit_session_mock = AsyncMock()

    # Mocks the database-row-operations class
    database_row_operations_mock = MagicMock(spec=DatabaseRowOperations)
    database_row_operations_mock._session_maker = lambda: session_maker_mock
    database_row_operations_mock._commit_session = commit_session_mock

    # Invokes the _execute_query functon
    await DatabaseRowOperations._execute_query(
        self=database_row_operations_mock, statement=statement_mock, is_commit=True
    )

    # Checks whether the required methods were called correctly
    assert async_session_mock.execute.called
    assert commit_session_mock.called

    # Checks whether the required parameters were passed correctly
    assert async_session_mock.execute.call_args.args[0] == statement_mock
    assert commit_session_mock.call_args.args[0] == async_session_mock


@mark.asyncio
async def test_execute_query_error():
    """
    Tests the _execute_query function when an error occurs. The
    _execute_query function should raise an InternalServerError
    """

    # Mocks the async-session class
    async_session_mock = AsyncMock(spec_set=AsyncSession)
    async_session_mock.execute = error_mock

    # Mocks the async_sessionmaker aenter function
    async def aenter_mock(_):
        return async_session_mock

    # Mocks the async_sessionmaker class
    session_maker_mock = MagicMock()
    session_maker_mock.__aenter__ = aenter_mock

    # Mocks the database-row-operations class
    database_row_operations_mock = MagicMock(spec=DatabaseRowOperations)
    database_row_operations_mock._session_maker = lambda: session_maker_mock

    # Checks whether the correct error was raised
    with raises(InternalServerError):
        await DatabaseRowOperations._execute_query(
            self=database_row_operations_mock, statement=MagicMock(), is_commit=False
        )


def test_init():
    """
    Tests the DatabaseRowOperations init function for completion. The DatabaseRowOperations init
    function should instantiate a DatabaseRowOperations instance without any errors
    """

    # Mocks and overrides the async_sessionmaker function
    session_maker_mock = MagicMock(spec_set=async_sessionmaker[AsyncSession])

    # Define and instantiates the DatabaseRowOperations class
    db_connection = DatabaseRowOperations(session_maker=session_maker_mock)

    # Checks whether the database-row-operations class was instantiated correctly
    assert db_connection._session_maker == session_maker_mock


@mark.asyncio
async def test_query_row(mocker):
    """
    Tests the query_row function for completion. The query_row function
    should call the required methods without any errors

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mocks the execute_query function
    execute_query_mock = AsyncMock()
    execute_query_mock.return_value = execute_query_mock

    # Mocks the row-result class
    row_result_mock = MagicMock(spec_set=RowResult)
    row_result_mock.return_value = row_result_mock
    mocker.patch.object(row_operations, "RowResult", row_result_mock)

    # Mocks the database-row-operations class
    database_row_operations_mock = MagicMock(spec=DatabaseRowOperations)
    database_row_operations_mock._execute_query = execute_query_mock

    # Mocks the select class
    statement_mock = MagicMock(spec_set=Select)

    # Invokes the query_row functon
    row_result = await DatabaseRowOperations.query_row.__wrapped__.__wrapped__(
        self=database_row_operations_mock, statement=statement_mock
    )

    # Checks whether the required methods were called correctly
    assert row_result == row_result_mock
    assert execute_query_mock.called
    assert row_result_mock.called

    # Checks whether the required parameters were passed correctly
    assert execute_query_mock.call_args.args == (statement_mock, False)
    assert row_result_mock.call_args.args == (execute_query_mock, True)


@mark.asyncio
async def test_query_rows(mocker):
    """
    Tests the query_rows function for completion. The query_rows function
    should call the required methods without any errors

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mocks the execute_query function
    execute_query_mock = AsyncMock()
    execute_query_mock.return_value = execute_query_mock

    # Mocks the row-result class
    row_results_mock = MagicMock(spec_set=RowResults)
    row_results_mock.return_value = row_results_mock
    mocker.patch.object(row_operations, "RowResults", row_results_mock)

    # Mocks the database-row-operations class
    database_row_operations_mock = MagicMock(spec=DatabaseRowOperations)
    database_row_operations_mock._execute_query = execute_query_mock

    # Mocks the select class
    statement_mock = MagicMock(spec_set=Select)

    # Invokes the query_row functon
    row_results = await DatabaseRowOperations.query_rows.__wrapped__.__wrapped__(
        self=database_row_operations_mock, statement=statement_mock
    )

    # Checks whether the required methods were called correctly
    assert row_results == row_results_mock
    assert execute_query_mock.called
    assert row_results_mock.called

    # Checks whether the required parameters were passed correctly
    assert execute_query_mock.call_args.args == (statement_mock, False)
    assert row_results_mock.call_args.args == (execute_query_mock, True)


@mark.asyncio
async def test_stream_rows(mocker):
    """
    Tests the stream_rows function for completion. The stream_rows function
    should call the required methods without any errors

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mocks and overrides the _enforce_base_type_mock function
    enforce_base_type_mock = MagicMock()
    mocker.patch.object(row_operations, "_enforce_base_type", enforce_base_type_mock)

    # Mocks the fetchmany function
    fetch_many_mock = AsyncMock()
    fetch_many_mock.return_value = ["test-value-one"]

    # Mocks the result value
    result_mock = MagicMock()
    result_mock.fetchmany = fetch_many_mock

    # Mocks the stream result value
    stream_result_mock = MagicMock()
    stream_result_mock.scalars.return_value = result_mock

    # Mocks the stream function
    stream_mock = AsyncMock()
    stream_mock.return_value = stream_result_mock

    # Mocks the async-session class
    async_session_mock = AsyncMock(spec_set=AsyncSession)
    async_session_mock.stream = stream_mock

    # Mocks the async_sessionmaker class
    session_maker_mock = MagicMock()
    session_maker_mock.__aenter__.return_value = async_session_mock

    # Mocks the database-row-operations class
    database_row_operations_mock = MagicMock(spec=DatabaseRowOperations)
    database_row_operations_mock._session_maker = lambda: session_maker_mock

    # Mocks the return-type type-var
    return_type_mock = MagicMock()

    # Mocks the select class
    statement_mock = MagicMock(spec_set=Select)

    # Invokes the stream_rows function
    async for rows in DatabaseRowOperations.stream_rows.__wrapped__(
        self=database_row_operations_mock,
        return_type=return_type_mock,
        statement=statement_mock,
        batch=1,
    ):
        assert rows == ["test-value-one"]
        fetch_many_mock.return_value = []

    # Invokes the stream_rows function
    fetch_many_mock.return_value = ["test-value-one"]
    stream_mock.return_value = result_mock
    async for rows in DatabaseRowOperations.stream_rows.__wrapped__(
        self=database_row_operations_mock,
        return_type=return_type_mock,
        statement=statement_mock,
        batch=1,
        is_scalar=False,
    ):
        assert rows == ["test-value-one"]
        fetch_many_mock.return_value = []

    # Checks whether the required methods were called correctly
    assert stream_mock.called
    assert stream_result_mock.scalars.called
    assert result_mock.fetchmany.called
    assert enforce_base_type_mock.called
    assert enforce_base_type_mock.call_args.args[0] == "test-value-one"
    assert enforce_base_type_mock.call_args.args[1] == return_type_mock

    # Checks whether the required parameters were passed correctly
    assert stream_mock.call_args.args[0] == statement_mock


@mark.asyncio
async def test_stream_rows_error():
    """
    Tests the stream_rows function when an error occurs. The
    stream_rows function should raise an InternalServerError
    """

    # Mocks the database-row-operations class
    database_row_operations_mock = MagicMock(spec=DatabaseRowOperations)

    # Mocks the return-type type-var
    return_type_mock = MagicMock()

    # Mocks the select class
    statement_mock = MagicMock(spec_set=Select)

    # Checks whether the correct error was raised
    with raises(InternalServerError):
        async for _ in DatabaseRowOperations.stream_rows.__wrapped__(
            self=database_row_operations_mock,
            return_type=return_type_mock,
            statement=statement_mock,
            batch=1,
        ):
            pass
