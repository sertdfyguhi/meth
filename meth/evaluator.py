from .interpreter import Interpreter
from .parser import Parser
from .lexer import Lexer


class Evaluator:
    def __init__(self):
        self.vars = {}

    def evaluate(self, expr: str):
        tokens = Lexer(expr).tokenize()
        ast = Parser(tokens).parse()
        result = Interpreter(ast).interpret()

        return result
