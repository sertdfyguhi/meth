from meth import *
import unittest


class SimplifyTest(unittest.TestCase):
    def test_mul_var_same(self):
        self.assertEqual(
            simplify("2x + 3x"),
            BinaryOpNode(TT_MUL, 5, Token(TT_IDENTIFIER, "x")),
        )

    def test_mul_var_diff(self):
        self.assertEqual(
            simplify("4y + 2x"),
            BinaryOpNode(
                TT_MUL,
                2,
                BinaryOpNode(
                    TT_PLUS,
                    BinaryOpNode(TT_MUL, 2, Token(TT_IDENTIFIER, "y")),
                    Token(TT_IDENTIFIER, "x"),
                ),  # 2(2y + x)
            ),
        )

    def test_mul_var_diff_reverse(self):
        self.assertEqual(
            simplify("2y + 4x"),
            BinaryOpNode(
                TT_MUL,
                2,
                BinaryOpNode(
                    TT_PLUS,
                    Token(TT_IDENTIFIER, "y"),
                    BinaryOpNode(TT_MUL, 2, Token(TT_IDENTIFIER, "x")),
                ),  # 2(y + 2x)
            ),
        )
