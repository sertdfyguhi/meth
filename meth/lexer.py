import string

from .builtins import *
from .token import *
from . import error


class Lexer:
    def __init__(self) -> None:
        """Initialize the lexer / tokenizer."""
        pass

    def next(self):
        """Advances to the next character."""
        self.i += 1
        self.curr = self.expr[self.i] if self.i < len(self.expr) else None

    def tokenize(self, expr: str):
        """Tokenizes the expression."""
        self.expr = expr
        self.i = -1
        self.next()

        tokens = []

        while self.curr:
            if self.curr == " ":
                pass
            elif self.curr in string.digits:
                tokens.append(self.number())
            elif self.curr in OPERATORS:
                tokens.append(Token(OPERATORS[self.curr]))
            elif self.curr in string.ascii_letters:
                tokens += self.identifier()
            elif self.curr in SPECIAL_CONST_SYM:
                tokens.append(Token(TT_IDENTIFIER, self.curr))
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
            if is_builtin(identifier)
            else [Token(TT_IDENTIFIER, idf) for idf in identifier]
        )
