import meth

evaluator = meth.Evaluator()
evaluator.evaluate("f(x) = sin(x^pi)")
print(evaluator.evaluate("f(1.0)"))
print(evaluator.evaluate("f(2.0)"))
