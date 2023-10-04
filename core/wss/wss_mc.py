from time import time
from types import SimpleNamespace

from django.core.cache import cache

from core.models import WssLogin
from core.wss.wss_endpoints import Login

TOKEN_NAME = ".FASTRAKMVC"


class WssMC:
    cachekey_prefix = "WSS_TOKEN_"

    def api_data(self, username):
        password = WssLogin.objects.filter(username=username).values_list("password", flat=True).first()
        wss_login_resp = Login().send(username, password)
        cookies = wss_login_resp.response.request._cookies
        data = dict(cookies)
        cookies_object_list = list(cookies)
        timeout = cookies_object_list[0].expires - int(time())  # seconds of timeout
        self._set(username, data, timeout)
        return data

    def _set(self, key, value, timeout):
        cached_key = f"{self.cachekey_prefix}{key}"
        cache.set(cached_key, value, timeout)
