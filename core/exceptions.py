class WssConnectionError(Exception):
    pass


class NonePasswordError(Exception):
    message = "Unknown username and null password"

    def __init__(self, message=None):
        if message:
            self.message = message
        super().__init__(self.message)


class LoginCredentialsError(Exception):
    message = "You have entered the wrong Username/Password combination"

    def __init__(self, message=None):
        if message:
            self.message = message
        super().__init__(self.message)
