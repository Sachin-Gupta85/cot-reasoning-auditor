"""Find and check inline arithmetic claims like ``3 * 4 = 12``.

CoT traces are full of little equations, and a wrong one often invalidates the
whole chain. We extract each ``a OP b = c`` claim and recompute it exactly.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

_EQUATION = re.compile(
    r"(-?\d+(?:\.\d+)?)\s*([+\-*/×÷])\s*(-?\d+(?:\.\d+)?)\s*=\s*(-?\d+(?:\.\d+)?)"
)
_OPS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "×": lambda a, b: a * b,
    "/": lambda a, b: a / b if b != 0 else None,
    "÷": lambda a, b: a / b if b != 0 else None,
}


@dataclass(frozen=True)
class Equation:
    lhs: str
    claimed: float
    actual: float | None
    ok: bool


def check_equations(text: str, tol: float = 1e-6) -> list[Equation]:
    out: list[Equation] = []
    for a, op, b, c in _EQUATION.findall(text):
        actual = _OPS[op](float(a), float(b))
        claimed = float(c)
        ok = actual is not None and abs(actual - claimed) <= tol
        out.append(Equation(f"{a} {op} {b}", claimed, actual, ok))
    return out
