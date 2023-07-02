from . import utils, error
from .token import *
from .nodes import *


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
        disallow_assign: bool = False,
        in_args: bool = False,
        is_paren: bool = False,
    ) -> BaseNode:
        """
        Parse the inputted tokens.

        Args:
            tokens: list[Token]
                List of tokens to parse.

        Internal Args:
            disallow_assign: bool = False
                Raises an error if an assignment is found.
            in_args: bool = False
                Parses tokens as arguments.
            is_paren: bool = False
                Sets the is_paren value of the node.

        Returns: Node
        """
        self.tokens = tokens
        self.i = -1
        self._next()

        if self.curr is None:
            return None

        self.node = self.curr
        if in_args:
            args = []

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
                right = self._factor()

                self.node = (
                    UnaryOpNode(op_type, right)
                    if self.node in [TT_PLUS, TT_MINUS]
                    else BinaryOpNode(op_type, self.node, right)
                )
            elif self.curr in [TT_MUL, TT_DIV, TT_MOD]:
                self._binary_op(self.curr.type, stop_at=[TT_POW])
            elif self.curr == TT_POW:
                self._binary_op(TT_POW)
            elif self.curr == TT_LBRACKET:
                node = utils.get_leaf_node_right(self.node, True)

                # check for 2(x + 1) or (1 + 2)(2 * 2)
                is_mul = last_tok in [TT_INT, TT_FLOAT] or getattr(
                    node, "is_paren", False
                )
                is_func = last_tok == TT_IDENTIFIER

                right = self._factor(is_func)
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
                    self._binary_op(TT_MUL, self.curr, is_paren=True)
            elif not disallow_assign and self.curr == TT_EQUAL:
                self.node = AssignNode(
                    self.node, Parser().parse(self.tokens[self.i + 1 :], True)
                )
                self.i = len(self.tokens)
            elif in_args and self.curr == TT_COMMA:
                self.node.is_paren = is_paren
                args.append(self.node)
                self.node = self._next(check_EOF=True, change_curr=False)
            else:
                if (last_tok in [TT_INT, TT_FLOAT, TT_IDENTIFIER, TT_RBRACKET]) or (
                    self._next(change_curr=False)
                    in [
                        TT_INT,
                        TT_FLOAT,
                        TT_RBRACKET,
                    ]
                ):
                    raise error.SyntaxError(f"Unexpected character {self.curr}")

            self._next()

        if in_args:
            args.append(self.node)
        else:
            self.node.is_paren = is_paren

        return args if in_args else self.node

    def _factor(self, in_args: bool = False):
        """Parse a factor."""
        self._next(True)

        if TT_LBRACKET in [self.curr, self.tokens[self.i - 1]]:
            if self.curr == TT_LBRACKET:
                self._next(True)

            tokens = []
            opened = 1

            # get all tokens in bracket
            while opened:
                tokens.append(self.curr)
                self._next(True)

                if self.curr == TT_RBRACKET:
                    opened -= 1
                elif self.curr == TT_LBRACKET:
                    opened += 1

            return Parser().parse(tokens, True, in_args, True)
        elif self.curr in [TT_INT, TT_FLOAT, TT_IDENTIFIER]:
            return self.curr
        elif self.curr in [TT_PLUS, TT_MINUS]:
            # cases like -1, +1
            return UnaryOpNode(self.curr.type, self._factor())
        else:
            raise error.SyntaxError(f"Invalid character {self.curr.type}")

    def _binary_op(
        self, op_type, right=None, stop_at: list = [], is_paren: bool = False
    ):
        """Parse a binary operation."""
        node = utils.get_leaf_node_right(self.node, True, stop_at=stop_at)
        if right is None:
            right = self._factor()

        # if is_paren is True then i shouldn't change it
        if type(node) not in [Token, UnaryOpNode] and not getattr(
            node.right, "is_paren", False
        ):
            node.right = BinaryOpNode(op_type, node.right, right, is_paren)
        else:
            self.node = BinaryOpNode(op_type, node, right, is_paren)
