class Node:
    def __init__(self, left, value, right):
        self.left = left
        self.value = value
        self.right = right

    def __repr__(self):
        return f"Node({self.left}, {self.value}, {self.right})"


class BinaryOpNode(Node):
    def __repr__(self):
        return f"BinaryOp({self.left}, {self.value}, {self.right})"


class NumberNode(Node):
    def __init__(self, value):
        super().__init__(None, value, None)

    def __repr__(self):
        return f"Number({self.value})"


class IdentifierNode(Node):
    def __init__(self, value):
        super().__init__(None, value, None)

    def __repr__(self):
        return f"Identifier({self.value})"
