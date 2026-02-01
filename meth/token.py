TT_NUMBER = "NUMBER"
TT_IDENTIFIER = "IDENTIFIER"

TT_LPAREN = "("
TT_RPAREN = ")"

TT_ADD = "+"
TT_MINUS = "-"
TT_MUL = "*"
TT_DIV = "/"


class Token:
    def __init__(self, token_type, value=None):
        self.token_type = token_type
        self.value = value

    def __repr__(self):
        return f"Token({self.token_type}, {self.value})"


class OpToken(Token):
    def __init__(self, op_type):
        super().__init__(op_type, None)
