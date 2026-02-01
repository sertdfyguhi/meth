from .error import *
from .token import *
from .node import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = -1
        self.next()

    def next(self):
        self.i += 1
        self.curr = self.tokens[self.i] if len(self.tokens) > self.i else None
        return self.curr

    def peek(self):
        return self.tokens[self.i + 1] if len(self.tokens) > self.i + 1 else None

    def parse(self):
        return self.parse_lowest()

    def parse_parentheses(self):
        self.next()

        node = self.parse_add_minus()
        if self.curr.token_type != TT_RPAREN:
            raise MethSyntaxError('expected ")"')

        return node

    # parse highest priority, terms
    def parse_highest(self):
        if self.curr.token_type in [TT_NUMBER, TT_IDENTIFIER, TT_LPAREN]:
            if self.curr.token_type == TT_NUMBER:
                node = NumberNode(self.curr.value)
            elif self.curr.token_type == TT_IDENTIFIER:
                node = IdentifierNode(self.curr.value)
            else:
                node = self.parse_parentheses()

            self.next()

            # also handle terms like: 3x, ax, 3(1 + 2), (1 + 2)(3 + 4)
            while self.curr and self.curr.token_type in [TT_IDENTIFIER, TT_LPAREN]:
                if self.curr.token_type == TT_IDENTIFIER:
                    right = IdentifierNode(self.curr.value)
                else:
                    right = self.parse_parentheses()

                node = BinaryOpNode(node, TT_MUL, right)
                self.next()

            return node
        elif self.curr.token_type in [TT_ADD, TT_MINUS]:
            operator = self.curr.token_type
            self.next()
            return UnaryOpNode(operator, self.parse_highest())
        else:
            raise MethSyntaxError(f'unexpected token "{self.curr}"')

    def parse_mul_div(self):
        node = self.parse_highest()

        while self.curr and self.curr.token_type in [TT_MUL, TT_DIV]:
            operator = self.curr.token_type
            self.next()
            node = BinaryOpNode(node, operator, self.parse_highest())

        return node

    def parse_add_minus(self):
        node = self.parse_mul_div()

        while self.curr and self.curr.token_type in [TT_ADD, TT_MINUS]:
            operator = self.curr.token_type
            self.next()
            node = BinaryOpNode(node, operator, self.parse_mul_div())

        return node

    # for parsing assignments
    def parse_lowest(self):
        node = self.parse_add_minus()

        while self.curr and self.curr.token_type == TT_ASSIGN:
            self.next()
            node = AssignNode(node, self.parse_add_minus())

        return node
