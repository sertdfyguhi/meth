from .interpreter import Interpreter
from .nodes import BaseNode
from .parser import Parser
from .lexer import Lexer


def parse(expr: str | list[str]):
    tokens = Lexer(expr).tokenize()
    ast = Parser(tokens).parse()

    return ast


def evaluate(ast: BaseNode):
    pass
