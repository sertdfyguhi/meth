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

    def test_modulo(self):
        self.assertEqual(self.eval.evaluate("7 % 2"), 1)

    def test_power(self):
        self.assertEqual(self.eval.evaluate("3 ^ 2"), 9)

    def test_power_syntax2(self):
        self.assertEqual(self.eval.evaluate("3 ** 2"), 9)

    def test_factorial(self):
        self.assertEqual(self.eval.evaluate("3!"), 6)

    def test_multiply_precedence(self):
        self.assertEqual(self.eval.evaluate("1 + 2 * 3"), 7)

    def test_divide_precedence(self):
        self.assertEqual(self.eval.evaluate("1 + 4 / 2"), 3)

    def test_modulo_precedence(self):
        self.assertEqual(self.eval.evaluate("1 + 5 % 2"), 2)

    def test_power_precedence(self):
        self.assertEqual(self.eval.evaluate("1 + 5 * 2 ^ 3"), 41)

    def test_factorial_precedence(self):
        self.assertEqual(self.eval.evaluate("1 + 5 * 3! ^ 2"), 181)

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

    def test_unary_with_parentheses(self):
        self.assertEqual(self.eval.evaluate("-(1 + 2)"), -3)

    def test_unary_precedence(self):
        self.assertEqual(self.eval.evaluate("3 + -(1 + 2)"), 0)

    def test_implied_multiplication(self):
        self.assertEqual(self.eval.evaluate("3(1 + 2)"), 9)

    def test_implied_multiplication_with_unary(self):
        self.assertEqual(self.eval.evaluate("-3(1 + 2)"), -9)

    def test_implied_multiplication_with_parentheses(self):
        self.assertEqual(self.eval.evaluate("(1 + 2)(3 + 4)"), 21)

    def test_implied_multiplication_with_parentheses_with_unary(self):
        self.assertEqual(self.eval.evaluate("-(1 + 2)(3 + 4)"), -21)

    def test_assignment(self):
        self.eval.evaluate("x = 1")
        self.assertEqual(self.eval.evaluate("x"), 1)

    def test_assignment_with_expression(self):
        self.eval.evaluate("x = 1 + 2 * 3 / 3")
        self.assertEqual(self.eval.evaluate("x"), 3)

    def test_implied_multiplication_with_variables(self):
        self.eval.evaluate("x = 1")
        self.assertEqual(self.eval.evaluate("2x"), 2)

    def test_implied_multiplication_with_multiple_variables(self):
        self.eval.evaluate("x = 2")
        self.eval.evaluate("y = 3")
        self.assertEqual(self.eval.evaluate("4xy"), 24)

    def test_implied_multiplication_with_variables_with_unary(self):
        self.eval.evaluate("x = 1")
        self.assertEqual(self.eval.evaluate("-2x"), -2)

    def test_function(self):
        self.eval.evaluate("f(x) = 2x")
        self.assertEqual(self.eval.evaluate("f(2)"), 4)

    def test_function_with_multiple_arguments(self):
        self.eval.evaluate("f(x, y) = 2x + y")
        self.assertEqual(self.eval.evaluate("f(2, 3)"), 7)

    def test_function_with_implied_multiplication(self):
        self.eval.evaluate("f(x) = 2x")
        self.assertEqual(self.eval.evaluate("3f(2)"), 12)

    def test_builtin(self):
        # sin(pi)
        self.assertAlmostEqual(self.eval.evaluate("sin(π)"), 0)

    def test_builtin_multiplication_with_multiple_variables(self):
        self.eval.evaluate("x = 2")
        self.eval.evaluate("y = 3")
        self.assertEqual(self.eval.evaluate("xysqrt(4)"), 12)

    def test_builtin_multiplication_with_builtin(self):
        self.assertEqual(self.eval.evaluate("sqrt(4)sqrt(9)"), 6)

    def test_builtin_multiplication_with_builtin_and_variables(self):
        self.eval.evaluate("x = 2")
        self.eval.evaluate("y = 3")
        self.assertEqual(self.eval.evaluate("xsqrt(4)ysqrt(9)"), 36)
