from meth import *
import unittest


class EvaluateTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.eval = Evaluator()

    def test_plus(self):
        self.assertEqual(self.eval.evaluate("5 + 15"), 20)

    def test_subtract(self):
        self.assertEqual(self.eval.evaluate("5 - 15"), -10)

    def test_multiply(self):
        self.assertEqual(self.eval.evaluate("5 * 10"), 50)

    def test_division(self):
        self.assertEqual(self.eval.evaluate("30 / 15"), 2)

    def test_modulo(self):
        self.assertEqual(self.eval.evaluate("15 % 10"), 5)

    def test_power(self):
        self.assertEqual(self.eval.evaluate("10 ^ 3"), 1000)

    def test_unary(self):
        self.assertEqual(self.eval.evaluate("-22"), -22)

    def test_unary_mul(self):
        self.assertEqual(self.eval.evaluate("-10 * 5"), -50)

    def test_unary_mul_var(self):
        self.eval.evaluate("x = 3")
        self.assertEqual(self.eval.evaluate("-10x"), -30)

    def test_bracket_mul(self):
        self.assertEqual(self.eval.evaluate("(2 * 2)(2 + 1)"), 12)

    def test_func(self):
        self.eval.evaluate("f(x) = 2x + sqrt(9)")
        self.assertEqual(self.eval.evaluate("f(5)"), 13)

    def test_plus_func(self):
        self.assertEqual(self.eval.evaluate("1 + 2 * abs(2)"), 5)
