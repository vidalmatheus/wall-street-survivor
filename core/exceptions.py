class WssConnectionError(Exception):
    pass


class UnknowUsernameError(Exception):
    def __init__(self, message="Unknow user"):
        self.message = message
        super().__init__(self.message)


class LoginCredentialsError(Exception):
    def __init__(self, message="You have entered the wrong Username/Password combination"):
        self.message = message
        super().__init__(self.message)
