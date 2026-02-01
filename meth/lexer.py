from .token import *
from .error import *
import string

OPERATORS = "+-*/()="


class Lexer:
    def __init__(self, expr):
        self.expr = expr
        self.i = -1
        self.next()

    def next(self):
        self.i += 1
        self.curr = self.expr[self.i] if len(self.expr) > self.i else None
        return self.curr

    def tokenize(self):
        tokens = []

        while self.curr:
            # ignore whitespaces
            if self.curr == " ":
                self.next()
                continue

            if self.curr in string.digits + ".":
                tokens.append(self.tokenize_number())
                continue
            elif self.curr in string.ascii_letters:
                tokens.append(Token(TT_IDENTIFIER, self.curr))
            elif self.curr in OPERATORS:
                # token type value is the same as operator character
                tokens.append(Token(self.curr))
            else:
                raise MethSyntaxError(f'unrecognized character "{self.curr}"')

            self.next()

        return tokens

    def tokenize_number(self):
        number = ""

        # check self.curr too to ensure its not None
        while self.curr and self.curr in string.digits + ".":
            # if there are multiple dots
            if self.curr == "." and "." in number:
                raise MethSyntaxError("multiple dots in number")

            number += self.curr
            self.next()

        return Token(TT_NUMBER, float(number) if "." in number else int(number))
