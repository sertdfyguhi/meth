from .interpreter import Interpreter
from .parser import Parser
from .lexer import Lexer
from .node import Node


class Evaluator:
    def __init__(self, variables={}) -> None:
        """Initializes an evaluator with variables."""
        self.variables = variables

    def evaluate(self, expr: Node | str) -> int | float | None:
        """
        Evaluate an expression.

        Args:
            expr: Node | str
                Expression to evaluate / interpret.

        Returns: int | float | None
        """
        if type(expr) == str:
            tokens = Lexer(expr).tokenize()
            expr = Parser(tokens).parse()

        return Interpreter(expr, self.variables).interpret()

    def set_var(self, name: str, value: int | float) -> None:
        """
        Set the value of a variable.

        Args:
            name: str
                Name of the variable to set. Has to be a single character.
            value: int | float
                Value to set the variable with.

        Returns: None
        """
        if len(name) > 1:
            raise ValueError("Name can only be of length one.")
        if type(value) not in [int, float]:
            raise TypeError("Value can only be an int or float.")

        self.variables[name] = value

    def get_var(self, name: str) -> int | float:
        """
        Get the value of a variable.

        Args:
            name: str
                Name of the variable to get.

        Returns: int | float
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

        Returns: None
        """
        del self.variables[name]

    def clear_var(self) -> None:
        """Deletes all variables."""
        self.variables.clear()
