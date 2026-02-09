from .token import TokenType
from .node import *


PRECEDNECE = {
    TokenType.ADD: 1,
    TokenType.MINUS: 1,
    TokenType.MUL: 2,
    TokenType.DIV: 2,
    TokenType.MOD: 2,
    TokenType.POW: 3,
}


def stringify(ast: Node) -> str:
    """
    Stringifies an AST into an equation.

    Args:
        ast: Node
            The tree to stringify.

    Returns: str
    """

    if isinstance(ast, AssignNode):
        return f"{stringify(ast.left)} = {stringify(ast.right)}"
    elif isinstance(ast, BinaryOpNode):  # TODO: add implied multiplication?
        left = stringify(ast.left)
        right = stringify(ast.right)
        op_precedence = PRECEDNECE[ast.value]

        if (
            isinstance(ast.left, BinaryOpNode)
            and PRECEDNECE[ast.left.value] < op_precedence
        ):
            left = f"({left})"

        if (
            isinstance(ast.right, BinaryOpNode)
            and PRECEDNECE[ast.right.value] < op_precedence
        ):
            right = f"({right})"

        return f"{left} {ast.value} {right}"
    elif isinstance(ast, UnaryOpNode):
        right = stringify(ast.right)
        # factorial is behind the number unlike plus and minus
        return f"{right}!" if ast.value == TokenType.FACT else f"{ast.value}{right}"
    elif isinstance(ast, FunctionNode):
        args = ", ".join([str(stringify(arg)) for arg in ast.right])
        return f"{stringify(ast.value)}({args})"
    elif isinstance(ast, (NumberNode, IdentifierNode)):
        return ast.value
    else:
        raise TypeError(f"Unknown type {type(ast)}.")
