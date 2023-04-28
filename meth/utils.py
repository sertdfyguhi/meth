from .nodes import BaseNode


def get_last_right_node(tree: BaseNode, stop_at: list = []):
    node = tree
    depth = 0

    while (
        getattr((n := getattr(node, "right", None)), "right", None)
        and n.value not in stop_at
    ):
        node = node.right
        depth += 1

    return node, depth


def get_from_depth(tree: BaseNode, depth: int):
    node = tree

    for _ in range(depth):
        node = node.left

    return node
