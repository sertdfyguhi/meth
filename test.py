import meth

# tokens = meth.tokenize("2af(x + 2, 2) * (x - 2)")
# print(tokens)

# ast = meth.parse(tokens)
# print(ast)

# result = meth.Interpreter(ast).interpret()
# print(result)

evaluator = meth.Evaluator()
print(evaluator.evaluate("f(x, y) = 2x + y"))
print(evaluator.evaluate("f(2, 3)"))
