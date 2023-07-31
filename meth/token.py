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

SYMBOLS = {
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
    def __init__(self, tok_type, value: Any = None) -> None:
        """
        Initializes a token.

        Args:
            tok_type: TT_
                Type of token.
            value: Any = None
                Value of the token.
        """
        self.type = tok_type
        self.value = value

    def is_type(self, tok_type) -> bool:
        """
        Checks if token is of type.

        Args:
            tok_type: TT_
                Token type to check for.

        Returns: bool
        """
        return self.type == tok_type

    def is_types(self, tok_types: list) -> bool:
        """
        Checks if token type is in types provided.

        Args:
            tok_types: list[TT_]
                Token types to check for.

        Returns: bool
        """
        return self.type in tok_types

    def __eq__(self, other) -> bool:
        return self.type == other.type and self.value == other.value

    def __repr__(self) -> str:
        return f"{self.type}{f'({self.value})' if self.value else ''}"
