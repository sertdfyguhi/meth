import meth

EXPRESSIONS = ["f(x) = 2x + x", "f(,)"]

interpreter = meth.Interpreter()

for expr in EXPRESSIONS:
    print(interpreter.interpret(meth.parse(expr)))
