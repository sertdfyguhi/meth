TT_IDENTIFIER = "IDENTIFIER"
TT_RBRACKET = "RIGHT_BRACKET"
TT_LBRACKET = "LEFT_BRACKET"
TT_EQUAL = "EQUAL"

TT_FLOAT = "FLOAT"
TT_INT = "INTEGER"

TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MULTIPLY"
TT_DIV = "DIVIDE"
TT_POW = "POWER"


class Token:
    def __init__(self, token_type, value=None) -> None:
        self.type = token_type
        self.value = value

    def __eq__(self, __value: object) -> bool:
        if type(__value) == Token:
            return self.type == __value.type and self.value == __value.value
        else:
            return self.type == __value

    def __repr__(self) -> str:
        return f"{self.type}({self.value})"
