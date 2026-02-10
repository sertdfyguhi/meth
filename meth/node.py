from .token import TokenType

from numbers import Number


class Node:
    """A node in an AST."""

    def __init__(self, left, value, right):
        """
        Initializes the node.

        Args:
            left: Any
                The left of the node.
            value: Any
                The value of the node.
            right: Any
                The right of the node.
        """
        self.left = left
        self.value = value
        self.right = right

    def __repr__(self):
        return f"Node({self.left}, {self.value}, {self.right})"


class NumberNode(Node):
    """A node for numbers."""

    def __init__(self, value: Number):
        """
        Initializes the number node.

        Args:
            value: Number
                The number.
        """
        super().__init__(None, value, None)

    def __repr__(self):
        return f"Number({self.value})"


class IdentifierNode(Node):
    """A node for identifiers."""

    def __init__(self, value: str):
        """
        Initializes the identifier node.

        Args:
            value: str
                The identifier.
        """
        super().__init__(None, value, None)

    def __repr__(self):
        return f"Identifier({self.value})"


class AssignNode(Node):
    """A node for assignment."""

    def __init__(self, left: Node, right: Node):
        """
        Initializes the assignment node.

        Args:
            left: Node
                The left of the assignment.
            right: Node
                The right of the assignment.
        """
        super().__init__(left, TokenType.ASSIGN, right)

    def __repr__(self):
        return f"Assign({self.left} = {self.right})"


class BinaryOpNode(Node):
    """A node for binary operations."""

    def __repr__(self):
        return f"BinaryOp({self.left}, {self.value}, {self.right})"


class UnaryOpNode(Node):
    """A node for unary operations."""

    def __init__(self, operator: TokenType, value: Node):
        """
        Initializes the unary node.

        Args:
            operator: TokenType
                The operator of the unary operation.
            value: Node
                The value in the unary operation.
        """
        super().__init__(None, operator, value)

    def __repr__(self):
        return f"UnaryOp({self.value}, {self.right})"


# can also act as multiplication, eg: x(1 + 2)
class FunctionNode(Node):
    """A node for function calls and implied multiplication for identifiers."""

    def __init__(self, name: IdentifierNode, args: list[Node]):
        """
        Initializes the function node.

        Args:
            name: IdentifierNode
                The name of the function called or the identifier of the multiplication.
            args: list[Node]
                The arguments of the function call or the inside of the multiplicatiom.
        """
        super().__init__(None, name, args)

    def __repr__(self):
        return f"Function({self.value}, {self.right})"
