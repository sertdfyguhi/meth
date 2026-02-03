from .builtin import *
from .error import *
from .node import *
import math


class MethFunction:
    def __init__(self, name, args, ast) -> None:
        """Initializes a meth function."""
        self.name = name
        self.args = args
        self.ast = ast

    def __call__(self, *args) -> None:
        if len(args) != len(self.args):
            raise MethArgumentError(
                f"{self.name}() takes in {len(self.args)} arguments but {len(args)} were given."
            )

        return Interpreter(
            self.ast, {self.args[i].value: args[i] for i in range(len(self.args))}
        ).interpret()


def _get_variable_or_constant(name, variables):
    if name in variables:
        return variables[name]
    elif name in CONSTANTS:
        return CONSTANTS[name]
    else:
        raise MethVarNotDefinedError(f'Variable "{name}" is not defined.')


def _find_product_of_identifier(identifier, variables):
    product = 1

    for char in identifier:
        value = _get_variable_or_constant(char, variables)

        if type(value) not in [int, float]:
            raise MethValueError(
                f'Expected variable "{char}" to be number, found {type(value)}.'
            )

        product *= value

    return product


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
        identifier = node.value

        if len(identifier) > 1:
            if is_builtin(identifier):
                return get_builtin(identifier)

            for name in BUILTINS:
                if identifier.endswith(name):
                    builtin = get_builtin(name)
                    product = _find_product_of_identifier(
                        identifier[: -len(name)], self.variables
                    )

                    if callable(builtin):
                        return lambda *args: product * builtin(*args)
                    else:
                        # if builtin is a number, multiply it with the other variables
                        return product * builtin

            return _find_product_of_identifier(identifier, self.variables)
        else:
            return _get_variable_or_constant(identifier, self.variables)

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
        if not isinstance(node.left, (IdentifierNode, FunctionNode)):
            raise MethSyntaxError(
                f"Expected assignment to identifier or function, found {node.left}."
            )

        if isinstance(node.left, FunctionNode):
            if len(node.left.value.value) > 1:
                raise MethSyntaxError(
                    f"Function assignment name cannot be more than one character."
                )

            # check if all arguments in function is an identifier, eg: f(x, y) and not f(x+2, y)
            # ? maybe allow for binary operations in arguments
            if any(not isinstance(arg, IdentifierNode) for arg in node.left.right):
                raise MethArgumentError(
                    "Expected all arguments in function assignment to be identifiers."
                )

            func = MethFunction(node.left.value.value, node.left.right, node.right)
            self.variables[node.left.value.value] = func
        else:
            right = self.visit(node.right)
            self.variables[node.left.value] = right

    def visit_FunctionNode(self, node):
        func = self.visit(node.value)

        if callable(func):
            # visit all arguments and pass it to function
            return func(*[self.visit(arg) for arg in node.right])
        else:
            if len(node.right) > 1:
                raise MethSyntaxError("Unexpected argument in implied multiplication.")

            return func * self.visit(node.right[0])
