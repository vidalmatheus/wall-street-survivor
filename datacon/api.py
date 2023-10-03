from django.http import JsonResponse
from ninja import NinjaAPI

from core.wss.wss_api import WssAPI
from datacon.schemas import GetTransactionsSchema

api = NinjaAPI()


@api.get("/hello")
def hello(request):
    return JsonResponse({"message": "Hey there"})


@api.post("/wallstreetsurvivor")
def get_last_transactions(request, params: GetTransactionsSchema):
    transactions_list = WssAPI().get_transactions(start_date=params.start_date, end_date=params.end_date)
    return JsonResponse(transactions_list, safe=False)
