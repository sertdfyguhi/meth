import matplotlib.pyplot as plt
import numpy as np
import meth

STEP = 1 / 10


print("Simple equation grapher made using meth.")

equation = input("Input equation to graph (use x, y): ")
ast = meth.parse(meth.tokenize(equation))

start = int(input("Input start (default: -10): ") or -10)
end = int(input("Input end (default: 10): ") or 10)

x_points = np.arange(start, end, STEP)
y_points = []

if isinstance(ast, meth.AssignNode):
    pass
else:
    # y = x
    evaluator = meth.Evaluator()

    for x in x_points:
        evaluator.set_var("x", x)
        y = evaluator.evaluate(ast)
        y_points.append(y)

plt.plot(x_points, y_points)
plt.grid(True)
plt.show()
