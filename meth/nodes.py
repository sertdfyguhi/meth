class BaseNode:
    def __init__(self, value, left=None, right=None) -> None:
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.left}, {self.value}, {self.right})"


class BinaryOpNode(BaseNode):
    pass


class UnaryOpNode(BaseNode):
    def __init__(self, op_token, number) -> None:
        super().__init__(op_token, number)


class VarAssignNode(BaseNode):
    def __init__(self, var_name: str, value: BaseNode) -> None:
        super().__init__(var_name, value)


class VarAccessNode(BaseNode):
    def __init__(self, var_name: str) -> None:
        super().__init__(var_name)
