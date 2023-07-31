from .nodes import *
from .token import *


def get_leaf_node_left(
    tree: BaseNode, stop_at_paren: bool = False, stop_at: list = []
) -> BaseNode:
    """
    Get leftest leaf node of a tree.

    Args:
        tree: Node
            Tree to get from.
        stop_at_paren: bool = False
            Stops at the node before if the left of that node is parenthesized.
        stop_at: list[TT_] = []
            List of token types to stop at.

    Return: Node
    """
    node = tree

    try:
        while (
            (n := node.left).left
            and n.value not in stop_at
            and (stop_at_paren or not n.is_paren)
        ):
            node = node.left
    except AttributeError:
        pass

    return node


def get_leaf_node_right(
    tree: BaseNode, stop_at_paren: bool = False, stop_at: list = []
) -> BaseNode:
    """
    Get rightest leaf node of a tree.

    Args:
        tree: Node
            Tree to get from.
        stop_at_paren: bool = False
            Stops at the node before if the right of that node is parenthesized.
        stop_at: list[TT_] = []
            List of token types to stop at.

    Return: Node
    """
    node = tree

    try:
        while (
            (n := node.right).right
            and n.value not in stop_at
            and (stop_at_paren or not n.is_paren)
        ):
            node = node.right
    except AttributeError:
        pass

    return node


def get_from_depth_left(tree: BaseNode, depth: int) -> BaseNode:
    """
    Get the leftest node of a tree using a depth.

    Args:
        tree: Node
            Tree to get from.
        depth: int
            Depth starting from root of tree.

    Returns: Node
    """
    node = tree

    for _ in range(depth):
        node = node.left

    return node


def get_from_depth_right(tree: BaseNode, depth: int):
    """
    Get the rightest node of a tree using a depth.

    Args:
        tree: Node
            Tree to get from.
        depth: int
            Depth starting from root of tree.

    Returns: Node
    """
    node = tree

    for _ in range(depth):
        node = node.right

    return node


def create_number_token(number: int | float) -> Token:
    """
    Shorthand function to create a token from a number using its type.

    Args:
        number: int | float
            Number to create the token from.

    Returns: Token
    """
    is_int = type(number) == int
    return Token(TT_INT if is_int else TT_FLOAT, number)
