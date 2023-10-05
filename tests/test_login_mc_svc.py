import time
from http.cookiejar import Cookie, CookieJar
from types import SimpleNamespace

import pytest
from freezegun import freeze_time
from requests.cookies import RequestsCookieJar

from core.exceptions import LoginCredentialsError
from core.services import login_mc_svc
from core.wss.wss_mc import WssMC


def test_wss_mc(mock_wss_login, wss_login):
    username = wss_login.username
    login_mc_svc.get_data(WssMC, username)
    login_mc_svc.get_data(WssMC, username)
    assert mock_wss_login.call_count == 1


def test_wss_mc_credentials_error(mock_wss_login_credentals_error, wss_login):
    username = wss_login.username
    with pytest.raises(LoginCredentialsError, match=LoginCredentialsError().message):
        login_mc_svc.get_data(WssMC, username)


def test_get_data_none_key():
    assert login_mc_svc.get_data(WssMC, None) is None


@freeze_time("2023-10-04 16:43:34", tz_offset=-3)
def test_wss_mc_timeout(mocker, wss_login):
    timeout = 100
    cookie = Cookie(
        version=0,  # Cookie version (0 for Netscape-style cookies)
        name="abc",
        value="value",
        expires=int(time.time()) + timeout,  # Expiration time in seconds
        port=None,
        port_specified=False,
        domain="example.com",  # Specify the domain of the cookie
        domain_specified=True,
        domain_initial_dot=False,
        path="/",  # Specify the path for the cookie
        path_specified=True,
        secure=False,  # Whether the cookie is secure (HTTPS only)
        discard=False,
        comment=None,
        comment_url=None,
        rest=None,
    )
    requests_cookie_jar = RequestsCookieJar()
    requests_cookie_jar.set_cookie(cookie)
    login_wss_resp = SimpleNamespace(
        response=SimpleNamespace(
            content="<html><body>Mocked HTML</body></html>", request=SimpleNamespace(_cookies=requests_cookie_jar)
        )
    )
    mocker.patch("core.wss.wss_endpoints.Login.send", return_value=login_wss_resp)
    mock_wssmc__set = mocker.patch("core.wss.wss_mc.WssMC._set")
    username = wss_login.username
    login_mc_svc.get_data(WssMC, username)
    mock_wssmc__set.assert_called_once_with(username, {"abc": "value"}, timeout)
