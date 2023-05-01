from .token import *
from .nodes import *
from . import utils


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        """Parser."""
        self.tokens = tokens
        self.node = None
        self.i = -1
        self.next()

    def next(self, check_EOF: bool = False, change_curr=True):
        """Advances to the next token."""
        if not change_curr:
            return self.tokens[self.i + 1] if self.i + 1 < len(self.tokens) else None

        self.i += 1
        self.curr = self.tokens[self.i] if self.i < len(self.tokens) else None

        if check_EOF and self.curr == None:
            raise SyntaxError("Unexpected end of expression.")

        return self.curr

    def parse(self, disallow_assign=False, args=False, is_paren=True):
        """Parse the inputted tokens."""
        self.node = self.curr
        if args:
            self.res = []

        if self.curr not in [
            TT_PLUS,
            TT_MINUS,
            TT_LBRACKET,
            TT_IDENTIFIER,
            TT_INT,
            TT_FLOAT,
        ]:
            raise SyntaxError(f"Unexpected character {self.curr}")

        while self.curr:
            if self.curr in [TT_PLUS, TT_MINUS]:
                op_type = self.curr.type
                right = self.factor()

                self.node = (
                    UnaryOpNode(op_type, right)
                    if self.node in [TT_PLUS, TT_MINUS]
                    else BinaryOpNode(op_type, self.node, right)
                )
            elif self.curr in [TT_MUL, TT_DIV, TT_MOD]:
                self.binary_op(self.curr.type, stop_at=[TT_POW])
            elif self.curr == TT_POW:
                self.binary_op(TT_POW)
            elif self.curr == TT_LBRACKET:
                node = utils.get_final_node(self.node)

                last_tok = self.tokens[self.i - 1] if self.i > 0 else None
                is_multiply = last_tok in [
                    TT_INT,
                    TT_FLOAT,
                    TT_IDENTIFIER,
                ] or (
                    getattr(node.right, "is_paren", False)
                    if type(node) != Token
                    else False
                )
                right = self.factor(is_multiply)

                if type(node) != Token:
                    node.right = (
                        FunctionNode(node.right, right) if is_multiply else right
                    )
                else:
                    self.node = FunctionNode(node, right) if is_multiply else right
            elif self.curr == TT_IDENTIFIER:
                if (self.tokens[self.i - 1] if self.i > 0 else None) in [
                    TT_INT,
                    TT_FLOAT,
                    TT_IDENTIFIER,
                ]:
                    self.binary_op(TT_MUL, self.curr)
            elif not disallow_assign and self.curr == TT_EQUAL:
                self.node = AssignNode(
                    self.node, Parser(self.tokens[self.i + 1 :]).parse(True)
                )
                self.i = len(self.tokens)
            elif args and self.curr == TT_COMMA:
                self.node.is_paren = is_paren
                self.res.append(self.node)
                self.node = self.next(change_curr=False)
            else:
                if (
                    (self.tokens[self.i - 1] if self.i > 0 else None)
                    in [TT_INT, TT_FLOAT, TT_IDENTIFIER, TT_RBRACKET]
                ) or (
                    self.next(change_curr=False)
                    in [
                        TT_INT,
                        TT_FLOAT,
                        TT_RBRACKET,
                    ]
                ):
                    raise SyntaxError(f"Unexpected character {self.curr}")

            self.next()

        if args:
            self.res.append(self.node)
        else:
            self.node.is_paren = is_paren
        return self.node if not args else self.res

    def factor(self, func=False):
        """Parse a factor."""
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

            return Parser(tokens).parse(True, func, True)
        elif self.curr in [TT_INT, TT_FLOAT, TT_IDENTIFIER]:
            return self.curr
        elif self.curr in [TT_PLUS, TT_MINUS]:
            return UnaryOpNode(self.curr.type, self.factor())
        else:
            raise SyntaxError(f"Invalid character {self.curr.type}")

    def binary_op(self, op_type, right=None, stop_at=[]):
        """Parse a binary operation."""
        node = utils.get_final_node(self.node, stop_at=stop_at)
        if not right:
            right = self.factor()

        if type(node) != Token and not getattr(node.right, "is_paren", False):
            node.right = BinaryOpNode(op_type, node.right, right)
        else:
            self.node = BinaryOpNode(op_type, node, right)
