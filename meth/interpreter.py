from .token import TokenType
from .builtin import *
from .error import *
from .node import *


from numbers import Number
import operator
import math


OPERATORS = {
    TokenType.ADD: operator.add,
    TokenType.MINUS: operator.sub,
    TokenType.MUL: operator.mul,
    TokenType.DIV: operator.truediv,
    TokenType.MOD: operator.mod,
    TokenType.POW: operator.pow,
}


class MethFunction:
    """A math function."""

    def __init__(self, name: str, args: list[IdentifierNode], ast: Node) -> None:
        """Initializes a meth function."""
        self.name = name
        self.args = args
        self.ast = ast

    def __call__(
        self, variables: dict[str, Number | Callable], args: list[Number]
    ) -> Number | Callable | None:
        """Calls the meth function."""
        if len(args) != len(self.args):
            raise MethArgumentError(
                f"{self.name}() takes in {len(self.args)} arguments but {len(args)} were given."
            )

        variables = variables.copy()

        for i, arg in enumerate(self.args):
            variables[arg.value] = args[i]

        return Interpreter(self.ast, variables).interpret()


class Interpreter:
    """An interpreter that interprets an AST."""

    def __init__(
        self, ast: Node, variables: dict[str, Number | Callable] | None = None
    ) -> None:
        """
        Initializes the interpreter.

        Args:
            ast: Node
                Abstract syntax tree to interpret.
            variables: dict[str, Number | Callable] | None = None
                Dictionary of variables.
        """
        self.ast = ast
        self.variables = {} if variables is None else variables

    def interpret(self) -> Number | Callable | None:
        """
        Interprets the AST.

        Returns: int | float | Callable | None
        """
        return self._visit(self.ast)

    def _get_variable_or_constant(self, name: str) -> Number | Callable:
        """Get name from variables or constants."""
        if name in self.variables:
            return self.variables[name]
        elif name in CONSTANTS:
            return CONSTANTS[name]
        else:
            raise MethVarNotDefinedError(f'Variable "{name}" is not defined.')

    def _find_product_of_identifier(self, identifier) -> Number:
        """Gets the product of all variables in an identifier."""
        product = 1

        for char in identifier:
            value = self._get_variable_or_constant(char)

            if not isinstance(value, (int, float)):
                raise MethValueError(
                    f'Expected variable "{char}" to be number, found {type(value)}.'
                )

            product *= value

        return product

    def _visit(self, node: Node) -> Number | Callable | None:
        """Visits a node."""
        match node:
            case NumberNode():
                return node.value

            case IdentifierNode():
                return self._visit_IdentifierNode(node)

            case BinaryOpNode():
                return self._visit_BinaryOpNode(node)

            case UnaryOpNode():
                return self._visit_UnaryOpNode(node)

            case AssignNode():
                return self._visit_AssignNode(node)

            case FunctionNode():
                return self._visit_FunctionNode(node)

            case _:
                raise MethNotImplError(f"Unknown node type {type(node).__name__}.")

    def _visit_IdentifierNode(self, node: IdentifierNode) -> Number | Callable:
        """Visits a IdentifierNode."""
        identifier = node.value

        if len(identifier) > 1:
            if is_builtin(identifier):
                return get_builtin(identifier)

            for name in BUILTINS:
                if identifier.endswith(name):
                    builtin = get_builtin(name)
                    product = self._find_product_of_identifier(identifier[: -len(name)])

                    if callable(builtin):
                        return lambda *args: product * builtin(*args)
                    else:
                        # if builtin is a number, multiply it with the other variables
                        return product * builtin

            return self._find_product_of_identifier(identifier)
        else:
            return self._get_variable_or_constant(identifier)

    def _visit_BinaryOpNode(self, node: BinaryOpNode) -> Number:
        """Visits a BinaryOpNode."""
        left = self._visit(node.left)
        right = self._visit(node.right)

        if node.value == TokenType.DIV and right == 0:
            raise MethZeroDivError("Cannot divide by zero.")

        if node.value not in OPERATORS:
            raise MethNotImplError(f'Unknown operator "{node.value}".')

        return OPERATORS[node.value](left, right)

    def _visit_UnaryOpNode(self, node: UnaryOpNode) -> Number:
        """Visits a UnaryOpNode."""
        right = self._visit(node.right)

        match node.value:
            case TokenType.ADD:
                return +right
            case TokenType.MINUS:
                return -right
            case TokenType.FACT:
                return math.factorial(right)
            case _:
                raise MethNotImplError(f'Unknown unary operator "{node.value}".')

    def _visit_AssignNode(self, node: AssignNode) -> None:
        """Visits a AssignNode."""
        if not isinstance(node.left, (IdentifierNode, FunctionNode)):
            raise MethSyntaxError(
                f"Expected assignment to identifier or function, found {node.left}."
            )

        if isinstance(node.left, FunctionNode):
            func_name = node.left.value.value
            if len(func_name) > 1:
                raise MethSyntaxError(
                    f"Function assignment name cannot be more than one character."
                )

            # check if all arguments in function is an identifier, eg: f(x, y) and not f(x+2, y)
            # ? maybe allow for binary operations in arguments
            args = node.left.right
            if any(not isinstance(arg, IdentifierNode) for arg in args):
                raise MethValueError(
                    "Expected all arguments in function assignment to be identifiers."
                )

            func = MethFunction(func_name, args, node.right)
            self.variables[func_name] = func
        else:
            right = self._visit(node.right)
            self.variables[node.left.value] = right

    def _visit_FunctionNode(self, node: FunctionNode) -> Number:
        """Visits a FunctionNode."""
        func = self._visit(node.value)

        if callable(func):
            # visit all arguments and pass it to function
            args = [self._visit(arg) for arg in node.right]

            if isinstance(func, MethFunction):
                return func(self.variables, args)
            else:
                return func(*args)
        else:
            if len(node.right) > 1:
                raise MethSyntaxError("Unexpected argument in implied multiplication.")

            return func * self._visit(node.right[0])
