import meth

EXPRESSIONS = ["sqrt(1, 2) + 2"]

interpreter = meth.Interpreter()

for expr in EXPRESSIONS:
    print(interpreter.interpret(meth.parse(expr)))
