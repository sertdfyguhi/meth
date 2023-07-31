import timeit
import meth

expr = meth.tokenize("1 + (2(2 * x) ^ 2) % 5")

# old_p = meth.Parser()
new_p = meth.Parser()


def new():
    new_p.parse(expr)


print("new:", timeit.timeit(new, number=10000, globals=globals()))
# print("old:", timeit.timeit(old, number=10000, globals=globals()))
