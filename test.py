import meth

# print(meth.simplify("2x + 2x"))

evaluator = meth.Evaluator()
evaluator.evaluate("x = 5")
print(evaluator.evaluate("x"))  # 5
