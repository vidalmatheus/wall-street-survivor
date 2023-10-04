import json
from django.core import serializers
from django.http import JsonResponse
from ninja import NinjaAPI

from core.wss.wss_api import WssAPI
from datacon.schemas import FetchTransactionsSchema

api = NinjaAPI()


@api.get("/hello")
def hello(request):
    return JsonResponse({"message": "Hey there"})


@api.post("/wallstreetsurvivor")
def fetch_last_transactions(request, params: FetchTransactionsSchema):
    transactions_list = WssAPI(username=params.username, password=params.password).fetch_last_transactions(
        start_date=params.start_date, end_date=params.end_date
    )
    return JsonResponse(transactions_list, safe=False)


@api.get("/get_last_transactions")
def get_last_transactions(request, username: str, password: str = None, quantity: int = 12):
    transactions_list = WssAPI(username=username, password=password).get_last_transactions(quantity=quantity)
    serialized_transactions = json.loads(serializers.serialize("json", transactions_list))
    return JsonResponse(serialized_transactions, safe=False)
