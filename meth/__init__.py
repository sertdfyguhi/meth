from .interpreter import Interpreter
from .parser import Parser
from .lexer import Lexer
from .token import *
from .nodes import *

from .functions import *


def parse(expr: str):
    """Parse an expression."""
    return Parser(Lexer(expr).tokenize()).parse()


def evaluate(ast: BaseNode | str):
    """Evaluate an expression."""
    if type(ast) == str:
        ast = parse(ast)

    return Interpreter().interpret(ast)


class Evaluator:
    def __init__(self) -> None:
        """Evaluate expressions with variables."""
        self.intepreter = Interpreter()

    def evaluate(self, expr: BaseNode | str):
        """Evaluate an expression."""
        return self.intepreter.interpret(expr if type(expr) != str else parse(expr))

    @property
    def vars(self) -> dict:
        """Variables as a dictionary."""
        return self.intepreter.vars
