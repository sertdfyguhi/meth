import meth

tokens = meth.tokenize("xx + 1")
print(tokens)

ast = meth.parse(tokens)
print(ast)

# result = meth.interpret(ast)
# print(result)
