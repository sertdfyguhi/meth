from ..parser import Parser
from ..lexer import Lexer
from ..token import *
from ..nodes import *


def simplify(expr: BaseNode | str):
    "Simplify an expression."
    if type(expr) == str:
        expr = Parser(Lexer(expr).tokenize()).parse()
    return _simplify_node(expr)


def _simplify_node(node: BaseNode | Token):
    node_t = type(node)

    if node is None or type(node) == Token:
        return node
    elif node_t == BinaryOpNode:
        return _simplify_binaryop(node)
    elif node_t == FunctionNode:
        return _simplify_function(node)
    else:
        return node


def _simplify_binaryop(node: BinaryOpNode):
    left = _simplify_node(node.left)
    right = _simplify_node(node.right)
    t_left = type(left)
    t_right = type(right)

    if node.value == TT_PLUS:
        if t_left == t_right == Token:
            # check for 1 + 2
            if left in [TT_INT, TT_FLOAT] and right in [TT_INT, TT_FLOAT]:
                res = left.value + right.value
                return Token(TT_INT if type(res) == int else TT_FLOAT, res)
            elif (  # check for x + x
                left == TT_IDENTIFIER
                and right == TT_IDENTIFIER
                and left.value == right.value
            ):
                return BinaryOpNode(TT_MUL, 2, left.value, True)
        elif t_left == t_right == BinaryOpNode:
            # check if its a case like 2x + 2x
            if (
                left.value == right.value == TT_MUL
                and left.right == TT_IDENTIFIER
                and right.right == TT_IDENTIFIER
            ):
                left_l = _simplify_node(left.left)
                # TODO: check for cases like 2xy + 2xz and 2x + 2xy
                if left_l not in [TT_INT, TT_FLOAT]:
                    pass

                right_l = _simplify_node(right.left)
                if right_l not in [TT_INT, TT_FLOAT]:
                    pass

                # check for cases like 3x + 2y that wont work
                max_v = max(left_l.value, right_l.value)
                min_v = min(left_l.value, right_l.value)
                if left.right != right.right and max_v % min_v != 0:
                    return node

                # check for cases like 2x + 2x or 2y + 2x
                if left.right == right.right:
                    return BinaryOpNode(
                        TT_MUL, left_l.value + right_l.value, left.right, True
                    )
                else:
                    is_equal = max_v == min_v
                    return BinaryOpNode(
                        TT_MUL,
                        min_v,
                        BinaryOpNode(
                            TT_PLUS,
                            left.right
                            if is_equal or left_l.value != max_v  # check for 2x + 4y
                            else BinaryOpNode(TT_MUL, max_v // min_v, left.right),
                            right.right
                            if is_equal or right_l.value != max_v  # check for 2x + 4y
                            else BinaryOpNode(TT_MUL, max_v // min_v, right.right),
                            True,
                        ),
                    )
    else:
        return node


def _simplify_function(node: FunctionNode) -> BaseNode:
    pass
