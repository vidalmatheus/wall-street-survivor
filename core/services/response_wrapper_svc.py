from enum import Enum
from functools import cached_property

class Method(Enum):
    GET = "GET"
    POST = "POST"


class ResponseWrapper:
    def __init__(self, request, response):
        self.request = request
        self.response = response

    @cached_property
    def raw(self):
        return self.response.raw

    @cached_property
    def cleaned(self):
        return self.request.clean_response(self.raw)

    @cached_property
    def parsed(self):
        return self.request.parse_response(self.cleaned)
