from .token import *
import string


class Lexer:
    def __init__(self, expr: str) -> None:
        self.expr = expr
        self.i = -1
        self.next()

    def next(self):
        self.i += 1
        self.curr = self.expr[self.i] if self.i < len(self.expr) else None

    def tokenize(self):
        tokens = []

        while self.curr:
            if self.curr == " ":
                pass
            elif self.curr in string.digits:
                tokens.append(self.number())
            elif self.curr in string.ascii_letters:
                tokens.append(Token(TT_IDENTIFIER, self.curr))
            elif self.curr == "(":
                tokens.append(Token(TT_LBRACKET))
            elif self.curr == ")":
                tokens.append(Token(TT_RBRACKET))
            elif self.curr == "=":
                tokens.append(Token(TT_EQUAL))
            elif self.curr == "+":
                tokens.append(Token(TT_PLUS))
            elif self.curr == "-":
                tokens.append(Token(TT_MINUS))
            elif self.curr == "*":
                tokens.append(Token(TT_MUL))
            elif self.curr == "/":
                tokens.append(Token(TT_DIV))
            elif self.curr == "^":
                tokens.append(Token(TT_POW))
            else:
                raise SyntaxError(f"Invalid character '{self.curr}'")

            self.next()

        return tokens

    def number(self) -> Token:
        number = ""
        is_float = False

        while self.curr and self.curr in string.digits + ".":
            if self.curr == ".":
                if is_float:
                    raise SyntaxError("Unexpected '.'")
                else:
                    is_float = True

            number += self.curr

            self.next()

        self.i -= 1
        self.curr = self.expr[self.i]

        return Token(
            TT_FLOAT if is_float else TT_INT, (float if is_float else int)(number)
        )
