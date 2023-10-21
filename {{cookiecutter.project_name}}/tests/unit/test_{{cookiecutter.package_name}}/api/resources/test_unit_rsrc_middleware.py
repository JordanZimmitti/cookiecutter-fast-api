from {{cookiecutter.package_name}}.api.resources.rsrc_middleware import RequestMetadataModel


def test_request_metadata_model():
    """
    Tests the request metadata pydantic model for completion. The request metadata
    pydantic model should instantiate a new request metadata instance without any
    errors
    """

    # Mocks the health data
    request_metadata_data = {"method": "GET", "url": "https://test-url", "userAgent": "test-agent"}

    # Checks whether the request metadata model was instantiated correctly
    request_metadata_model = RequestMetadataModel(**request_metadata_data)
    assert request_metadata_model.method == "GET"
    assert request_metadata_model.url == "https://test-url"
    assert request_metadata_model.user_agent == "test-agent"
