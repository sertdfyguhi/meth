from meth.functions.simplify import simplify
from meth.nodes import *
import unittest


class SimplifyTest(unittest.TestCase):
    def test_mul_var_same(self):
        # 2x + 3x = 5x
        self.assertEqual(
            simplify("2x + 3x"),
            BinaryOpNode(TT_MUL, Token(TT_INT, 5), Token(TT_IDENTIFIER, "x")),
        )

    def test_mul_var_diff(self):
        # 4y + 2x = 2(2y + x)
        self.assertEqual(
            simplify("4y + 2x"),
            BinaryOpNode(
                TT_MUL,
                2,
                BinaryOpNode(
                    TT_PLUS,
                    BinaryOpNode(TT_MUL, Token(TT_INT, 2), Token(TT_IDENTIFIER, "y")),
                    Token(TT_IDENTIFIER, "x"),
                ),
            ),
        )

    def test_mul_var_diff_reverse(self):
        # 2y + 4x = 2(y + 2x)
        self.assertEqual(
            simplify("2y + 4x"),
            BinaryOpNode(
                TT_MUL,
                2,
                BinaryOpNode(
                    TT_PLUS,
                    Token(TT_IDENTIFIER, "y"),
                    BinaryOpNode(TT_MUL, Token(TT_INT, 2), Token(TT_IDENTIFIER, "x")),
                ),
            ),
        )

    def test_mul_func_var(self):
        # 2(2x) = 4x
        self.assertEqual(
            simplify("2(2x)"),
            BinaryOpNode(TT_MUL, Token(TT_INT, 4), Token(TT_IDENTIFIER, "x")),
        )

    def test_mul_func_var_diff(self):
        # 2(2x + 2y) = 4x + 4y
        self.assertEqual(
            simplify("2(2x + 2y)"),
            BinaryOpNode(
                TT_PLUS,
                BinaryOpNode(TT_MUL, Token(TT_INT, 4), Token(TT_IDENTIFIER, "x")),
                BinaryOpNode(TT_MUL, Token(TT_INT, 4), Token(TT_IDENTIFIER, "y")),
            ),
        )
