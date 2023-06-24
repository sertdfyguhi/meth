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


class Token:
    def __init__(self, token_type, value=None) -> None:
        self.type = token_type
        self.value = value

    def __eq__(self, other: object) -> bool:
        if type(other) is Token:
            return self.type == other.type and self.value == other.value
        else:
            return self.type == other

    def __repr__(self) -> str:
        return f"{self.type}({self.value})"
