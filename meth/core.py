from .interpreter import Interpreter
from .parser import Parser
from .lexer import Lexer
from .token import Token
from .node import Node

from typing import Callable
from numbers import Number


def tokenize(expr: str) -> list[Token]:
    """
    Tokenize an expression.

    Args:
        expr: str
            The expression to tokenize.

    Returns: list[Token]
    """
    return Lexer(expr).tokenize()


def parse(tokens: list[Token] | str) -> Node | None:
    """
    Parses a list of tokens or string into an AST (abstract syntax tree).

    Args:
        tokens: list[Token] | str
            The list of tokens or string to parse.

    Returns: Node | None
    """
    if type(tokens) == str:
        tokens = Lexer(tokens).tokenize()

    return Parser(tokens).parse()


def evaluate(expr: str | list[Token] | Node) -> Number | Callable | None:
    """
    Evaluates an expression.

    Args:
        expr: str | list[Token] | Node
            The expression to evaluate.

    Returns: Number | Callable | None
    """
    if type(expr) == str:
        expr = Lexer(expr).tokenize()

    if type(expr) == list:
        expr = Parser(expr).parse()

    return Interpreter(expr).interpret()
