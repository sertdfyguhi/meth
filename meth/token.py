from typing import Any

TT_IDENTIFIER = "IDENTIFIER"
TT_LBRACKET = "LEFT_BRACKET"
TT_RBRACKET = "RIGHT_BRACKET"
TT_EQUAL = "EQUAL"
TT_COMMA = "COMMA"

TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MULTIPLY"
TT_DIV = "DIVIDE"
TT_MOD = "MODULO"
TT_POW = "POWER"

TT_FLOAT = "FLOAT"
TT_INT = "INTEGER"

OPERATORS = {
    "(": TT_LBRACKET,
    ")": TT_RBRACKET,
    "=": TT_EQUAL,
    ",": TT_COMMA,
    "+": TT_PLUS,
    "-": TT_MINUS,
    "*": TT_MUL,
    "/": TT_DIV,
    "%": TT_MOD,
    "^": TT_POW,
}


class Token:
    def __init__(self, token_type, value: Any = None) -> None:
        """
        Initializes a token.

        Args:
            token_type: TT_
                Type of token.
            value: Any = None
                Value of the token.
        """
        self.type = token_type
        self.value = value

    def __eq__(self, other) -> bool:
        if type(other) == Token:
            return self.type == other.type and self.value == other.value
        else:
            return self.type == other

    def __repr__(self) -> str:
        return f"{self.type}{f'({self.value})' if self.value else ''}"
