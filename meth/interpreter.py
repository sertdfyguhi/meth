from .nodes import *
from .token import *


class Interpreter:
    def __init__(self, vars: dict = {}) -> None:
        self.vars = vars

    def interpret(self, ast: BaseNode) -> int | float:
        return self.visit(ast)

    def visit(self, node: BaseNode) -> int | float:
        return getattr(self, "visit_" + type(node).__name__)(node)

    def visit_Token(self, token: Token):
        if token.type == TT_IDENTIFIER:
            if token.value not in self.vars:
                raise NameError(f"{token.value} is not defined.")
            return self.vars[token.value]

        return token.value

    def visit_BinaryOpNode(self, node: BaseNode):
        if node.value == TT_PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.value == TT_MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.value == TT_MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.value == TT_DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif node.value == TT_MOD:
            return self.visit(node.left) % self.visit(node.right)
        elif node.value == TT_POW:
            return self.visit(node.left) ** self.visit(node.right)
        else:
            raise SyntaxError("how the fuck would this even happen")

    def visit_UnaryOpNode(self, node: BaseNode):
        pass

    def visit_AssignNode(self, node: BaseNode) -> None:
        if node.left != TT_IDENTIFIER:
            return self.visit(node.left)

        self.vars[node.left.value] = self.visit(node.right)

    def visit_FunctionNode(self, node: BaseNode) -> None:
        if callable(value := self.visit(node.value)):
            pass
        else:
            if len(node.left) > 1:
                raise SyntaxError("Unexpected argument.")
            return value * self.visit(node.left[0])
