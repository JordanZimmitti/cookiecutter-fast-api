from unittest.mock import MagicMock

from sqlalchemy import Result, Row

from {{cookiecutter.package_name}}.core.database.row_operations import RowResults


def test_all():
    """
    Tests the all function for completion. The all function
    should call the required methods without any errors
    """

    # Mocks the row class
    row_mock = MagicMock(Row)

    # Mocks the result class
    result_mock = MagicMock(spec_set=Result)
    result_mock.all.return_value = [row_mock]

    # Mocks the row-results class
    row_results_mock = MagicMock(spec=RowResults)
    row_results_mock._is_scalar = False
    row_results_mock._result = result_mock

    # Invokes the all functon
    rows = RowResults.all(self=row_results_mock, return_type=MagicMock())

    # Checks whether the required methods were called correctly
    assert result_mock.all.called
    assert rows == [row_mock]


def test_fetch():
    """
    Tests the fetch function for completion. The fetch function
    should call the required methods without any errors
    """

    # Mocks the row class
    row_mock = MagicMock(Row)

    # Mocks the result class
    result_mock = MagicMock(spec_set=Result)
    result_mock.fetchmany.return_value = [row_mock]

    # Mocks the row-results class
    row_results_mock = MagicMock(spec=RowResults)
    row_results_mock._is_scalar = False
    row_results_mock._result = result_mock

    # Invokes the fetch functon
    rows = RowResults.fetch(self=row_results_mock, return_type=MagicMock(), size=1)

    # Checks whether the required methods were called correctly
    assert result_mock.fetchmany.called
    assert rows == [row_mock]


def test_init():
    """
    Tests the RowResults init function for completion. The RowResults init
    function should instantiate a RowResults instance without any errors
    """

    # Mocks the result class
    result_mock = MagicMock(spec_set=Result)
    result_mock.scalars.return_value = result_mock
    result_mock.unique = result_mock

    # Define and instantiates the RowResult class
    row_result_with_scalar = RowResults(result_mock, True)
    row_result_without_scalar = RowResults(result_mock, False)

    # Checks whether the row-result class with scalars was instantiated correctly
    row_result_with_scalar._is_scalar = True
    row_result_with_scalar._unique_result = result_mock
    row_result_with_scalar._result = result_mock

    # Checks whether the row-result class without scalars was instantiated correctly
    row_result_without_scalar._is_scalar = False
    row_result_without_scalar._unique_result = result_mock
    row_result_without_scalar._result = result_mock


def test_unique():
    """
    Tests the unique function for completion. The unique function
    should call the required methods without any errors
    """

    # Mocks the row class
    new_result_mock = MagicMock(spec_set=Result)
    new_result_mock.unique = MagicMock

    # Mocks the result class
    unique_result_mock = MagicMock(spec_set=Result)
    unique_result_mock.return_value = new_result_mock

    # Mocks the result class
    result_mock = MagicMock(spec_set=Result)
    result_mock.unique = unique_result_mock

    # Mocks the row-results class
    row_results_mock = MagicMock(spec=RowResults)
    row_results_mock._is_scalar = False
    row_results_mock._unique_result = unique_result_mock

    # Invokes the first functon
    row_results = RowResults.unique(self=row_results_mock)

    # Checks whether the required methods were called correctly
    assert unique_result_mock.called
    assert row_results._result == new_result_mock
