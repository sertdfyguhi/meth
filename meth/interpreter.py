from .nodes import *
from .token import *


class Function:
    def __init__(self, func_node: FunctionNode, func: BaseNode) -> None:
        self.name = func_node.value.value
        self.args = func_node.left
        self.func = func

    def __call__(self, *args) -> None:
        if len(args) != len(self.args):
            raise TypeError(
                f"{self.name}() takes in {len(self.args)} arguments but {len(args)} were given."
            )

        return Interpreter(
            {self.args[i].value: args[i] for i in range(len(self.args))}
        ).interpret(self.func)


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
            raise SyntaxError("how would this even happen")

    def visit_UnaryOpNode(self, node: BaseNode):
        if node.value == TT_MINUS:
            return -self.visit(node.left)

        return self.visit(node.left)

    def visit_AssignNode(self, node: BaseNode) -> None:
        if node.left == TT_IDENTIFIER:
            self.vars[node.left.value] = self.visit(node.right)
        elif type(node.left) == FunctionNode:
            self.vars[node.left.value.value] = Function(node.left, node.right)
        else:
            return self.visit(node.left)

    def visit_FunctionNode(self, node: BaseNode) -> None:
        if type(value := self.visit(node.value)) == Function:
            return value(*[self.visit(arg) for arg in node.left])
        else:
            if len(node.left) > 1:
                raise SyntaxError("Unexpected argument.")
            return value * self.visit(node.left[0])
