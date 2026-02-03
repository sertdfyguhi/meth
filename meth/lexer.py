from .builtin import CONSTANTS
from .token import *
from .error import *
import string

ALLOWED_CHARS = string.ascii_letters + "".join(CONSTANTS.keys())


class Lexer:
    def __init__(self, expr):
        self.expr = expr
        self.i = -1
        self.next()

    def next(self):
        self.i += 1
        self.curr = self.expr[self.i] if len(self.expr) > self.i else None
        return self.curr

    def peek(self):
        return self.expr[self.i + 1] if len(self.expr) > self.i + 1 else None

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
            elif self.curr in ALLOWED_CHARS:
                tokens.append(self.tokenize_identifier())
                continue
            elif self.curr in "+-/%^()=!,":
                # token type value is the same as operator character
                tokens.append(Token(self.curr))
            elif self.curr == "*":
                # allow for ** syntax for power
                if self.peek() == "*":
                    self.next()
                    tokens.append(Token(TT_POW))
                else:
                    tokens.append(Token(TT_MUL))
            else:
                raise MethSyntaxError(f'Unrecognized character "{self.curr}".')

            self.next()

        return tokens

    def tokenize_number(self):
        number = ""

        # check self.curr too to ensure its not None
        while self.curr and self.curr in string.digits + ".":
            # if there are multiple dots
            if self.curr == "." and "." in number:
                raise MethSyntaxError('Unexpected ".".')

            number += self.curr
            self.next()

        return Token(TT_NUMBER, float(number) if "." in number else int(number))

    def tokenize_identifier(self):
        identifier = ""

        while self.curr and self.curr in ALLOWED_CHARS:
            identifier += self.curr
            self.next()

        return Token(TT_IDENTIFIER, identifier)
