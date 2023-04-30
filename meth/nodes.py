from .token import *


class BaseNode:
    def __init__(self, value, left=None, right=None, is_paren=False) -> None:
        self.value = value
        self.left = left
        self.right = right
        self.is_paren = is_paren

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value}, {self.left}, {self.right})"


class BinaryOpNode(BaseNode):
    pass


class FunctionNode(BaseNode):
    def __init__(self, name: str, args=None) -> None:
        super().__init__(name, args, is_paren=True)


class AssignNode(BaseNode):
    def __init__(self, left, right, is_paren=False) -> None:
        super().__init__(TT_EQUAL, left, right, is_paren)


class UnaryOpNode(BaseNode):
    def __init__(self, op_token, number, is_paren=False) -> None:
        super().__init__(op_token, number, is_paren=is_paren)
