class BaseNode:
    def __init__(self, value, left=None, right=None, is_paren=False) -> None:
        self.value = value
        self.left = left
        self.right = right
        self.is_paren = is_paren

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.left}, {self.value}, {self.right})"


class BinaryOpNode(BaseNode):
    pass


class UnaryOpNode(BaseNode):
    def __init__(self, op_token, number, is_paren=False) -> None:
        super().__init__(op_token, number, is_paren=is_paren)


class VarAssignNode(BaseNode):
    def __init__(self, var_name: str, value: BaseNode, is_paren=False) -> None:
        super().__init__(var_name, value, is_paren=is_paren)


class VarAccessNode(BaseNode):
    def __init__(self, var_name: str) -> None:
        super().__init__(var_name)
