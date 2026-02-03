class MethError(Exception):
    def __init__(self, *args: object) -> None:
        self.name = type(self).__name__
        super().__init__(*args)

    def __str__(self) -> str:
        return f"{self.name}: {self.args[0]}"


class MethSyntaxError(MethError):
    pass


class MethNotImplError(MethError):
    pass


class MethVarNotDefinedError(MethError):
    pass


class MethZeroDivError(MethError):
    pass


class MethArgumentError(MethError):
    pass


class MethValueError(MethError):
    pass
