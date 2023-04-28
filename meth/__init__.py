from .interpreter import Interpreter
from .parser import Parser
from .lexer import Lexer


def parse(expr: str):
    tokens = Lexer(expr).tokenize()

    return tokens


def evaluate(ast):
    pass
