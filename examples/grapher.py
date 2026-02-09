import matplotlib.pyplot as plt
import numpy as np
import meth

STEP = 1 / 10
X_LIMIT = (-10, 10)
Y_LIMIT = (-10, 10)

print("Simple equation grapher made using meth.")

x_or_y = input("Axis (x or y, default: y): ").strip().lower() or "y"
if x_or_y not in "xy":
    print("Axis has to be x or y.")
    exit(0)

equation = input(f"Input equation to graph (use x, y)\n{x_or_y} = ")
ast = meth.parse(equation)

start = int(input("Input start (default: -20): ") or -20)
end = int(input("Input end (default: 20): ") or 20)

a_points = np.arange(start, end, STEP)
b_points = []

evaluator = meth.Evaluator()

for a in a_points:
    evaluator.set_var("x" if x_or_y == "y" else "y", a)
    b = evaluator.evaluate(ast)
    b_points.append(b)

full_equation = f"{x_or_y} = {equation}"

if x_or_y == "y":
    plt.plot(a_points, b_points, label=full_equation)
else:
    plt.plot(b_points, a_points, label=full_equation)

plt.title(f"Graph of {full_equation}")
plt.xlabel("x")
plt.ylabel("y")
plt.axhline(0, color="black", linewidth=1)
plt.axvline(0, color="black", linewidth=1)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.xlim(X_LIMIT)
plt.ylim(Y_LIMIT)
plt.show()
