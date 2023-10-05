from datetime import datetime

from memoize import memoize

from commons.dateutils import to_tz
from core.exceptions import NonePasswordError
from core.models import Transaction, WssLogin
from core.services import login_mc_svc
from core.wss import wss_endpoints
from core.wss.wss_mc import WssMC


class WssAPI:
    def __init__(self, username, password=None):
        self.username = username
        self._resolve_password(password)

    def __repr__(self):
        return f"{self.__class__.__name__}_{self.username}"

    def _resolve_password(self, password):
        try:
            wss_login_object = WssLogin.objects.get(username=self.username)
        except WssLogin.DoesNotExist:
            wss_login_object = self._create_wss_login(password)

        self.wss_login_object = wss_login_object
        self.password = wss_login_object.password

    def _create_wss_login(self, password):
        if not password:
            raise NonePasswordError
        return WssLogin.objects.create(username=self.username, password=password)

    @property
    def get_auth_token(self):
        return login_mc_svc.get_data(
            provider=WssMC,
            key=self.username,
        )

    @memoize(timeout=5)
    def fetch_last_transactions(self, start_date, end_date):
        resp = wss_endpoints.GetTransactions(self).send(start_date, end_date)
        transacitons_list = resp.parsed
        transaciton_objects_to_create_list = []
        timezone = "US/Eastern"
        for transaction in transacitons_list:
            date_time = datetime.strptime(transaction["date_time"], "%m/%d/%Y - %H:%M")
            date_time_tz = to_tz(date_time, timezone)
            transaciton_objects_to_create_list.append(
                Transaction(
                    wss_login=self.wss_login_object,
                    actions=transaction["actions"],
                    transaction_type=transaction["transaction_type"],
                    symbol=transaction["symbol"],
                    quantity=transaction["quantity"],
                    type=transaction["type"],
                    price_status=transaction["price_status"],
                    fee=transaction["fee"],
                    date_time=date_time_tz,
                    timezone=timezone,
                )
            )
        Transaction.objects.bulk_create(transaciton_objects_to_create_list, ignore_conflicts=True)
        return transacitons_list

    def get_last_transactions(self, quantity=12):
        transactions = Transaction.objects.filter(wss_login=self.wss_login_object).order_by("-date_time")[:quantity]
        return transactions
