from .token import *


class BaseNode:
    def __init__(self, value, left=None, right=None, is_paren=False) -> None:
        """Base class for all node tyoes."""
        self.value = value
        self.left = left
        self.right = right
        self.is_paren = is_paren

        self.name = type(self).__name__

    def __repr__(self) -> str:
        return f"{self.name}({self.value}, {self.left}, {self.right})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseNode):
            return False

        return (
            self.value == other.value
            and self.left == other.left
            and self.right == other.right
            # and self.is_paren == other.is_paren
        )


class BinaryOpNode(BaseNode):
    pass


class FunctionNode(BaseNode):
    def __init__(self, name, args=None) -> None:
        super().__init__(name, args, is_paren=True)


class AssignNode(BaseNode):
    def __init__(self, left, right, is_paren=False) -> None:
        super().__init__(TT_EQUAL, left, right, is_paren)


class UnaryOpNode(BaseNode):
    def __init__(self, op_token, number, is_paren=False) -> None:
        super().__init__(op_token, number, is_paren=is_paren)
