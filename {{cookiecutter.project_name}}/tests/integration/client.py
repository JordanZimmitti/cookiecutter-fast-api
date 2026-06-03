from typing import Any, Dict

from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

# Disable warning about insecure request
disable_warnings(InsecureRequestWarning)


class ApiClient:
    def __init__(
        self,
        api_url: str,
        auth_url: str | None = None,
        user_id: str | None = None,
        api_key: str | None = None,
    ):
        """
        Client used for hitting API server endpoints
        """

        # Sets the API url
        self.api_url = api_url

        # Sets the credentials to access the API
        self.auth_url = auth_url
        self.user_id = user_id
        self.api_key = api_key

        # Creates the client session
        self.session = Session()
        self.session.mount(api_url, HTTPAdapter(pool_connections=2, max_retries=2))
        self.session.verify = False

        # Saves the login tokens
        self._access_token: str | None = None
        self._refresh_token: str | None = None

    @property
    def refresh_token(self) -> str | None:
        """
        Property that gets the refresh token for
        getting a new access token

        :return: The API refresh token
        """
        return self._refresh_token

    def login(self):

        # Checks whether the auth_url exists
        if self.auth_url is None:
            raise RuntimeError("'auth_url' cannot be None")

        # Creates the endpoint for logging in
        endpoint = f"{self.api_url}{self.auth_url}"

        # Creates the credentials' dictionary for logging in
        credentials = {"userId": self.user_id, "apiKey": self.api_key}

        # Hits the endpoint and gets the response
        response = self.session.request("POST", endpoint, data=credentials)
        if response.status_code != 200:
            raise Exception(f"{str(response)}")

        # Extracts the access and refresh tokens from the response
        response_data = response.json()
        access_token = response_data.get("accessToken")
        refresh_token = response_data.get("refreshToken")

        # Adds the access and refresh tokens to the class state
        self._access_token = access_token
        self._refresh_token = refresh_token

        # Adds the access token to the header
        headers = {
            "Authorization": f"Bearer {access_token}",
            "User-Agent": "{{cookiecutter.project_name}}-client/0.1.0",
        }
        self.session.headers.update(headers)

    def delete(self, endpoint: str, params: Dict[str, Any] | None = None) -> Response:
        return self._request(endpoint, "DELETE", params=params)

    def get(self, endpoint: str, params: Dict[str, Any] | None = None) -> Response:
        return self._request(endpoint, "GET", params=params)

    def head(self, endpoint: str, params: Dict[str, Any] | None = None) -> Response:
        return self._request(endpoint, "HEAD", params=params)

    def post(
        self,
        endpoint: str,
        files: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
        json: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
    ) -> Response:
        return self._request(endpoint, "POST", files=files, data=data, json=json, params=params)

    def put(
        self,
        endpoint: str,
        data: Dict[str, Any] | None = None,
        json: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
    ) -> Response:
        return self._request(endpoint, "PUT", data=data, json=json, params=params)

    def patch(
        self,
        endpoint: str,
        data: Dict[str, Any] | None = None,
        json: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
    ) -> Response:
        return self._request(endpoint, "PATCH", data=data, json=json, params=params)

    def _request(
        self,
        endpoint: str,
        method: str,
        files: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
        json: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
    ) -> Response:
        full_url = f"{self.api_url}{endpoint}"
        return self.session.request(
            method, full_url, files=files, data=data, json=json, params=params
        )
