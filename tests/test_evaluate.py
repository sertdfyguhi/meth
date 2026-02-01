from meth import *
import unittest


class EvaluateTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.eval = Evaluator()

    def test_add(self):
        self.assertEqual(self.eval.evaluate("1 + 2"), 3)

    def test_minus(self):
        self.assertEqual(self.eval.evaluate("2 - 1"), 1)

    def test_multiply(self):
        self.assertEqual(self.eval.evaluate("2 * 3"), 6)

    def test_divide(self):
        self.assertEqual(self.eval.evaluate("6 / 2"), 3)

    def test_multiply_precedence(self):
        self.assertEqual(self.eval.evaluate("1 + 2 * 3"), 7)

    def test_divide_precedence(self):
        self.assertEqual(self.eval.evaluate("1 + 4 / 2"), 3)

    def test_multiple_precedence(self):
        self.assertEqual(self.eval.evaluate("1 + 2 * 3 - 4 / 2"), 5)

    def test_parentheses(self):
        self.assertEqual(self.eval.evaluate("(1 + 2) * 3"), 9)

    def test_nested_parentheses(self):
        self.assertEqual(self.eval.evaluate("(100 - (10 + 20)) / 2"), 35)

    def test_multiple_parentheses(self):
        self.assertEqual(self.eval.evaluate("10 * (2 + 3) / (10 - 5)"), 10)

    def test_unary_minus(self):
        self.assertEqual(self.eval.evaluate("-1"), -1)

    def test_unary_plus(self):
        self.assertEqual(self.eval.evaluate("+1"), 1)

    def test_multiple_unary(self):
        self.assertEqual(self.eval.evaluate("--1"), 1)

    def test_unary_parentheses(self):
        self.assertEqual(self.eval.evaluate("-(1 + 2)"), -3)

    def test_unary_precedence(self):
        self.assertEqual(self.eval.evaluate("3 + -(1 + 2)"), 0)

    def test_implied_multiplication(self):
        self.assertEqual(self.eval.evaluate("3(1 + 2)"), 9)

    def test_unary_implied_multiplication(self):
        self.assertEqual(self.eval.evaluate("-3(1 + 2)"), -9)

    def test_implied_multiplication_parentheses(self):
        self.assertEqual(self.eval.evaluate("(1 + 2)(3 + 4)"), 21)

    def test_unary_implied_multiplication_parentheses(self):
        self.assertEqual(self.eval.evaluate("-(1 + 2)(3 + 4)"), -21)
