import requests
from requests.adapters import HTTPAdapter, Retry
from core.exceptions import WssConnectionError
from core.services.response_wrapper_svc import ResponseWrapper

class BaseRequest:
    def __init__(self, client):
        self.client = client
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
        url = f"{self.client.base_url}/{endpoint}"
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                cookies=self.cookies,
                timeout=60,
                data=data
            )
        except ConnectionError as ex:
            error_msg = f"wss {method} {url} with {params=} {json=} {data=} connection error"
            raise WssConnectionError(error_msg) from ex

        response.raise_for_status()

        return response

    def send(self, params=None, json=None, data=None):
        response = self._request(
            method=self.method,
            endpoint=self.endpoint,
            params=params,
            json=json,
            data=data
        )

        return ResponseWrapper(self, response)


class AuthenticatedBaseRequest(BaseRequest):
    def __init__(self, client):
        super().__init__(client)
        # self.cookies = client.get_auth_token()
        self.cookies = { # just testing
            ".FASTRAKMVC": "F6E40F5BBA77C8FDFA7D327B6A6C9FB26CA42CBCD1DA5EC22781EFCF5FE0D0978249F61E5730939152405847070A1BF3A27E36878578708D92E3A5785A7B9DAB05AB6419996B8E004B27CFB43A32F6C64A184FF7BCC81B384256A9894C52FB7DAAA68A83"
        }
