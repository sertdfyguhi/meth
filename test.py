import meth

EXPRESSIONS = ["x = 2", "x + 3"]

interpreter = meth.Interpreter()

for expr in EXPRESSIONS:
    print(interpreter.interpret(meth.parse(expr)))
