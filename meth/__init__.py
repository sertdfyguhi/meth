from .interpreter import Interpreter
from .nodes import BaseNode
from .parser import Parser
from .lexer import Lexer


def parse(expr: str):
    """Parse an expression."""
    tokens = Lexer(expr).tokenize()
    ast = Parser(tokens).parse()

    return ast


def evaluate(ast: BaseNode):
    """Evaluate a parsed expression."""
    pass
