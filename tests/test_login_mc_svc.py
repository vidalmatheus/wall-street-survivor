import pytest
from django.core.cache import cache

from core.services import login_mc_svc
from core.wss.wss_mc import WssMC
from core.exceptions import LoginCredentialsError


def test_wss_mc(mock_wss_login, wss_login):
    cache.clear()
    username = wss_login.username
    login_mc_svc.get_data(WssMC, username)
    login_mc_svc.get_data(WssMC, username)
    assert mock_wss_login.call_count == 1


def test_wss_mc_credentials_error(mock_wss_login_credentals_error, wss_login):
    cache.clear()
    username = wss_login.username
    with pytest.raises(LoginCredentialsError, match=LoginCredentialsError.message):
        login_mc_svc.get_data(WssMC, username)
    

def test_get_data_none_key():
    assert login_mc_svc.get_data(WssMC, None) is None
