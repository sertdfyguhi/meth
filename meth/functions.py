from .token import TokenType
from .node import *


PRECEDENCE = {
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

    match ast:
        case AssignNode():
            return f"{stringify(ast.left)} = {stringify(ast.right)}"

        case BinaryOpNode():
            left = stringify(ast.left)
            right = stringify(ast.right)
            op_precedence = PRECEDENCE[ast.value]

            if (
                isinstance(ast.left, BinaryOpNode)
                and PRECEDENCE[ast.left.value] < op_precedence
            ):
                left = f"({left})"

            if (
                isinstance(ast.right, BinaryOpNode)
                and PRECEDENCE[ast.right.value] < op_precedence
            ):
                right = f"({right})"

            return f"{left} {ast.value.value} {right}"

        case UnaryOpNode():
            right = stringify(ast.right)
            # factorial is behind the number unlike plus and minus
            return (
                f"{right}!"
                if ast.value == TokenType.FACT
                else f"{ast.value.value}{right}"
            )

        case FunctionNode():
            args = ", ".join([str(stringify(arg)) for arg in ast.right])
            return f"{stringify(ast.value)}({args})"

        case NumberNode():
            return str(ast.value)

        case IdentifierNode():
            return ast.value

        case _:
            raise TypeError(f"Unknown type {type(ast)}.")
