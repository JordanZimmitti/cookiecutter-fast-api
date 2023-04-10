from requests import Session
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
        username: str | None = None,
        password: str | None = None,
    ):
        """
        Client used for hitting API server endpoints
        """

        # Sets the API url
        self.api_url = api_url

        # Sets the credentials to access the API
        self.auth_url = auth_url
        self.username = username
        self.password = password

        # Creates the client session
        self.session = Session()
        self.session.mount(api_url, HTTPAdapter(pool_connections=2, max_retries=2))
        self.session.verify = False

    def login(self):

        # Checks whether the auth_url exists
        if self.auth_url is None:
            raise RuntimeError("'auth_url' cannot be None")

        # Creates the endpoint for logging in
        endpoint = f"{self.api_url}{self.auth_url}"

        # Creates the credentials' dictionary for logging in
        credentials = {"username": self.username, "password": self.password}

        # Hits the endpoint and gets the response
        response = self.session.request("POST", endpoint, data=credentials)
        if response.status_code != 200:
            raise Exception(f"{str(response)}")

        # Adds the access token to the header
        response_data = response.json()
        token = response_data["access_token"]
        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": "{{cookiecutter.project_name}}-client/0.1.0",
        }
        self.session.headers.update(headers)

    def delete(self, endpoint, params: dict = None):
        return self._request(endpoint, "DELETE", params=params)

    def get(self, endpoint, params: dict = None):
        return self._request(endpoint, "GET", params=params)

    def head(self, endpoint, params: dict = None):
        return self._request(endpoint, "HEAD", params=params)

    def post(self, endpoint, data, params: dict = None):
        return self._request(endpoint, "POST", data=data, params=params)

    def put(self, endpoint, data, params: dict = None):
        return self._request(endpoint, "PUT", data=data, params=params)

    def patch(self, endpoint, data, params: dict = None):
        return self._request(endpoint, "PATCH", data=data, params=params)

    def _request(self, endpoint, method, data: dict = None, params: dict = None):
        full_url = f"{self.api_url}{endpoint}"
        response = self.session.request(method, full_url, json=data, params=params)
        return response
