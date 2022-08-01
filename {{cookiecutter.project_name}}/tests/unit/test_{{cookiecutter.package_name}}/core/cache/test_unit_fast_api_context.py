from {{cookiecutter.package_name}}.core.cache import FastApiContext, get_fast_api_context


def test_get_fast_api_context():
    """
    Tests the get_fast_api_context function for completion. The get_fast_api_context
    function should return the fast-api-context instance without any errors
    """

    # Checks whether a fast-api-context instance is returned
    fast_api_context = get_fast_api_context()
    assert isinstance(fast_api_context, FastApiContext)


def test_set_correlation_id_var():
    """
    Tests the FastApiContext class when the correlation-id should be gotten, set, and reset.
    The FastApiContext class should handle the correlation-id operations without any errors
    """

    # Creates a fast-api-context instance and sets a correlation-id
    fast_api_context = FastApiContext()
    fast_api_context.correlation_id_var = "a976b291-fa0e-4b65-8a9b-dcf4d94e3dd2"

    # Checks whether the correlation-id was get and set correctly
    assert fast_api_context.correlation_id_var == "a976b291-fa0e-4b65-8a9b-dcf4d94e3dd2"

    # Checks whether the fast-api-context variables were reset correctly
    fast_api_context.reset()
    assert fast_api_context.correlation_id_var is None
