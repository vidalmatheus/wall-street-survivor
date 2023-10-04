import json

from django.core import serializers
from django.http import JsonResponse
from ninja import NinjaAPI

from core.exceptions import NonePasswordError, WrongCredentialsError
from core.wss.wss_api import WssAPI
from datacon.schemas import FetchTransactionsSchema

api = NinjaAPI()


@api.get("/hello")
def hello(request):
    return JsonResponse({"message": "Hey there"})


@api.post("/wallstreetsurvivor")
def fetch_last_transactions(request, params: FetchTransactionsSchema):
    """
    Fetch the last 12 transactions using a given username/password directly on the WallStreetSurvivor platform
    """
    try:
        transactions_list = WssAPI(username=params.username, password=params.password).fetch_last_transactions(
            start_date=params.start_date, end_date=params.end_date
        )
    except WrongCredentialsError as e:
        return JsonResponse({"message": e.message}, status=400)
    else:
        return JsonResponse(transactions_list, safe=False)


@api.get("/get_last_transactions")
def get_last_transactions(request, username: str, quantity: int = 3):
    """
    Get last transactions from an username stored in the database
    """
    try:
        transactions_list = WssAPI(username=username).get_last_transactions(quantity=quantity)
    except NonePasswordError as e:
        return JsonResponse({"message": e.message}, status=400)
    else:
        serialized_transactions = json.loads(serializers.serialize("json", transactions_list))
        return JsonResponse(serialized_transactions, safe=False)
