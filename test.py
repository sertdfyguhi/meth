import meth

tokens = meth.tokenize("3(1 + 2)(2 * 3)")
print(tokens)

ast = meth.parse(tokens)
print(ast)

result = meth.interpret(ast)
print(result)
