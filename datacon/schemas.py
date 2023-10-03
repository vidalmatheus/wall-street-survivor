from ninja import Schema


class GetTransactionsSchema(Schema):
    username: str
    password: str
    start_date: str
    end_date: str
