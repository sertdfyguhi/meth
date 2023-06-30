import math


def meth_ln(x: float | int):
    return math.log(x)


# inspect signature bypass
def meth_log(x: float | int, base: int):
    return math.log(x, base)


def meth_min(a: int | float, b: int | float):
    return a if a < b else b


def meth_max(a: int | float, b: int | float):
    return a if a > b else b


# fmt: off
CONSTANTS = {
    "pi|π": math.pi,
    "tau|τ": math.tau,
    "phi|ϕ": (1 + math.sqrt(5)) / 2,
    "e": math.e,
}

BUILTINS = {
    # trigonometric functions
    "sin": math.sin,
    "sinh": math.sinh,
    "cos": math.cos,
    "cosh": math.cosh,
    "tan": math.tan,
    "tanh": math.tanh,
    "csc": lambda x: 1 / math.sin(x),
    "sec": lambda x: 1 / math.cos(x),
    "cot": lambda x: 1 / math.tan(x),

    "asin": math.asin,
    "asinh": math.asinh,
    "acos": math.acos,
    "acosh": math.acosh,
    "atan": math.atan,
    "atan2": math.atan2,
    "atanh": math.atanh,

    "ln": meth_ln,
    "log": meth_log,
    "log2": math.log2,
    "log10": math.log10,
    "exp": math.exp,
    "sqrt": math.sqrt,

    "rad": math.radians,
    "abs": abs,
    "trunc": math.trunc,
    "floor": math.floor,
    "ceil": math.ceil,
    "round": round,
    "min": meth_min,
    "max": meth_max
}

def get_builtin(name: str):
    """Get builtin from name."""
    if name in BUILTINS:
        return BUILTINS[name]

    for const in CONSTANTS:
        if name in const.split('|'):
            return CONSTANTS[const]
