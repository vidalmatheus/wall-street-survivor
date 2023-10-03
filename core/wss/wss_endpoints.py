from core.wss.base import BaseRequest
from core.services.response_wrapper_svc import Method


class Login(BaseRequest):
    method = Method.POST
    endpoint = "login"

    def send(self, data):
        return super().send(data=data)

    def clean_response(self, response):
        return response

    def parse_response(self, clean_response):
        return clean_response


class GetTransactions(BaseRequest):
    method = Method.GET
    endpoint = "account/gettransactions"

    def send(self, start_date, end_date, page_index=0, page_size=12, sort_field="CreateDate", sort_direction="DESC", transaction_type=1):
        params = {
            "pageIndex": page_index,
            "pageSize": page_size,
            "sortField": sort_field,
            "sortDirection": sort_direction,
            "transactionType": transaction_type,
            "startDate": start_date,
            "endDate": end_date,
        }
        return super().send(params=params)
