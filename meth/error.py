class MethError(Exception):
    """Base class for all Meth errors."""

    pass


class MethSyntaxError(MethError):
    """Invalid syntax in expression."""

    pass


class MethNotImplError(MethError):
    """Feature hasn't been implemented."""

    pass


class MethVarNotDefinedError(MethError):
    """Variable hasn't been defined."""

    pass


class MethZeroDivError(MethError):
    """Divide by zero."""

    pass


class MethArgumentError(MethError):
    """Invalid arguments passed to function."""

    pass


class MethValueError(MethError):
    """Invalid value."""

    pass
