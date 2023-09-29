from . import error, nodes, token, utils
from .interpreter import Interpreter
from .evaluator import Evaluator
from .parser import Parser
from .lexer import Lexer
from .functions import *


__version__ = "1.2.1"


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
