from enum import Enum


class TokenType(Enum):
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"

    # lowest precedence
    ADD = "+"
    MINUS = "-"

    # second precedence
    MUL = "*"
    DIV = "/"
    MOD = "%"

    # third precedence
    POW = "^"

    # highest precedence
    FACT = "!"
    LPAREN = "("
    RPAREN = ")"

    ASSIGN = "="
    COMMA = ","


class Token:
    def __init__(self, token_type: TokenType, value=None):
        """Initializes a token."""
        self.token_type = token_type
        self.value = value

    def __repr__(self):
        if self.value:
            return f"Token({self.token_type}, {self.value})"
        else:
            return f"Token({self.token_type})"
