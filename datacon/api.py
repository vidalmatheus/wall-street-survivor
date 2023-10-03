from django.http import JsonResponse
from ninja import NinjaAPI

api = NinjaAPI()


@api.get("/hello")
def hello(request):
    return JsonResponse({
        "message": "Hey there"
    })


@api.get("/wallstreetsurvivor")
def get_last_transactions(request):
    return JsonResponse({
        "message": "WallStreet"
    })
