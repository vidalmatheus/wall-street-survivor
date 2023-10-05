import pytest

from core.exceptions import UnknowUsernameError
from core.services import transactions_svc


def test_get_last_transactions(wss_login, wss_transactions):
    username = wss_login.username
    transctions = transactions_svc.get_last_transactions(username=username)
    assert len(transctions) == len(wss_transactions)


def test_get_last_transactions_unknow_username():
    with pytest.raises(UnknowUsernameError):
        transactions_svc.get_last_transactions(username="unknow_user")
