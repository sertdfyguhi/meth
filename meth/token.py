TT_IDENTIFIER = "IDENTIFIER"
TT_RBRACKET = "RIGHT_BRACKET"
TT_LBRACKET = "LEFT_BRACKET"

TT_FLOAT = "FLOAT"
TT_INT = "INTEGER"

TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MULTIPLY"
TT_DIV = "DIVIDE"


class Token:
    def __init__(self, token_type, value=None) -> None:
        self.token_type = token_type
        self.value = value

    def __eq__(self, __value: object) -> bool:
        return self.token_type == __value.token_type and self.value == __value.value

    def __repr__(self) -> str:
        return f"{self.token_type}({self.value})"
