from .interpreter import Interpreter, MethFunction
from .parser import Parser
from .lexer import Lexer
from .node import Node

from typing import Callable
from numbers import Number


class Evaluator:
    def __init__(self, variables: dict[str, Number | Callable] = {}) -> None:
        """
        Initializes an evaluator with variables.

        Args:
            variables: dict[str, Number | Callable]
                Dictionary of variables.
        """
        self.variables = variables

    def evaluate(self, expr: Node | str) -> Number | None:
        """
        Evaluate an expression.

        Args:
            expr: Node | str
                Expression to evaluate / interpret.

        Returns: int | float | None
        """
        if type(expr) == str:
            expr = Lexer(expr).tokenize()

        if type(expr) == list:
            expr = Parser(expr).parse()

        return Interpreter(expr, self.variables).interpret()

    def set_var(self, name: str, value: Number | MethFunction) -> None:
        """
        Set the value of a variable.

        Args:
            name: str
                Name of the variable to set. Has to be a single character.
            value: Number | MethFunction
                Value to set the variable with.
        """
        if len(name) > 1:
            raise ValueError("Name can only be of length one.")
        if not isinstance(value, (Number, MethFunction)):
            raise TypeError("Value can only be a number or MethFunction.")

        self.variables[name] = value

    def get_var(self, name: str) -> Number | MethFunction:
        """
        Get the value of a variable.

        Args:
            name: str
                Name of the variable to get.

        Returns: Number | MethFunction
        """
        if name not in self.vars:
            raise ValueError(f'"{name}" is not defined.')

        return self.variables[name]

    def delete_var(self, name: str) -> None:
        """
        Delete a variable.

        Args:
            name: str
                Name of the variable to delete.
        """
        del self.variables[name]

    def clear_var(self) -> None:
        """Deletes all variables."""
        self.variables.clear()
