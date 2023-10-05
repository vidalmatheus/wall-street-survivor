import pytest
from model_bakery import baker

from core.models import WssLogin, Transaction
from core.wss.wss_api import WssAPI
from core.wss.wss_endpoints import (
    Login as WssLoginRequestObject,
    GetTransactions as WssFetchTransactionsRequestObject,
)
from tests.mock_data_response import mock_response_wss_fetch_transactions


@pytest.fixture(autouse=True)
def db_autouse(db):
    pass


@pytest.fixture
def wss_login():
    return baker.make(WssLogin, username="tony_stark", password="mack3")


@pytest.fixture
def wss_transactions(wss_login):
    return [
        baker.make(Transaction, wss_login=wss_login),
        baker.make(Transaction, wss_login=wss_login),
        baker.make(Transaction, wss_login=wss_login),
    ]


@pytest.fixture
def wss_api(wss_login):
    return WssAPI(username=wss_login.username, password=wss_login.password)


@pytest.fixture
def mock_wss_login(requests_mock, wss_api):
    return requests_mock.post(
        url=f"{WssLogin.BASE_URL}/{WssLoginRequestObject.endpoint}",
        text="<html><body>Mocked HTML</body></html>",
        status_code=200,
    )


@pytest.fixture
def mock_wss_login_credentals_error(requests_mock, wss_api):
    return requests_mock.post(
        url=f"{WssLogin.BASE_URL}/{WssLoginRequestObject.endpoint}",
        text=(
            """
                <html>
                    <body>
                        <div class='validation-summary-errors is-alert-color'>
                            <ul>
                                <li>You have entered the wrong Username/Password combination</li>
                            </ul>
                        </div>
                    </body>
                </html>
            """
        ),
        status_code=200,
    )


@pytest.fixture
def mock_wss_fetch_transactions(requests_mock, wss_api):
    return requests_mock.get(
        url=f"{WssLogin.BASE_URL}/{WssFetchTransactionsRequestObject.endpoint}",
        json=mock_response_wss_fetch_transactions.response,
        status_code=200,
    )
