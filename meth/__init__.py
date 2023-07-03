from .interpreter import Interpreter
from .parser import Parser
from .lexer import Lexer

from .functions import *
from . import error, nodes, token, utils


def tokenize(expr: str) -> list[token.Token]:
    """
    Tokenize an expression.

    Args:
        expr: str
            The expression to tokenize.

    Returns: list[Token]
    """
    return Lexer().tokenize(expr)


def parse(expr: str | list[token.Token]) -> nodes.BaseNode | None:
    """
    Parses an expression.

    Args:
        expr: str | list[Token]
            The expression to parse.

    Returns: Node | None
    """
    return Parser().parse(tokenize(expr) if type(expr) == str else expr)


def evaluate(expr: nodes.BaseNode | str) -> int | float | None:
    """
    Evaluate an expression.

    Args:
        expr: Node | str
            The expression to evaluate / interpret.

    Returns: int | float | None
    """
    if parsed := parse(expr) if type(expr) == str else expr:
        return Interpreter().interpret(parsed)


class Evaluator:
    def __init__(self) -> None:
        """Initializes an evaluator with variables."""
        self.lexer = Lexer()
        self.parser = Parser()
        self.intepreter = Interpreter()

    def evaluate(self, expr: nodes.BaseNode | str) -> int | float | None:
        """
        Evaluate an expression.

        Args:
            expr: Node | str
                Expression to evaluate / interpret.

        Returns: int | float | None
        """
        if parsed := (
            self.parser.parse(self.lexer.tokenize(expr)) if type(expr) == str else expr
        ):
            return self.intepreter.interpret(parsed)

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

        self.intepreter.vars[name] = value

    def get_var(self, name: str) -> int | float:
        """
        Get the value of a variable.

        Args:
            name: str
                Name of the variable to get.

        Returns: int | float
        """
        if name not in self.vars:
            raise error.VarNotDefinedError(f"{name} is not defined.")

        return self.vars[name]

    def delete_var(self, name: str) -> None:
        """
        Delete a variable.

        Args:
            name: str
                Name of the variable to delete.

        Returns: None
        """
        del self.intepreter.vars[name]

    def clear_var(self) -> None:
        """Deletes all variables."""
        self.intepreter.vars = {}

    @property
    def vars(self) -> dict[str, int | float]:
        """
        Variables as a dictionary.

        Returns: dict[str, int | float]
        """
        return self.intepreter.vars
