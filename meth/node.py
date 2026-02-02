from .token import TT_ASSIGN


class Node:
    def __init__(self, left, value, right):
        self.left = left
        self.value = value
        self.right = right

    def __repr__(self):
        return f"Node({self.left}, {self.value}, {self.right})"


class AssignNode(Node):
    def __init__(self, left, right):
        super().__init__(left, TT_ASSIGN, right)

    def __repr__(self):
        return f"Assign({self.left} = {self.right})"


class BinaryOpNode(Node):
    def __repr__(self):
        return f"BinaryOp({self.left}, {self.value}, {self.right})"


class UnaryOpNode(Node):
    def __init__(self, operator, value):
        super().__init__(None, operator, value)

    def __repr__(self):
        return f"UnaryOp({self.value}, {self.right})"


# can also act as multiplication, eg: x(1 + 2)
class FunctionNode(Node):
    def __init__(self, name, args):
        super().__init__(None, name, args)

    def __repr__(self):
        return f"Function({self.value}, {self.right})"


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
