import string

from .builtins import BUILTINS
from .token import *
from . import error


TOKENS = {
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


class Lexer:
    def __init__(self, expr: str) -> None:
        """Lexer."""
        self.expr = expr
        self.i = -1
        self.next()

    def next(self):
        """Advances to the next character."""
        self.i += 1
        self.curr = self.expr[self.i] if self.i < len(self.expr) else None

    def tokenize(self):
        """Tokenizes the inputted expression."""
        tokens = []

        while self.curr:
            if self.curr == " ":
                pass
            elif self.curr in string.digits:
                tokens.append(self.number())
            elif self.curr in string.ascii_letters:
                tokens += self.identifier()
            elif self.curr in TOKENS:
                tokens.append(Token(TOKENS[self.curr]))
            else:
                raise error.SyntaxError(f"Invalid character '{self.curr}'")

            self.next()

        return tokens

    def number(self) -> Token:
        """Tokenizes a number."""
        number = ""
        is_float = False

        while self.curr and self.curr in string.digits + ".":
            if self.curr == ".":
                if is_float:
                    raise error.SyntaxError("Unexpected '.'")
                is_float = True

            number += self.curr
            self.next()

        self.i -= 1
        self.curr = self.expr[self.i]

        return Token(
            TT_FLOAT if is_float else TT_INT, (float if is_float else int)(number)
        )

    def identifier(self) -> list[Token]:
        """Tokenizes an identifier."""
        identifier = ""

        while self.curr and (
            self.curr in string.ascii_letters or self.curr in string.digits
        ):
            identifier += self.curr
            self.next()

        self.i -= 1
        self.curr = self.expr[self.i]

        return (
            [Token(TT_IDENTIFIER, identifier)]
            if identifier in BUILTINS
            else [Token(TT_IDENTIFIER, id) for id in identifier]
        )
