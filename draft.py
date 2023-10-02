import requests
import json
from bs4 import BeautifulSoup

USERNAME = "matheusvidal"
PASSWORD = "Vid@l123"

def login():
    url = "https://app.wallstreetsurvivor.com/login"
    payload = {
        "UserName": USERNAME,
        "Password": PASSWORD
    }
    resp = requests.post(
        url=url,
        data=payload,
    )
    print(resp)
    cookies = dict(resp.request._cookies)
    for k, v in cookies.items():
        print(f"{k} : {v}")
    return cookies


def _parse_transactions(html):
    soup = BeautifulSoup(html, 'html.parser')
    transaction_rows = soup.find_all('tr')
    transactions_list = []
    for row in transaction_rows:
        columns = row.find_all('td')
        if len(columns) == 8:
            transaction = {
                'actions': columns[0].text.strip(),
                'transaction_type': columns[1].text.strip(),
                'symbol': columns[2].text.strip(),
                'quantity': int(columns[3].text.strip()),
                'type': columns[4].text.strip(),
                'price_status': columns[5].text.strip(),
                'fee': columns[6].text.strip(),
                'date_time': columns[7].text.strip()
            }
            transactions_list.append(transaction)

    print(json.dumps(transactions_list, indent=4))
    return transactions_list


def get_transactions(cookies, start_date, end_date):
    url = "https://app.wallstreetsurvivor.com/account/gettransactions"
    params = {
        "pageIndex": 0,
        "pageSize": 12,
        "sortField": "CreateDate",
        "sortDirection": "DESC",
        "transactionType": 1,
        "startDate": start_date,
        "endDate": end_date
    }
    resp = requests.get(
        url=url,
        params=params,
        cookies=cookies
    )
    print(resp)
    print(resp.json().keys())
    return _parse_transactions(resp.json()["Html"])


cookies = login()
transactions = get_transactions(cookies, "10-01-2023", "10-03-2023")
