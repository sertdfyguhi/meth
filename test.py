import meth

tokens = meth.tokenize("1/ 0")
print(tokens)

ast = meth.parse(tokens)
print(ast)

result = meth.evaluate(ast)
print(result)

# print(meth.stringify(ast))

# evaluator = meth.Evaluator()
# print(evaluator.evaluate("2 + 3"))
