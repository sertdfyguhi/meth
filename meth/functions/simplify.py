from ..utils import create_number_token
from ..parser import Parser
from ..lexer import Lexer
from ..token import *
from ..nodes import *


def simplify(expr: BaseNode | str):
    "Simplify an expression. WARNING: This is unfinished and may contain bugs."
    if type(expr) == str:
        expr = Parser().parse(Lexer().tokenize(expr))
    return simplify_node(expr)


def is_number(token: Token):
    return token in [TT_INT, TT_FLOAT]


def is_var_mul(node: BinaryOpNode):
    return node.value == TT_MUL and is_number(node.left) and node.right == TT_IDENTIFIER


def simplify_node(node: BaseNode | Token):
    node_t = type(node)

    if node is None or type(node) == Token:
        return node
    elif node_t == BinaryOpNode:
        return simplify_binaryop(node)
    elif node_t == FunctionNode:
        return simplify_function(node)
    else:
        return node


def simplify_binaryop(node: BinaryOpNode):
    left = simplify_node(node.left)
    right = simplify_node(node.right)
    t_left = type(left)
    t_right = type(right)

    # TODO: handle cases like xx == x²
    if node.value == TT_PLUS:
        if t_left == t_right == Token:
            # check for 1 + 2
            if is_number(left) and is_number(right):
                res = left.value + right.value
                return create_number_token(res)
            elif (  # check for x + x
                left == TT_IDENTIFIER
                and right == TT_IDENTIFIER
                and left.value == right.value
            ):
                return BinaryOpNode(
                    TT_MUL,
                    create_number_token(2),
                    create_number_token(left.value),
                    True,
                )
        elif t_left == t_right == BinaryOpNode:
            if left.value == right.value == TT_MUL:
                # handle case 2x + 2x
                if left.right == TT_IDENTIFIER and right.right == TT_IDENTIFIER:
                    left_l = simplify_node(left.left)
                    # TODO: check for cases like 2xy + 2xz and 2x + 2xy
                    if not is_number(left_l):
                        pass

                    right_l = simplify_node(right.left)
                    if not is_number(right_l):
                        pass

                    # check for cases like 3x + 2y that wont work
                    max_v = max(left_l.value, right_l.value)
                    min_v = min(left_l.value, right_l.value)
                    if left.right != right.right and max_v % min_v != 0:
                        return node

                    # check for cases like 2x + 2x or 2y + 2x
                    if left.right == right.right:
                        return BinaryOpNode(
                            TT_MUL,
                            create_number_token(left_l.value + right_l.value),
                            left.right,
                            True,
                        )
                    else:
                        is_equal = max_v == min_v
                        return BinaryOpNode(
                            TT_MUL,
                            min_v,
                            BinaryOpNode(
                                TT_PLUS,
                                left.right
                                if is_equal
                                or left_l.value != max_v  # check for 2x + 4y
                                else BinaryOpNode(
                                    TT_MUL,
                                    create_number_token(max_v // min_v),
                                    left.right,
                                ),
                                right.right
                                if is_equal
                                or right_l.value != max_v  # check for 2x + 4y
                                else BinaryOpNode(
                                    TT_MUL,
                                    create_number_token(max_v // min_v),
                                    right.right,
                                ),
                                True,
                            ),
                        )
    else:
        return node


def simplify_function(node: FunctionNode) -> BaseNode:
    iden = simplify_node(node.value)
    args = node.left

    # TODO: handle cases like 2x(2x)
    if len(args) == 1 and is_number(iden):
        # handle 2(4)
        if is_number(args[0]):
            return create_number_token(iden.value * args[0].value)
        elif type(args[0]) == BinaryOpNode:
            # handle 2(2x)
            if (
                args[0].value == TT_MUL
                and is_number(args[0].left)
                and args[0].right == TT_IDENTIFIER
            ):
                return BinaryOpNode(
                    TT_MUL,
                    create_number_token(iden.value * args[0].left.value),
                    args[0].right,
                )
            elif (
                args[0].value == TT_PLUS
                and is_var_mul(args[0].left)
                and is_var_mul(args[0].right)
            ):
                # handle cases like 2(2x + 2y)
                print(iden.value * args[0].left.left.value)
                return BinaryOpNode(
                    TT_PLUS,
                    BinaryOpNode(
                        TT_MUL,
                        create_number_token(iden.value * args[0].left.left.value),
                        args[0].left.right,
                    ),
                    BinaryOpNode(
                        TT_MUL,
                        create_number_token(iden.value * args[0].right.left.value),
                        args[0].right.right,
                    ),
                )

    return FunctionNode(iden, [simplify_node(arg) for arg in args])
