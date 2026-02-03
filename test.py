import meth

# tokens = meth.tokenize("xsin")
# print(tokens)

# ast = meth.parse(tokens)
# print(ast)

# result = meth.Interpreter(ast).interpret()
# print(result)

evaluator = meth.Evaluator()
print(evaluator.evaluate("x = 2"))
print(evaluator.evaluate("y = 3"))
print(evaluator.evaluate("xytan(2)cos(7)3"))
