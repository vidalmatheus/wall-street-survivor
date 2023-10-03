from bs4 import BeautifulSoup

def parse_transactions_from_html(html):
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
