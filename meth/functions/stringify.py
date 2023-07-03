from ..token import *
from ..nodes import *
from .. import error

TT_CONV = {
    TT_LBRACKET: "(",
    TT_RBRACKET: ")",
    TT_EQUAL: "=",
    TT_COMMA: ",",
    TT_PLUS: "+",
    TT_MINUS: "-",
    TT_MUL: "*",
    TT_DIV: "/",
    TT_MOD: "%",
    TT_POW: "^",
}


def stringify(node: BaseNode | Token) -> str:
    """
    Stringifies a tree into an equation string.

    Args:
        node: Node | Token
            The tree to turn into an equation string.

    Returns: str
    """
    node_t = type(node)

    if node_t == Token:
        return str(node.value) if node.value else TT_CONV[node.type]
    elif node_t == BinaryOpNode:
        # check for 3x
        if (
            node.value == TT_MUL
            and (is_left := node.left == TT_IDENTIFIER)
            or node.right == TT_IDENTIFIER
        ):
            rval, lval = node.right.value, node.left.value
            return f"{rval if is_left else lval}{lval if is_left else rval}"
        else:
            equation_str = (
                f"{stringify(node.left)} {TT_CONV[node.value]} {stringify(node.right)}"
            )
            return f"({equation_str})" if node.is_paren else equation_str
    elif node_t == UnaryOpNode:
        return f"{TT_CONV[node.value]}{stringify(node.left)}"
    elif node_t == AssignNode:
        return f"{stringify(node.left)} = {stringify(node.right)}"
    elif node_t == FunctionNode:
        return (
            f"{stringify(node.value)}({', '.join([stringify(n) for n in node.left])})"
        )
    else:
        raise ValueError("Could not stringify node.")
