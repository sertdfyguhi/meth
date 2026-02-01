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
        ast = self.parse_add_minus()
        return ast

    # parse highest priority, numbers
    def parse_highest(self):
        if self.curr.token_type in [TT_NUMBER, TT_IDENTIFIER]:
            node = (
                NumberNode(self.curr.value)
                if self.curr.token_type == TT_NUMBER
                else IdentifierNode(self.curr.value)
            )
            self.next()

            # also handle terms like: 3x, ax
            while self.curr and self.curr.token_type == TT_IDENTIFIER:
                node = BinaryOpNode(node, TT_MUL, IdentifierNode(self.curr.value))
                self.next()

            return node
        elif self.curr.token_type == TT_LPAREN:
            self.next()

            expr_ast = self.parse_add_minus()
            if self.curr.token_type != TT_RPAREN:
                raise ValueError('expected ")"')

            self.next()

            return expr_ast
        else:
            raise NotImplementedError()

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
