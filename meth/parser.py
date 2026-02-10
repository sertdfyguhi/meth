from .token import Token, TokenType
from .error import *
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
        """Advances to the next token."""
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
        """Parses the inside of parentheses."""
        self._next()

        node = self._parse_add_minus()

        # parse as arguments of function
        if parse_args:
            node = [node]  # turn it into a list of args

            while self.curr and self.curr.token_type == TokenType.COMMA:
                self._next()
                node.append(self._parse_add_minus())

        if self.curr.token_type != TokenType.RPAREN:
            raise MethSyntaxError(f'Expected ")", found {self.curr}.')

        return node

    def _parse_highest(self):
        """Parses highest precedence operators (numbers, identifiers, parentheses, unary)."""
        node = None

        if self.curr.token_type in [
            TokenType.NUMBER,
            TokenType.IDENTIFIER,
            TokenType.LPAREN,
        ]:
            if self.curr.token_type == TokenType.NUMBER:
                node = NumberNode(self.curr.value)
            elif self.curr.token_type == TokenType.IDENTIFIER:
                node = IdentifierNode(self.curr.value)
            else:
                node = self._parse_parentheses()

            self._next()

            # also handle terms like: 3x, ax, 3(1 + 2), (1 + 2)(3 + 4)
            while self.curr and self.curr.token_type in [
                TokenType.NUMBER,
                TokenType.IDENTIFIER,
                TokenType.LPAREN,
            ]:
                if self.curr.token_type == TokenType.NUMBER:
                    if isinstance(node, NumberNode):
                        raise MethSyntaxError(
                            "Expected identifier or parentheses, found number."
                        )

                    node = BinaryOpNode(
                        node, TokenType.MUL, NumberNode(self.curr.value)
                    )
                elif self.curr.token_type == TokenType.IDENTIFIER:
                    node = BinaryOpNode(
                        node, TokenType.MUL, IdentifierNode(self.curr.value)
                    )
                else:
                    # if previous token is an identifier and current is parentheses
                    # make a function node instead of binary op
                    if isinstance(node, IdentifierNode):
                        right = self._parse_parentheses(parse_args=True)
                        node = FunctionNode(node, right)
                    elif isinstance(node.right, IdentifierNode):
                        right = self._parse_parentheses(parse_args=True)
                        node.right = FunctionNode(node.right, right)
                    else:
                        node = BinaryOpNode(
                            node, TokenType.MUL, self._parse_parentheses()
                        )

                self._next()
        elif self.curr.token_type in [TokenType.ADD, TokenType.MINUS]:
            operator = self.curr.token_type
            self._next()
            node = UnaryOpNode(operator, self._parse_highest())
        else:
            raise MethSyntaxError(f"Unexpected token {self.curr}.")

        while self.curr and self.curr.token_type == TokenType.FACT:
            node = UnaryOpNode(TokenType.FACT, node)
            self._next()

        return node

    def _parse_pow(self):
        """Parses fourth precedence operators (power)."""
        node = self._parse_highest()

        while self.curr and self.curr.token_type == TokenType.POW:
            operator = self.curr.token_type
            self._next()
            node = BinaryOpNode(node, operator, self._parse_highest())

        return node

    def _parse_mul_div_mod(self):
        """Parses third precedence operators (multiply, divide, modulo)."""
        node = self._parse_pow()

        while self.curr and self.curr.token_type in [
            TokenType.MUL,
            TokenType.DIV,
            TokenType.MOD,
        ]:
            operator = self.curr.token_type
            self._next()
            node = BinaryOpNode(node, operator, self._parse_pow())

        return node

    def _parse_add_minus(self):
        """Parses second precedence operators (add, minus)."""
        node = self._parse_mul_div_mod()

        while self.curr and self.curr.token_type in [TokenType.ADD, TokenType.MINUS]:
            operator = self.curr.token_type
            self._next()
            node = BinaryOpNode(node, operator, self._parse_mul_div_mod())

        return node

    def _parse_lowest(self):
        """Parses lowest precedence operators (assign)."""
        node = self._parse_add_minus()

        while self.curr and self.curr.token_type == TokenType.ASSIGN:
            self._next()
            node = AssignNode(node, self._parse_add_minus())

        return node
