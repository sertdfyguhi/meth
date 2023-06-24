from ..token import *
from ..nodes import *

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
    node_t = type(node)

    if node_t == Token:
        return str(node.value) if node.value else TT_CONV[node.type]
    elif node_t == BinaryOpNode:
        equation_str = (
            f"{stringify(node.left)} {TT_CONV[node.value]} {stringify(node.right)}"
        )

        return f"({equation_str})" if node.is_paren else equation_str
    elif node_t == UnaryOpNode:
        return f"{TT_CONV[node.value]}{stringify(node.left)}"
    else:
        raise ValueError("Could not stringify node.")
