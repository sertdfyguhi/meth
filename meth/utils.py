from .nodes import BaseNode
from .token import *


def get_final_node(tree: BaseNode, stop_at: list = []):
    node = tree

    while (
        getattr((n := getattr(node, "right", None)), "right", None)
        and n.value not in stop_at
        and not n.is_paren
    ):
        node = node.right

    return node


def get_from_depth(tree: BaseNode, depth: int):
    node = tree

    for _ in range(depth):
        node = node.left

    return node
