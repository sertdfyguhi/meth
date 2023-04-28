from .interpreter import Interpreter
from .parser import Parser
from .lexer import Lexer


def parse(expr: str):
    tokens = Lexer(expr).tokenize()
    ast = Parser(tokens).parse()

    return ast


def evaluate(ast):
    pass
