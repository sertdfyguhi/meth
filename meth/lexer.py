from .token import Token, TokenType
from .builtin import CONSTANTS
from .error import *
import string

ALLOWED_VARIABLE_CHARS = string.ascii_letters + "".join(CONSTANTS.keys())


class Lexer:
    def __init__(self, expr: str) -> None:
        """
        Initializes the lexer.

        Args:
            expr: str
                The expression to tokenize.
        """
        self.expr = expr
        self.i = -1
        self._next()

    def _next(self):
        self.i += 1
        self.curr = self.expr[self.i] if len(self.expr) > self.i else None
        return self.curr

    def _peek(self):
        return self.expr[self.i + 1] if len(self.expr) > self.i + 1 else None

    def tokenize(self) -> list[Token]:
        """
        Tokenizes the expression.

        Returns: list[Token]
        """
        tokens = []

        while self.curr:
            # ignore whitespaces
            if self.curr == " ":
                self._next()
                continue

            if self.curr in string.digits + ".":
                tokens.append(self._tokenize_number())
                continue
            elif self.curr in ALLOWED_VARIABLE_CHARS:
                tokens.append(self._tokenize_identifier())
                continue
            elif self.curr in "+-/%^()=!,":
                # token type value is the same as operator character
                tokens.append(Token(TokenType(self.curr)))
            elif self.curr == "*":
                # allow for ** syntax for power
                if self._peek() == "*":
                    self._next()
                    tokens.append(Token(TokenType.POW))
                else:
                    tokens.append(Token(TokenType.MUL))
            else:
                raise MethSyntaxError(f'Unrecognized character "{self.curr}".')

            self._next()

        return tokens

    def _tokenize_number(self):
        number = ""

        # check self.curr too to ensure its not None
        while self.curr and self.curr in string.digits + ".":
            # if there are multiple dots
            if self.curr == "." and "." in number:
                raise MethSyntaxError('Unexpected ".".')

            number += self.curr
            self._next()

        return Token(TokenType.NUMBER, float(number) if "." in number else int(number))

    def _tokenize_identifier(self):
        identifier = ""

        while self.curr and self.curr in ALLOWED_VARIABLE_CHARS:
            identifier += self.curr
            self._next()

        return Token(TokenType.IDENTIFIER, identifier)
