from timeit import timeit
import meth

parsed = meth.parse("2 + 3 ^ (2 - 1)")


def replace():
    meth.stringify(parsed).replace(" ", "")


def add_space():
    meth.stringify(parsed, True)


times = [timeit(add_space, number=50000, globals=globals()) for _ in range(10)]
print(sum(times) / len(times))
