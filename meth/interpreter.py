from .node import IdentifierNode
from .error import *
import math


class Interpreter:
    def __init__(self, ast, variables={}):
        self.ast = ast
        self.variables = variables

    def interpret(self):
        return self.visit(self.ast)

    def visit(self, node):
        # find visit function for that type of node using its type name
        visit_func = getattr(self, f"visit_{type(node).__name__}", None)
        if visit_func is None:
            raise MethNotImplError(f"Unknown node type {type(node).__name__}.")

        return visit_func(node)

    def visit_NumberNode(self, node):
        return node.value

    def visit_IdentifierNode(self, node):
        if node.value not in self.variables:
            raise MethVarNotDefinedError(f'Variable "{node.value}" is not defined.')

        return self.variables[node.value]

    def visit_BinaryOpNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        # cant use token type variables due to being recognized as a pattern
        match node.value:
            case "+":
                return left + right
            case "-":
                return left - right
            case "*":
                return left * right
            case "/":
                return left / right
            case "%":
                return left % right
            case "^":
                return left**right
            case _:
                raise MethNotImplError(f'Unknown operator "{node.value}".')

    def visit_UnaryOpNode(self, node):
        right = self.visit(node.right)

        match node.value:
            case "+":
                return +right
            case "-":
                return -right
            case "!":
                return math.factorial(right)
            case _:
                raise MethNotImplError(f'Unknown unary operator "{node.value}".')

    def visit_AssignNode(self, node):
        if not isinstance(node.left, IdentifierNode):
            raise MethSyntaxError(
                f"Expected assignment to identifier, found {node.left}."
            )

        right = self.visit(node.right)
        self.variables[node.left.value] = right
