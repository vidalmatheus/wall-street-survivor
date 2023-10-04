class WssConnectionError(Exception):
    pass


class NonePasswordError(Exception):
    message = "Unknown username and null password"

    def __init__(self):
        super().__init__(self.message)


class WrongCredentialsError(Exception):
    message = "You have entered the wrong Username/Password combination"

    def __init__(self):
        super().__init__(self.message)
