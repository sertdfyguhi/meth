from inspect import signature

from .builtins import *
from .nodes import *
from .token import *
from . import error


class Function:
    def __init__(self, func_node: FunctionNode, func: BaseNode) -> None:
        """Initializes a meth function."""
        self.name = func_node.value.value
        self.args = func_node.left
        self.func = func

    def __call__(self, *args) -> None:
        if len(args) != len(self.args):
            raise error.ArgumentError(
                f"{self.name}() takes in {len(self.args)} arguments but {len(args)} were given."
            )

        return Interpreter(
            {self.args[i].value: args[i] for i in range(len(self.args))}
        ).interpret(self.func)


class Interpreter:
    def __init__(self, vars: dict[str, int | float] = {}) -> None:
        """
        Initializes the interpreter.

        Args:
            vars: dict[str, int | float] = {}
                Dictionary of variables.
        """
        self.vars = vars

    def interpret(self, ast: BaseNode) -> int | float | None:
        """
        Interpret an AST.

        Args:
            ast: Node
                Tree to interpret.

        Returns: int | float | None
        """
        return self._visit(ast)

    def _visit(self, node: BaseNode):
        return getattr(self, "_visit_" + type(node).__name__)(node)

    def _visit_Token(self, token: Token):
        if token.type == TT_IDENTIFIER:
            is_var = token.value in self.vars
            if not is_var and (builtin := get_builtin(token.value)) is None:
                raise error.VarNotDefinedError(f"{token.value} is not defined.")

            return self.vars[token.value] if is_var else builtin

        return token.value

    def _visit_BinaryOpNode(self, node: BaseNode):
        if node.value == TT_PLUS:
            return self._visit(node.left) + self._visit(node.right)
        elif node.value == TT_MINUS:
            return self._visit(node.left) - self._visit(node.right)
        elif node.value == TT_MUL:
            return self._visit(node.left) * self._visit(node.right)
        elif node.value == TT_DIV:
            return self._visit(node.left) / self._visit(node.right)
        elif node.value == TT_MOD:
            return self._visit(node.left) % self._visit(node.right)
        elif node.value == TT_POW:
            return self._visit(node.left) ** self._visit(node.right)
        else:
            raise error.NotImplError(f"{node.value} is unimplemented.")

    def _visit_UnaryOpNode(self, node: BaseNode):
        value = self._visit(node.left)
        return value if node.value == TT_PLUS else -value

    def _visit_AssignNode(self, node: BaseNode):
        if node.left == TT_IDENTIFIER:
            self.vars[node.left.value] = self._visit(node.right)
        elif type(node.left) == FunctionNode:
            self.vars[node.left.value.value] = Function(node.left, node.right)
        else:
            return self._visit(node.left)

    def _visit_FunctionNode(self, node: BaseNode):
        if type(value := self._visit(node.value)) == Function:
            return value(*[self._visit(arg) for arg in node.left])
        elif callable(value):
            if (plen := len(signature(value).parameters)) != len(node.left):
                raise error.SyntaxError(
                    f"{value}() takes in {plen} arguments but {len(node.left)} were given."
                )

            return value(*[self._visit(arg) for arg in node.left])
        else:
            if len(node.left) > 1:
                raise error.SyntaxError("Unexpected argument.")

            return value * self._visit(node.left[0])
