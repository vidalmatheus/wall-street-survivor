import pytest
from core.wss.wss_api import WssAPI
from core.models import WssLogin, Transaction
from core.exceptions import NonePasswordError


def test_repr(wss_api):
    username = wss_api.username
    assert wss_api.__repr__() == f"{WssAPI.__name__}_{username}"


def test_wss_api_new_login():
    username = "steve_rogers"
    password = "abc123"
    WssAPI(username=username, password=password)
    wss_login_object = WssLogin.objects.filter(username=username).first()
    assert wss_login_object.password == password


def test_wss_api_unknow_username_and_none_password():
    username = "steve_rogers"
    password = None
    with pytest.raises(NonePasswordError, match=NonePasswordError.message):
        WssAPI(username=username, password=password)


def test_fetch_last_transactions(mock_wss_login, mock_wss_fetch_transactions, wss_api):
    transactions_list = wss_api.fetch_last_transactions("10-20-2023", "10-22-2023")
    transactions_stored_list = Transaction.objects.filter(wss_login=wss_api.wss_login_object)
    for transaction in transactions_list:
        assert transaction
    assert mock_wss_login.call_count == 1
    assert len(transactions_list) == len(transactions_stored_list)


def test_get_last_transactions(wss_api, wss_transactions):
    quantity = 2
    transactions = wss_api.get_last_transactions(quantity=quantity)
    assert len(transactions) <= quantity

