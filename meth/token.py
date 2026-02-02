TT_NUMBER = "NUMBER"
TT_IDENTIFIER = "IDENTIFIER"

TT_ADD = "+"
TT_MINUS = "-"

TT_MUL = "*"
TT_DIV = "/"
TT_MOD = "%"

TT_POW = "^"

TT_FACT = "!"
TT_LPAREN = "("
TT_RPAREN = ")"
TT_ASSIGN = "="
TT_COMMA = ","


class Token:
    def __init__(self, token_type, value=None):
        self.token_type = token_type
        self.value = value

    def __repr__(self):
        return f"Token({self.token_type}, {self.value})"
