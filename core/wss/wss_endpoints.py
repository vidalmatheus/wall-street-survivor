from bs4 import BeautifulSoup

from core.services.response_wrapper_svc import Method
from core.wss.base import AuthenticatedBaseRequest, BaseRequest


class Login(BaseRequest):
    method = Method.POST
    endpoint = "login"

    def send(self, username, password):
        data = {"username": username, "password": password}
        return super().send(data=data)


class GetTransactions(AuthenticatedBaseRequest):
    method = Method.GET
    endpoint = "account/gettransactions"

    def send(
        self,
        start_date,
        end_date,
        page_index=0,
        page_size=12,
        sort_field="CreateDate",
        sort_direction="DESC",
        transaction_type=1,
    ):
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

    def _parse_transactions_from_html(self, html):
        soup = BeautifulSoup(html, "html.parser")
        transaction_rows = soup.find_all("tr")
        transactions_list = []
        for row in transaction_rows:
            columns = row.find_all("td")
            if len(columns) == 8:
                transaction = {
                    "actions": columns[0].text.strip(),
                    "transaction_type": columns[1].text.strip(),
                    "symbol": columns[2].text.strip(),
                    "quantity": int(columns[3].text.strip()),
                    "type": columns[4].text.strip(),
                    "price_status": columns[5].text.strip(),
                    "fee": columns[6].text.strip(),
                    "date_time": columns[7].text.strip(),
                }
                transactions_list.append(transaction)

        return transactions_list

    def clean_response(self, response):
        return response["Html"]

    def parse_response(self, clean_response):
        return self._parse_transactions_from_html(clean_response)
