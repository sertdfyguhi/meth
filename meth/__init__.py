from .interpreter import Interpreter
from .parser import Parser
from .lexer import Lexer

from .functions import *
from . import error, nodes, token


def tokenize(expr: str) -> list[token.Token]:
    """Tokenize an expression."""
    return Lexer().tokenize(expr)


def parse(expr: str | list[token.Token]) -> nodes.BaseNode | None:
    """Parse an expression."""
    return Parser().parse(Lexer().tokenize(expr) if type(expr) == str else expr)


def evaluate(ast: nodes.BaseNode | str) -> int | float | None:
    """Evaluate an expression."""
    if parsed := parse(ast) if type(ast) == str else ast:
        return Interpreter().interpret(parsed)


class Evaluator:
    def __init__(self) -> None:
        """Evaluate expressions with variables."""
        self.lexer = Lexer()
        self.parser = Parser()
        self.intepreter = Interpreter()

    def evaluate(self, expr: nodes.BaseNode | str) -> int | float | None:
        """Evaluate an expression."""
        if parsed := (
            self.parser.parse(self.lexer.tokenize(expr)) if type(expr) == str else expr
        ):
            return self.intepreter.interpret(parsed)

    def set_var(self, name: str, value: int | float) -> None:
        """Set the value of a variable."""
        if len(name) > 1:
            raise ValueError("Name can only be of length one.")

        if type(value) not in [int, float]:
            raise TypeError("Value can only be an int or float.")

        self.intepreter.vars[name] = value

    def get_var(self, name: str) -> int | float:
        """Get the value of a variable."""
        if name not in self.vars:
            raise error.VarNotDefinedError(f"{name} is not defined.")

        return self.vars[name]

    def delete_var(self, name: str) -> None:
        """Delete a variable."""
        del self.intepreter.vars[name]

    @property
    def vars(self) -> dict:
        """Variables as a dictionary."""
        return self.intepreter.vars
