import requests
from requests.adapters import HTTPAdapter, Retry

from core.exceptions import WssConnectionError
from core.models import WssLogin
from core.services.response_wrapper_svc import ResponseWrapper


class BaseRequest:
    def __init__(self):
        self.cookies = {}
        self.session = self._build_session()

    def _build_session(self):
        session = requests.Session()
        retry_params = dict(total=3, backoff_factor=1, raise_on_status=False)
        retry_strategy = Retry(**retry_params)
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def _request(self, method, endpoint, params, json, data):
        url = f"{WssLogin.BASE_URL}/{endpoint}"
        try:
            response = self.session.request(
                method=method, url=url, params=params, json=json, cookies=self.cookies, timeout=60, data=data
            )
        except ConnectionError:
            error_msg = f"wss {method} {url} with {params=} {json=} {data=} connection error"
            raise WssConnectionError(error_msg)

        response.raise_for_status()

        return response

    def send(self, params=None, json=None, data=None):
        response = self._request(method=self.method, endpoint=self.endpoint, params=params, json=json, data=data)

        return ResponseWrapper(self, response)


class AuthenticatedBaseRequest(BaseRequest):
    def __init__(self, client):
        super().__init__()
        self.cookies = client.get_auth_token
