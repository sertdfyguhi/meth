from .interpreter import Interpreter
from .parser import Parser
from .lexer import Lexer

from .functions import *
from .nodes import *
from . import error


def parse(expr: str) -> BaseNode | None:
    """Parse an expression."""
    return Parser(Lexer(expr).tokenize()).parse()


def evaluate(ast: BaseNode | str) -> int | float:
    """Evaluate an expression."""
    if parsed := parse(ast) if type(ast) == str else ast:
        return Interpreter().interpret(parsed)


class Evaluator:
    def __init__(self) -> None:
        """Evaluate expressions with variables."""
        self.intepreter = Interpreter()

    def evaluate(self, expr: BaseNode | str) -> int | float:
        """Evaluate an expression."""
        if parsed := parse(expr) if type(expr) == str else expr:
            return self.intepreter.interpret(parsed)

    @property
    def vars(self) -> dict:
        """Variables as a dictionary."""
        return self.intepreter.vars
