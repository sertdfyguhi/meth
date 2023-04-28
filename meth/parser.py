from .token import *
from .nodes import *
from . import utils


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.node = None
        self.i = -1
        self.next()

    def next(self, check_EOF: bool = False):
        self.i += 1
        self.curr = self.tokens[self.i] if self.i < len(self.tokens) else None

        if check_EOF and self.curr == None:
            raise SyntaxError("Unexpected end of expression.")

        return self.curr

    def parse(self):
        self.node = self.curr

        while self.curr:
            if self.curr in [TT_INT, TT_FLOAT]:
                if self.next() == None:
                    return self.node

                self.binary_op()
            elif self.curr in [TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_POW]:
                self.binary_op()

            self.next()

        return self.node

    def binary_op(self):
        if self.curr in [TT_INT, TT_FLOAT]:
            return self.curr
            # raise SyntaxError(f"Unexpected {self.curr.type}")

        if self.curr in [TT_PLUS, TT_MINUS]:
            op_type = self.curr.type
            self.next(True)
            right = self.binary_op()

            self.node = BinaryOpNode(op_type, self.node, right)
        elif self.curr in [TT_MUL, TT_DIV]:
            node, _ = utils.get_last_right_node(self.node, [TT_POW])
            op_type = self.curr.type
            self.next(True)
            right = self.binary_op()

            if type(node) != Token:
                node.right = BinaryOpNode(op_type, node.right, right)
            else:
                self.node = BinaryOpNode(op_type, node, right)
        elif self.curr == TT_POW:
            node, _ = utils.get_last_right_node(self.node)
            self.next(True)
            right = self.binary_op()

            if type(node) != Token:
                node.right = BinaryOpNode(TT_POW, node.right, right)
            else:
                self.node = BinaryOpNode(TT_POW, node, right)
        elif self.curr == TT_LBRACKET:
            self.next(True)
            tokens = []

            while self.curr != TT_RBRACKET:
                tokens.append(self.curr)
                self.next(True)

            return Parser(tokens).parse()

        # elif self.curr == TT_IDENTIFIER:
        #     self.node

        return self.node
