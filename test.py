import meth

evaluator = meth.Evaluator()
evaluator.evaluate("x = 10")
print(evaluator.get_var("x ="))
