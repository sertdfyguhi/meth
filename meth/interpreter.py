from .token import *


class Interpreter:
    def __init__(self, ast):
        self.ast = ast

    def interpret(self):
        return self.visit(self.ast)

    def visit(self, node):
        # find visit function for that type of node using its type name
        visit_func = getattr(self, f"visit_{type(node).__name__}", None)
        if visit_func is None:
            raise ValueError(f"unknown node type {type(node).__name__}")

        return visit_func(node)

    def visit_NumberNode(self, node):
        return node.value

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
            case _:
                raise ValueError(f'unrecognized operator "{node.value}"')
