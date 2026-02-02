from .error import *
from .token import *
from .node import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = -1
        self.next()

    def next(self):
        self.i += 1
        self.curr = self.tokens[self.i] if len(self.tokens) > self.i else None
        return self.curr

    def peek_before(self):
        return self.tokens[self.i - 1] if self.i > 0 else None

    def parse(self):
        return self.parse_lowest()

    def parse_parentheses(self, parse_args=False):
        self.next()

        node = self.parse_add_minus()

        # parse as arguments of function
        if parse_args:
            node = [node]  # turn it into a list of args

            while self.curr and self.curr.token_type == TT_COMMA:
                self.next()
                node.append(self.parse_add_minus())

        if self.curr.token_type != TT_RPAREN:
            raise MethSyntaxError(f'Expected ")", found {self.curr}.')

        return node

    # parse highest priority, terms
    def parse_highest(self):
        node = None

        if self.curr.token_type in [TT_NUMBER, TT_IDENTIFIER, TT_LPAREN]:
            if self.curr.token_type == TT_NUMBER:
                node = NumberNode(self.curr.value)
            elif self.curr.token_type == TT_IDENTIFIER:
                node = IdentifierNode(self.curr.value)
            else:
                node = self.parse_parentheses()

            self.next()

            # also handle terms like: 3x, ax, 3(1 + 2), (1 + 2)(3 + 4)
            while self.curr and self.curr.token_type in [TT_IDENTIFIER, TT_LPAREN]:
                if self.curr.token_type == TT_IDENTIFIER:
                    right = IdentifierNode(self.curr.value)
                else:
                    # if previous token is an identifier and current is parentheses, make a function node
                    # TODO: update the code to be able to handle sin(x) with multiple identifiers
                    if self.peek_before().token_type == TT_IDENTIFIER:
                        right = self.parse_parentheses(parse_args=True)

                        if isinstance(node, IdentifierNode):
                            node = FunctionNode(node, right)
                        else:
                            if not isinstance(node.right, IdentifierNode):
                                raise MethNotImplError("node.right isn't an identifier")

                            node.right = FunctionNode(node.right, right)

                        self.next()
                        continue
                    else:
                        right = self.parse_parentheses()

                node = BinaryOpNode(node, TT_MUL, right)
                self.next()
        elif self.curr.token_type in [TT_ADD, TT_MINUS]:
            operator = self.curr.token_type
            self.next()
            node = UnaryOpNode(operator, self.parse_highest())
        else:
            raise MethSyntaxError(f"Unexpected token {self.curr}.")

        while self.curr and self.curr.token_type == TT_FACT:
            node = UnaryOpNode(TT_FACT, node)
            self.next()

        return node

    def parse_pow(self):
        node = self.parse_highest()

        while self.curr and self.curr.token_type == TT_POW:
            operator = self.curr.token_type
            self.next()
            node = BinaryOpNode(node, operator, self.parse_highest())

        return node

    def parse_mul_div_mod(self):
        node = self.parse_pow()

        while self.curr and self.curr.token_type in [TT_MUL, TT_DIV, TT_MOD]:
            operator = self.curr.token_type
            self.next()
            node = BinaryOpNode(node, operator, self.parse_pow())

        return node

    def parse_add_minus(self):
        node = self.parse_mul_div_mod()

        while self.curr and self.curr.token_type in [TT_ADD, TT_MINUS]:
            operator = self.curr.token_type
            self.next()
            node = BinaryOpNode(node, operator, self.parse_mul_div_mod())

        return node

    # for parsing assignments
    def parse_lowest(self):
        node = self.parse_add_minus()

        while self.curr and self.curr.token_type == TT_ASSIGN:
            self.next()
            node = AssignNode(node, self.parse_add_minus())

        return node
