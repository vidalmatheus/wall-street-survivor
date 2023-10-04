from datetime import datetime

from ninja import Schema
from pydantic import validator


class FetchTransactionsSchema(Schema):
    username: str
    password: str
    start_date: str
    end_date: str

    @validator("start_date")
    def convert_date_format_start(cls, value):
        try:
            input_date = datetime.strptime(value, "%Y-%m-%d")
            formatted_date = input_date.strftime("%m-%d-%Y")
            return formatted_date
        except ValueError:
            raise ValueError("Invalid date format. Use 'YYYY-MM-DD'.")

    @validator("end_date")
    def convert_date_format_end(cls, value):
        try:
            input_date = datetime.strptime(value, "%Y-%m-%d")
            formatted_date = input_date.strftime("%m-%d-%Y")

            return formatted_date
        except ValueError:
            raise ValueError("Invalid date format. Use 'YYYY-MM-DD'.")
