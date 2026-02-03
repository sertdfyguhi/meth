from functools import lru_cache
from typing import Callable
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


CONSTANTS = {
    "π": math.pi,
    "τ": math.tau,
    "ϕ": (1 + math.sqrt(5)) / 2,
    "e": math.e,
}

BUILTINS = {
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
    "exp": math.exp,
    "sqrt": math.sqrt,
    "rad": math.radians,
    "abs": abs,
    "trunc": math.trunc,
    "floor": math.floor,
    "ceil": math.ceil,
    "round": round,
    "min": meth_min,
    "max": meth_max,
}


# makes it 0.02s faster
@lru_cache(maxsize=len(BUILTINS))
def is_builtin(name: str) -> bool:
    """
    Checks to see if name is a builtin.

    Args:
        name: str
            Name to check.

    Returns: bool
    """
    return name in BUILTINS


def get_builtin(name: str) -> Callable | None:
    """
    Get builtin from name.

    Args:
        name: str
            Name of builtin.

    Returns: Callable | None if not found
    """
    return BUILTINS.get(name)
