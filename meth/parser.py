from .token import *
from .nodes import *
from . import utils


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.node = None
        self.i = -1
        self.next()

    def next(self, check_EOF: bool = False, change_curr=True):
        if not change_curr:
            return self.tokens[self.i + 1] if self.i + 1 < len(self.tokens) else None

        self.i += 1
        self.curr = self.tokens[self.i] if self.i < len(self.tokens) else None

        if check_EOF and self.curr == None:
            raise SyntaxError("Unexpected end of expression.")

        return self.curr

    def parse(self, disallow_assign=False):
        self.node = self.curr

        while self.curr:
            if self.curr in [TT_PLUS, TT_MINUS]:
                op_type = self.curr.type
                right = self.grouped_term()

                self.node = (
                    UnaryOpNode(op_type, right)
                    if self.node in [TT_PLUS, TT_MINUS]
                    else BinaryOpNode(op_type, self.node, right)
                )
            elif self.curr in [TT_MUL, TT_DIV]:
                self.binary_op(self.curr.type, stop_at=[TT_POW])
            elif self.curr == TT_POW:
                self.binary_op(TT_POW)
            elif self.curr == TT_LBRACKET:
                node = utils.get_final_node(self.node)
                is_multiply = (self.tokens[self.i - 1] if self.i > 0 else None) in [
                    TT_INT,
                    TT_FLOAT,
                    TT_IDENTIFIER,
                ] or (
                    getattr(node.right, "is_paren", False)
                    if type(node) != Token
                    else False
                )

                right = self.grouped_term()

                if is_multiply:
                    if type(node) != Token:
                        node.right = BinaryOpNode(TT_MUL, node.right, right, True)
                    else:
                        self.node = BinaryOpNode(TT_MUL, node, right, True)
                else:
                    if type(node) != Token:
                        node.right = right
                    else:
                        self.node = right
            elif self.curr == TT_IDENTIFIER:
                if (self.tokens[self.i - 1] if self.i > 0 else None) in [
                    TT_INT,
                    TT_FLOAT,
                    TT_IDENTIFIER,
                ]:
                    self.binary_op(TT_MUL, self.curr)
            elif self.curr == TT_EQUAL:
                if disallow_assign:
                    raise SyntaxError("Assigning is disallowed.")

                self.node = AssignNode(
                    self.node, Parser(self.tokens[self.i + 1 :]).parse(True)
                )
                self.i = len(self.tokens)
            else:
                if self.curr == TT_RBRACKET or (
                    self.next(change_curr=False)
                    or TT_INT  # check for end of expression
                ) in [
                    TT_INT,
                    TT_FLOAT,
                ]:
                    raise SyntaxError(f"Unexpected character {self.curr}")

            self.next()

        return self.node

    # TODO: use a better name
    def grouped_term(self):
        self.next(True)

        if TT_LBRACKET in [self.curr, self.tokens[self.i - 1]]:
            if self.curr == TT_LBRACKET:
                self.next(True)

            tokens = []
            opened = 1

            while opened:
                tokens.append(self.curr)
                self.next(True)

                if self.curr == TT_RBRACKET:
                    opened -= 1
                elif self.curr == TT_LBRACKET:
                    opened += 1

            ast = Parser(tokens).parse(True)
            ast.is_paren = True

            return ast
        elif self.curr in [TT_INT, TT_FLOAT, TT_IDENTIFIER]:
            return self.curr
        elif self.curr in [TT_PLUS, TT_MINUS]:
            return UnaryOpNode(self.curr.type, self.grouped_term())
        else:
            raise SyntaxError(f"Invalid character {self.curr.type}")

    def binary_op(self, op_type, right=None, stop_at=[]):
        node = utils.get_final_node(self.node, stop_at=stop_at)
        if not right:
            right = self.grouped_term()

        if type(node) != Token and not getattr(node.right, "is_paren", True):
            node.right = BinaryOpNode(op_type, node.right, right)
        else:
            self.node = BinaryOpNode(op_type, node, right)
