from .builtins import is_builtin
from . import utils, error
from .token import *
from .nodes import *

NUMBERS = [TT_INT, TT_FLOAT]
OPERATORS = [TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_POW, TT_MOD]


class Parser:
    def __init__(self) -> None:
        """Initialize the parser."""
        pass

    def _next(self, check_EOF: bool = False, change_curr: bool = True):
        """Advances to the next token."""
        self.i += 1
        token = self.tokens[self.i] if self.i < len(self.tokens) else None

        if check_EOF and token is None:
            raise error.SyntaxError("Unexpected end of expression.")

        if change_curr:
            self.curr = token
        else:
            self.i -= 1

        return token

    def parse(
        self,
        tokens: list[Token],
    ) -> BaseNode:
        """
        Parse the inputted tokens.

        Args:
            tokens: list[Token]
                List of tokens to parse.

        Returns: Node
        """
        self.tokens = tokens
        self.i = -1
        self._next()

        res = self._term()
        intermediate = []
        assign_left = None
        in_args = [False]
        args = []

        while self.curr:
            if self.curr.is_types(OPERATORS):
                op = self.curr

                self._next(check_EOF=True)

                right = self._term()

                if op.is_types([TT_PLUS, TT_MINUS]):
                    res = BinaryOpNode(op, res, right)
                    continue
                elif op.is_types([TT_MUL, TT_DIV]):
                    leaf = utils.get_leaf_node_right(res, True, [TT_POW, TT_MOD])
                else:
                    leaf = utils.get_leaf_node_right(res, True)

                if type(leaf) == Token or leaf.is_paren:
                    res = BinaryOpNode(op, leaf, right)
                else:
                    leaf.right = BinaryOpNode(op, leaf.right, right)
            elif self.curr.is_type(TT_LBRACKET):
                try:
                    if self.tokens[self.i - 1].is_type(TT_IDENTIFIER):
                        in_args.append(True)
                except IndexError:
                    # ignore when previous token does not exist
                    pass

                intermediate.append(res)
                self._next()
                res = self._term()
            elif self.curr.is_type(TT_RBRACKET):
                if res is None:
                    raise error.SyntaxError("Unexpected end of parentheses.")
                elif len(intermediate) == 0:
                    raise error.SyntaxError("Unexpected right bracket.")

                last_intermediate = intermediate.pop()
                res.is_paren = True

                if last_intermediate:
                    leaf = utils.get_leaf_node_right(last_intermediate)

                    if in_args[-1]:
                        if res:
                            args.append(res)

                        if type(leaf) == Token:
                            leaf = FunctionNode(leaf, args)
                        else:
                            leaf.right = FunctionNode(leaf.right, args)

                        in_args.pop()
                        args = []
                    elif type(leaf) == Token or leaf.is_paren:
                        leaf = BinaryOpNode(TT_MUL, leaf, res, is_paren=True)
                    elif leaf.right is None:
                        leaf.right = res
                    elif type(leaf.right) == UnaryOpNode:
                        leaf.right.left = res
                    else:
                        leaf.right = BinaryOpNode(
                            TT_MUL, leaf.right, res, is_paren=True
                        )

                    res = leaf

                self._next()
            elif self.curr.is_type(TT_EQUAL):
                if assign_left is not None:
                    raise error.SyntaxError("Unexpected equal sign.")

                assign_left = res
                self._next(check_EOF=True)
                res = self._term()
            elif in_args[-1] and self.curr.is_type(TT_COMMA):
                if res is None:
                    raise error.SyntaxError("Unexpected comma.")

                args.append(res)
                self._next(check_EOF=True)
                res = self._term()
            else:
                raise error.SyntaxError(f"Unexpected {self.curr}.")

        if len(intermediate) > 0:
            raise error.SyntaxError("Unexpected end of expression.")

        return AssignNode(assign_left, res) if assign_left else res

    def _term(self) -> Token | BinaryOpNode:
        res = None
        negative = False

        while self.curr:
            if res is None:
                if self.curr.is_type(TT_MINUS):
                    negative = not negative
                    self._next(check_EOF=True)
                elif self.curr.is_type(TT_PLUS):
                    negative = False
                    self._next(check_EOF=True)

            if self.curr.is_types(NUMBERS):
                res = self.curr
            elif self.curr.is_type(TT_IDENTIFIER):
                if res:
                    res = BinaryOpNode(TT_MUL, res, self.curr, is_paren=True)
                else:
                    res = self.curr
            else:
                break

            self._next()

        if res is None and (self.curr is None or not self.curr.is_type(TT_LBRACKET)):
            if self.curr is None:
                raise error.SyntaxError("Unexpected end of expression.")
            else:
                raise error.SyntaxError(f"Unexpected {self.curr}.")

        return UnaryOpNode(TT_MINUS, res, True) if negative else res
