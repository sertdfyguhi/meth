from .interpreter import Interpreter
from .nodes import BaseNode
from .parser import Parser
from .lexer import Lexer


def parse(expr: str):
    """Parse an expression."""
    tokens = Lexer(expr).tokenize()
    return Parser(tokens).parse()


def evaluate(ast: BaseNode):
    """Evaluate a parsed expression."""
    return Interpreter(ast).interpret()
