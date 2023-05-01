from .interpreter import Interpreter
from .nodes import BaseNode
from .parser import Parser
from .lexer import Lexer


def parse(expr: str):
    """Parse an expression."""
    tokens = Lexer(expr).tokenize()
    return Parser(tokens).parse()


def evaluate(ast: BaseNode | str):
    """Evaluate a parsed expression."""
    if type(ast) == str:
        ast = parse(ast)

    return Interpreter().interpret(ast)
