from core.exceptions import UnknowUsernameError
from core.models import Transaction, WssLogin


def _get_wss_login_from_username(username):
    try:
        wss_login = WssLogin.objects.get(username=username)
    except WssLogin.DoesNotExist:
        raise UnknowUsernameError
    else:
        return wss_login


def get_last_transactions(username, max_quantity=12):
    wss_login = _get_wss_login_from_username(username)
    transactions = Transaction.objects.filter(wss_login=wss_login).order_by("-date_time")[:max_quantity]
    return transactions
