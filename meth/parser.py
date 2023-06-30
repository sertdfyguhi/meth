from . import utils, error
from .token import *
from .nodes import *


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        """Parses a list of tokens."""
        self.tokens = tokens
        self.node = None
        self.i = -1
        self.next()

    def next(self, check_EOF: bool = False, change_curr=True):
        """Advances to the next token."""
        if not change_curr:
            n = self.tokens[self.i + 1] if self.i + 1 < len(self.tokens) else None
            if check_EOF and n == None:
                raise error.SyntaxError("Unexpected end of expression.")

            return n

        self.i += 1
        self.curr = self.tokens[self.i] if self.i < len(self.tokens) else None

        if check_EOF and self.curr == None:
            raise error.SyntaxError("Unexpected end of expression.")

        return self.curr

    def parse(self, disallow_assign=False, args=False, is_paren=False):
        """Parse the inputted tokens."""
        if self.curr == None:
            return None

        self.node = self.curr
        if args:
            res = []

        if self.curr not in [
            TT_PLUS,
            TT_MINUS,
            TT_LBRACKET,
            TT_IDENTIFIER,
            TT_INT,
            TT_FLOAT,
        ]:
            raise error.SyntaxError(f"Unexpected character {self.curr.type}.")

        while self.curr:
            last_tok = self.tokens[self.i - 1] if self.i > 0 else None

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

                # check if its like 2(x + 1)
                is_mul = last_tok in [TT_INT, TT_FLOAT] or getattr(
                    node, "is_paren", False
                )
                is_func = last_tok == TT_IDENTIFIER

                right = self.factor(is_func)
                fr = right if is_func else [right]

                if type(node) != Token and not node.is_paren:
                    node.right = (
                        FunctionNode(node.right, fr) if is_func or is_mul else right
                    )
                else:
                    self.node = FunctionNode(node, fr) if is_func or is_mul else right
            elif self.curr == TT_IDENTIFIER:
                if last_tok in [
                    TT_INT,
                    TT_FLOAT,
                    TT_IDENTIFIER,
                ]:
                    self.binary_op(TT_MUL, self.curr, is_paren=True)
            elif not disallow_assign and self.curr == TT_EQUAL:
                self.node = AssignNode(
                    self.node, Parser(self.tokens[self.i + 1 :]).parse(True)
                )
                self.i = len(self.tokens)
            elif args and self.curr == TT_COMMA:
                self.node.is_paren = is_paren
                res.append(self.node)
                self.node = self.next(True, False)
            else:
                if (last_tok in [TT_INT, TT_FLOAT, TT_IDENTIFIER, TT_RBRACKET]) or (
                    self.next(change_curr=False)
                    in [
                        TT_INT,
                        TT_FLOAT,
                        TT_RBRACKET,
                    ]
                ):
                    raise error.SyntaxError(f"Unexpected character {self.curr}")

            self.next()

        if args:
            res.append(self.node)
        else:
            self.node.is_paren = is_paren

        return self.node if not args else res

    def factor(self, func=False):
        """Parse a factor."""
        self.next(True)

        if TT_LBRACKET in [self.curr, self.tokens[self.i - 1]]:
            if self.curr == TT_LBRACKET:
                self.next(True)

            tokens = []
            opened = 1

            # get all tokens in bracket
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
            # cases like -1, +1
            return UnaryOpNode(self.curr.type, self.factor())
        else:
            raise error.SyntaxError(f"Invalid character {self.curr.type}")

    def binary_op(self, op_type, right=None, stop_at=[], is_paren=False):
        """Parse a binary operation."""
        node = utils.get_final_node(self.node, stop_at=stop_at)
        if not right:
            right = self.factor()

        # if is_paren is True then i shouldn't change it
        if type(node) not in [Token, UnaryOpNode] and not getattr(
            node.right, "is_paren", False
        ):
            node.right = BinaryOpNode(op_type, node.right, right, is_paren)
        else:
            self.node = BinaryOpNode(op_type, node, right, is_paren)
