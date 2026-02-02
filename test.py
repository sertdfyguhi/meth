import meth

tokens = meth.tokenize("1 + 5 * 2 ^ 3")
print(tokens)

ast = meth.parse(tokens)
print(ast)

result = meth.Interpreter(ast).interpret()
print(result)

# evaluator = meth.Evaluator()
# print(evaluator.evaluate("x = 4"))
# print(evaluator.evaluate("2x"))
