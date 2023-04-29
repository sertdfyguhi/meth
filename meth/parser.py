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

                self.term()
            elif self.curr in [
                TT_PLUS,
                TT_MINUS,
                TT_MUL,
                TT_DIV,
                TT_POW,
                TT_LBRACKET,
            ]:
                self.term()
            else:
                raise SyntaxError(f"Unexpected token '{self.curr}'")

            self.next()

        return self.node

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

            ast = Parser(tokens).parse()
            ast.is_paren = True

            return ast
        elif self.curr in [TT_INT, TT_FLOAT]:
            return self.curr
        else:
            raise SyntaxError(f"Invalid character {self.curr.type}")

    def term(self):
        if self.curr in [TT_INT, TT_FLOAT]:
            raise SyntaxError(f"Unexpected {self.curr.type}")

        if self.curr in [TT_PLUS, TT_MINUS]:
            op_type = self.curr.type
            right = self.grouped_term()
            # if right == TT_IDENTIFIER:
            #     right = BinaryOpNode(
            #         TT_MUL,
            #     )

            self.node = BinaryOpNode(op_type, self.node, right)
        elif self.curr in [TT_MUL, TT_DIV]:
            node = utils.get_final_node(self.node, [TT_POW])
            op_type = self.curr.type
            right = self.grouped_term()

            if type(node) != Token and not getattr(node.right, "is_paren", True):
                node.right = BinaryOpNode(op_type, node.right, right)
            else:
                self.node = BinaryOpNode(op_type, node, right)
        elif self.curr == TT_POW:
            node = utils.get_final_node(self.node)
            right = self.grouped_term()

            if type(node) != Token:
                node.right = BinaryOpNode(TT_POW, node.right, right)
            else:
                self.node = BinaryOpNode(TT_POW, node, right)
        elif self.curr == TT_LBRACKET:
            node = utils.get_final_node(self.node)
            is_multiply = (self.tokens[self.i - 1] if self.i > 0 else None) in [
                TT_INT,
                TT_FLOAT,
            ] or getattr(node.right, "is_paren", False)
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

        # elif self.curr == TT_IDENTIFIER:
        #     self.node

        return self.node
