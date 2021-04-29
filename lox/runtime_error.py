from lox.token import Token


class LoxRuntimeError(RuntimeError):

    def __init__(self, token: Token, message: str):
        super(message)
        self.token = token
