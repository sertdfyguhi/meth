import math


# inspect signature bypass
def log(x: float | int, base: int):
    return math.log(x, base)


BUILTINS = {
    "e": math.e,
    "pi": math.pi,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "atan2": math.atan2,
    "log": log,
    "log10": math.log10,
    "exp": math.exp,
    "sqrt": math.sqrt,
    "floor": math.floor,
    "ceil": math.ceil,
    "round": round,
    "abs": abs,
    "trunc": math.trunc,
}
