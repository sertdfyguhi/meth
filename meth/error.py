class BaseError(Exception):
    def __init__(self, *args: object) -> None:
        self.name = type(self).__name__
        super().__init__(*args)

    def __str__(self) -> str:
        return f"{self.name}: {self.args[0]}"


class SyntaxError(BaseError):
    pass


class NotImplError(BaseError):
    pass


class VarNotDefinedError(BaseError):
    pass


class ZeroDivError(BaseError):
    pass


class ArgumentError(BaseError):
    pass
