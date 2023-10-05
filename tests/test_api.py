import json

import pytest

from core.exceptions import LoginCredentialsError, UnknowUsernameError
from datacon import api
from datacon.schemas import FetchTransactionsSchema


def test_hello(rf):
    req = rf.get("/hello")
    resp = api.hello(req)
    assert resp.status_code == 200
    json_resp = json.loads(resp.content)
    assert json_resp["message"] == "Hey there"


def test_fetch_last_transactions(rf, mocker):
    mock_transactions_list = {
        "actions": "",
        "transaction_type": "Market - Buy",
        "symbol": "AAPL",
        "quantity": 2,
        "type": "Equities",
        "price_status": "$171.5500",
        "fee": "1.00",
        "date_time": "10/04/2023 - 09:31",
    }
    mocker.patch("core.wss.wss_api.WssAPI.fetch_last_transactions", return_value=mock_transactions_list)
    params = {"username": "tony_stark", "password": "mack3", "start_date": "2023-10-01", "end_date": "2023-10-04"}
    req = rf.post("/wallstreet/survivor")
    resp = api.fetch_last_transactions(req, params=FetchTransactionsSchema.parse_obj(params))
    assert resp.status_code == 200
    json_resp = json.loads(resp.content)
    assert json_resp == mock_transactions_list


def test_fetch_last_transactions_credentials_error(rf, mocker):
    mocker.patch("core.wss.wss_api.WssAPI.fetch_last_transactions", side_effect=LoginCredentialsError)
    params = {"username": "tony_stark", "password": "mack3", "start_date": "2023-10-01", "end_date": "2023-10-04"}
    req = rf.post("/wallstreet/survivor")
    resp = api.fetch_last_transactions(req, params=FetchTransactionsSchema.parse_obj(params))
    assert resp.status_code == 400
    json_resp = json.loads(resp.content)
    assert json_resp["message"] == LoginCredentialsError().message


def test_fetch_last_transactions_wrong_datetime_format(rf):
    params = {"username": "tony_stark", "password": "mack3", "start_date": "10-01-2023", "end_date": "10-04-2023"}
    req = rf.post("/wallstreet/survivor")
    with pytest.raises(ValueError):
        api.fetch_last_transactions(req, params=FetchTransactionsSchema.parse_obj(params))


def test_get_last_transactions(rf, mocker, wss_transactions):
    mocker.patch("core.services.transactions_svc.get_last_transactions", return_value=wss_transactions)
    req = rf.get("/get_last_transactions")
    resp = api.get_last_transactions(req, username="tony_stark")
    assert resp.status_code == 200
    json_resp = json.loads(resp.content)
    assert len(json_resp) == len(wss_transactions)


def test_get_last_transactions_unknow_user(rf, mocker, wss_transactions):
    mocker.patch("core.services.transactions_svc.get_last_transactions", side_effect=UnknowUsernameError)
    req = rf.get("/get_last_transactions")
    resp = api.get_last_transactions(req, username="tony_stark")
    assert resp.status_code == 400
    json_resp = json.loads(resp.content)
    assert json_resp["message"] == UnknowUsernameError().message
