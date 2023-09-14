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
            raise error.SyntaxError("Unexpected end of expastsion.")

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

        ast = self._term()
        intermediate = []
        assign_left = None
        arg_nests = 0
        args = []

        while self.curr:
            if self.curr.is_types(OPERATORS):
                op = self.curr

                self._next(check_EOF=True)

                right = self._term()

                if op.is_types([TT_PLUS, TT_MINUS]):
                    ast = BinaryOpNode(op, ast, right)
                    continue
                elif op.is_types([TT_MUL, TT_DIV]):
                    leaf = utils.get_leaf_node_right(ast, True, [TT_POW, TT_MOD])
                else:
                    leaf = utils.get_leaf_node_right(ast, True)

                if type(leaf) == Token or leaf.is_paren:
                    ast = BinaryOpNode(op, leaf, right)
                else:
                    leaf.right = BinaryOpNode(op, leaf.right, right)
            elif self.curr.is_type(TT_LBRACKET):
                try:
                    if self.tokens[self.i - 1].is_type(TT_IDENTIFIER):
                        arg_nests += 1
                except IndexError:
                    # ignore when previous token does not exist
                    pass

                intermediate.append(ast)
                self._next()
                ast = self._term()
            elif self.curr.is_type(TT_RBRACKET):
                if ast is None:
                    raise error.SyntaxError("Unexpected end of parentheses.")
                elif len(intermediate) == 0:
                    raise error.SyntaxError("Unexpected right bracket.")

                last_intermediate = intermediate.pop()
                ast.is_paren = True

                if last_intermediate:
                    leaf = utils.get_leaf_node_right(last_intermediate)

                    if arg_nests > 0:
                        if ast:
                            args.append(ast)

                        if type(leaf) == Token:
                            last_intermediate = FunctionNode(leaf, args)
                        else:
                            leaf.right = FunctionNode(leaf.right, args)

                        arg_nests -= 1
                        args = []
                    elif type(leaf) == Token or leaf.is_paren:
                        last_intermediate = BinaryOpNode(
                            TT_MUL, leaf, ast, is_paren=True
                        )
                    elif leaf.right is None:
                        leaf.right = ast
                    elif type(leaf.right) == UnaryOpNode:
                        leaf.right.left = ast
                    else:
                        leaf.right = BinaryOpNode(
                            TT_MUL, leaf.right, ast, is_paren=True
                        )

                    ast = last_intermediate

                self._next()
            elif self.curr.is_type(TT_EQUAL):
                if assign_left is not None:
                    raise error.SyntaxError("Unexpected equal sign.")

                assign_left = ast
                self._next(check_EOF=True)
                ast = self._term()
            elif arg_nests > 0 and self.curr.is_type(TT_COMMA):
                if ast is None:
                    raise error.SyntaxError("Unexpected comma.")

                args.append(ast)
                self._next(check_EOF=True)
                ast = self._term()
            else:
                raise error.SyntaxError(f"Unexpected {self.curr}.")

            # print(ast)

        if len(intermediate) > 0:
            raise error.SyntaxError("Unexpected end of expastsion.")

        return AssignNode(assign_left, ast) if assign_left else ast

    def _term(self) -> Token | BinaryOpNode:
        ast = None
        negative = False

        while self.curr:
            # unary checks
            if ast is None:
                if self.curr.is_type(TT_MINUS):
                    negative = not negative
                    self._next(check_EOF=True)
                elif self.curr.is_type(TT_PLUS):
                    negative = False
                    self._next(check_EOF=True)

            if self.curr.is_types(NUMBERS):
                ast = self.curr
            elif self.curr.is_type(TT_IDENTIFIER):
                if ast:
                    ast = BinaryOpNode(TT_MUL, ast, self.curr, is_paren=True)
                else:
                    ast = self.curr
            else:
                break

            self._next()

        if ast is None and (self.curr is None or not self.curr.is_type(TT_LBRACKET)):
            if self.curr is None:
                raise error.SyntaxError("Unexpected end of expastsion.")
            else:
                raise error.SyntaxError(f"Unexpected {self.curr}.")

        return UnaryOpNode(TT_MINUS, ast, True) if negative else ast
