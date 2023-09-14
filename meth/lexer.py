import string

from .builtins import *
from .token import *
from . import error


class Lexer:
    def __init__(self) -> None:
        """Initialize the lexer / tokenizer."""
        pass

    def _next(self):
        """Advances to the next character."""
        self.i += 1
        self.curr = self.expr[self.i] if self.i < len(self.expr) else None

    def tokenize(self, expr: str) -> list[Token]:
        """
        Tokenizes the expression.

        Args:
            expr: str
                Expression to tokenize.

        Returns: list[Token]
        """
        self.expr = expr
        self.i = -1
        self._next()

        tokens = []

        while self.curr:
            if self.curr in " \t\r\n":
                self._next()
            elif self.curr in string.digits:
                tokens.append(self._number())
            elif self.curr in string.ascii_letters:
                tokens += self._identifier()
            elif self.curr in SYMBOLS:
                tokens.append(Token(SYMBOLS[self.curr]))
                self._next()
            elif self.curr in SPECIAL_CONST_SYM:
                tokens.append(Token(TT_IDENTIFIER, self.curr))
                self._next()
            else:
                raise error.SyntaxError(f"Invalid character '{self.curr}'")

        return tokens

    def _number(self) -> Token:
        """Tokenizes a number."""
        number = ""
        is_float = False

        while self.curr and self.curr in string.digits + ".":
            if self.curr == ".":
                if is_float:
                    raise error.SyntaxError("Unexpected '.'")

                is_float = True

            number += self.curr
            self._next()

        if is_float:
            return Token(TT_FLOAT, float(number))
        else:
            return Token(TT_INT, int(number))

    def _identifier(self) -> list[Token]:
        """Tokenizes an identifier."""
        identifier = ""

        while self.curr and (
            self.curr in string.ascii_letters or self.curr in string.digits
        ):
            identifier += self.curr
            self._next()

        return (
            [Token(TT_IDENTIFIER, identifier)]
            if is_builtin(identifier)
            else [Token(TT_IDENTIFIER, idf) for idf in identifier]
        )
