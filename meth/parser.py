from .error import *
from .token import *
from .node import *


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        """
        Initializes the parser.

        Args:
            tokens: list[Token]
                The tokens to create the AST from.
        """
        self.tokens = tokens
        self.i = -1
        self._next()

    def _next(self):
        self.i += 1
        self.curr = self.tokens[self.i] if len(self.tokens) > self.i else None
        return self.curr

    def parse(self) -> Node | None:
        """
        Parses the tokens into an AST.

        Returns: Node | None
        """
        return self._parse_lowest()

    def _parse_parentheses(self, parse_args=False):
        self._next()

        node = self._parse_add_minus()

        # parse as arguments of function
        if parse_args:
            node = [node]  # turn it into a list of args

            while self.curr and self.curr.token_type == TT_COMMA:
                self._next()
                node.append(self._parse_add_minus())

        if self.curr.token_type != TT_RPAREN:
            raise MethSyntaxError(f'Expected ")", found {self.curr}.')

        return node

    # parse highest priority, terms
    def _parse_highest(self):
        node = None

        if self.curr.token_type in [TT_NUMBER, TT_IDENTIFIER, TT_LPAREN]:
            if self.curr.token_type == TT_NUMBER:
                node = NumberNode(self.curr.value)
            elif self.curr.token_type == TT_IDENTIFIER:
                node = IdentifierNode(self.curr.value)
            else:
                node = self._parse_parentheses()

            self._next()

            # also handle terms like: 3x, ax, 3(1 + 2), (1 + 2)(3 + 4)
            while self.curr and self.curr.token_type in [
                TT_NUMBER,
                TT_IDENTIFIER,
                TT_LPAREN,
            ]:
                if self.curr.token_type == TT_NUMBER:
                    if isinstance(node, NumberNode):
                        raise MethSyntaxError(
                            "Expected identifier or parentheses, found number."
                        )

                    node = BinaryOpNode(node, TT_MUL, NumberNode(self.curr.value))
                elif self.curr.token_type == TT_IDENTIFIER:
                    node = BinaryOpNode(node, TT_MUL, IdentifierNode(self.curr.value))
                else:
                    if isinstance(node, IdentifierNode) or isinstance(
                        node.right, IdentifierNode
                    ):
                        # if previous token is an identifier and current is parentheses, make a function node
                        right = self._parse_parentheses(parse_args=True)

                        if isinstance(node, IdentifierNode):
                            node = FunctionNode(node, right)
                        else:
                            if not isinstance(node.right, IdentifierNode):
                                raise MethNotImplError("node.right isn't an identifier")

                            node.right = FunctionNode(node.right, right)
                    else:
                        node = BinaryOpNode(node, TT_MUL, self._parse_parentheses())

                self._next()
        elif self.curr.token_type in [TT_ADD, TT_MINUS]:
            operator = self.curr.token_type
            self._next()
            node = UnaryOpNode(operator, self._parse_highest())
        else:
            raise MethSyntaxError(f"Unexpected token {self.curr}.")

        while self.curr and self.curr.token_type == TT_FACT:
            node = UnaryOpNode(TT_FACT, node)
            self._next()

        return node

    def _parse_pow(self):
        node = self._parse_highest()

        while self.curr and self.curr.token_type == TT_POW:
            operator = self.curr.token_type
            self._next()
            node = BinaryOpNode(node, operator, self._parse_highest())

        return node

    def _parse_mul_div_mod(self):
        node = self._parse_pow()

        while self.curr and self.curr.token_type in [TT_MUL, TT_DIV, TT_MOD]:
            operator = self.curr.token_type
            self._next()
            node = BinaryOpNode(node, operator, self._parse_pow())

        return node

    def _parse_add_minus(self):
        node = self._parse_mul_div_mod()

        while self.curr and self.curr.token_type in [TT_ADD, TT_MINUS]:
            operator = self.curr.token_type
            self._next()
            node = BinaryOpNode(node, operator, self._parse_mul_div_mod())

        return node

    # for parsing assignments
    def _parse_lowest(self):
        node = self._parse_add_minus()

        while self.curr and self.curr.token_type == TT_ASSIGN:
            self._next()
            node = AssignNode(node, self._parse_add_minus())

        return node
