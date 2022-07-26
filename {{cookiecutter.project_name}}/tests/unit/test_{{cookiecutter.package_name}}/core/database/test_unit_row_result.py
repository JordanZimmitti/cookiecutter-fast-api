from unittest.mock import MagicMock

from pytest import raises
from sqlalchemy import Result, Row

from {{cookiecutter.package_name}}.core.database.row_operations import RowResult
from {{cookiecutter.package_name}}.exceptions import InternalServerError


def test_first():
    """
    Tests the first function for completion. The first function
    should call the required methods without any errors
    """

    # Mocks the row class
    row_mock = MagicMock(Row)

    # Mocks the result class
    result_mock = MagicMock(spec_set=Result)
    result_mock.first.return_value = row_mock

    # Mocks the row-result class
    row_result_mock = MagicMock(spec=RowResult)
    row_result_mock._is_scalar = False
    row_result_mock._result = result_mock

    # Invokes the first functon
    row = RowResult.first(self=row_result_mock, return_type=MagicMock())

    # Checks whether the required methods were called correctly
    assert result_mock.first.called
    assert row == row_mock


def test_init():
    """
    Tests the RowResult init function for completion. The RowResult init
    function should instantiate a RowResult instance without any errors
    """

    # Mocks the result class
    result_mock = MagicMock(spec_set=Result)
    result_mock.scalars.return_value = result_mock

    # Define and instantiates the RowResult class
    row_result_with_scalar = RowResult(result_mock, True)
    row_result_without_scalar = RowResult(result_mock, False)

    # Checks whether the row-result class with scalars was instantiated correctly
    row_result_with_scalar._is_scalar = True
    row_result_with_scalar._result = result_mock

    # Checks whether the row-result class without scalars was instantiated correctly
    row_result_without_scalar._is_scalar = False
    row_result_without_scalar._result = result_mock


def test_one():
    """
    Tests the one function for completion. The one function
    should call the required methods without any errors
    """

    # Mocks the row class
    row_mock = MagicMock(Row)

    # Mocks the result class
    result_mock = MagicMock(spec_set=Result)
    result_mock.one.return_value = row_mock

    # Mocks the row-result class
    row_result_mock = MagicMock(spec=RowResult)
    row_result_mock._is_scalar = False
    row_result_mock._result = result_mock

    # Invokes the one functon
    row = RowResult.one(self=row_result_mock, return_type=MagicMock())

    # Checks whether the required methods were called correctly
    assert result_mock.one.called
    assert row == row_mock


def test_one_error():
    """
    Tests the one function when an error occurs. The one
    function should raise an InternalServerError
    """

    # Mocks the result class
    result_mock = MagicMock(spec_set=Result)
    result_mock.one = Exception("mock error")

    # Mocks the row-result class
    row_result_mock = MagicMock(spec=RowResult)
    row_result_mock._is_scalar = False
    row_result_mock._result = result_mock

    # Checks whether the correct error was raised
    with raises(InternalServerError):
        RowResult.one(self=row_result_mock, return_type=MagicMock())
