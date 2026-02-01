class BaseError(Exception):
    def __init__(self, *args: object) -> None:
        self.name = type(self).__name__
        super().__init__(*args)

    def __str__(self) -> str:
        return f"{self.name}: {self.args[0]}"


class MethSyntaxError(BaseError):
    pass


class MethNotImplError(BaseError):
    pass


class MethVarNotDefinedError(BaseError):
    pass


class MethZeroDivError(BaseError):
    pass


class MethArgumentError(BaseError):
    pass
