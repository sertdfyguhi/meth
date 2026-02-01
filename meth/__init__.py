from .interpreter import Interpreter
from .evaluator import Evaluator
from .parser import Parser
from .lexer import Lexer
from .token import *
from .node import *

__version__ = "2.0.0"
__author__ = "sertdfyguhi"


def tokenize(expr: str) -> list[Token]:
    """
    Tokenize an expression.

    Args:
        expr: str
            The expression to tokenize.

    Returns: list[Token]
    """
    return Lexer(expr).tokenize()


def parse(tokens: list[Token]) -> Node | None:
    """
    Parses a list of tokens into an AST (abstract syntax tree).

    Args:
        tokens: list[Token]
            The list of tokens to parse.

    Returns: Node | None
    """
    return Parser(tokens).parse()


def interpret(ast: Node) -> int | float | None:
    """
    Interprets an AST (abstract syntax tree).

    Args:
        ast: Node
            The AST to interpret.

    Returns: int | float | None
    """
    return Interpreter(ast).interpret()
