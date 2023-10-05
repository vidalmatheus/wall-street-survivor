from time import time

from bs4 import BeautifulSoup
from django.core.cache import cache

from core.exceptions import LoginCredentialsError
from core.models import WssLogin
from core.wss.wss_endpoints import Login

TOKEN_NAME = ".FASTRAKMVC"


class WssMC:
    cachekey_prefix = "WSS_TOKEN_"

    def api_data(self, username):
        wss_login_object = WssLogin.objects.get(username=username)
        password = wss_login_object.password
        wss_login_resp = Login().send(username, password)
        html_content = wss_login_resp.response.content
        error_message = self._parse_error_message(html_content)
        if error_message:
            wss_login_object.delete()
            raise LoginCredentialsError(error_message)
        cookies = wss_login_resp.response.request._cookies
        data = dict(cookies)
        cookies_object_list = list(cookies)
        if not cookies_object_list:
            timeout = 20 * 60  # default timeout just in case
        else:
            timeout = cookies_object_list[0].expires - int(time())  # seconds of timeout
        self._set(username, data, timeout)
        return data

    def _parse_error_message(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        div_element = soup.find("div", class_="validation-summary-errors is-alert-color")
        if not div_element:
            return None
        error_message = div_element.find("li").text.strip()
        return error_message

    def _set(self, key, value, timeout):
        cached_key = f"{self.cachekey_prefix}{key}"
        cache.set(cached_key, value, timeout)
