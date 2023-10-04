from ninja import Schema


class FetchTransactionsSchema(Schema):
    username: str
    password: str
    start_date: str
    end_date: str
