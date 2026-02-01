import meth

# tokens = meth.tokenize("x = 4")
# print(tokens)

# ast = meth.parse(tokens)
# print(ast)

# result = meth.Interpreter(ast).interpret()
# print(result)

evaluator = meth.Evaluator()
print(evaluator.evaluate("x = 4"))
print(evaluator.evaluate("2x"))
