"""The individual auditors. Each takes the parsed trace and yields Issues.

Deterministic, rule-based, and conservative — they flag concrete defects
(a wrong sum, a variable asserted two ways, a final answer that doesn't follow
from the work) rather than guessing at semantic quality.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from .arithmetic import check_equations
from .parse import Step, final_answer

_ASSIGN = re.compile(r"\b([a-zA-Z]\w*)\s*=\s*(-?\d+(?:\.\d+)?)\b")
_NUMBER = re.compile(r"-?\d+(?:\.\d+)?")


@dataclass(frozen=True)
class Issue:
    check: str
    severity: str           # "high" | "medium" | "low"
    step_index: int | None
    message: str


def arithmetic_issues(steps: list[Step]) -> list[Issue]:
    issues = []
    for s in steps:
        for eq in check_equations(s.text):
            if not eq.ok:
                issues.append(Issue("arithmetic", "high", s.index,
                                    f"'{eq.lhs} = {eq.claimed:g}' but actual is {eq.actual:g}"))
    return issues


def contradiction_issues(steps: list[Step]) -> list[Issue]:
    """Flag a variable asserted with two different constant values."""
    seen: dict[str, tuple[float, int]] = {}
    issues = []
    for s in steps:
        for var, val in _ASSIGN.findall(s.text):
            v = float(val)
            if var in seen and abs(seen[var][0] - v) > 1e-9:
                prev_val, prev_idx = seen[var]
                issues.append(Issue("contradiction", "medium", s.index,
                                    f"'{var}' = {prev_val:g} (step {prev_idx}) but = {v:g} here"))
            seen[var] = (v, s.index)
    return issues


def answer_consistency_issues(steps: list[Step], trace: str) -> list[Issue]:
    """The stated final answer should match the last computed equation result."""
    ans = final_answer(trace)
    if ans is None:
        return []
    m = _NUMBER.search(ans)
    if not m:
        return []
    ans_val = float(m.group())

    last_result = None
    for s in steps:
        eqs = check_equations(s.text)
        if eqs:
            last_result = eqs[-1].actual if eqs[-1].actual is not None else eqs[-1].claimed
    if last_result is not None and abs(last_result - ans_val) > 1e-6:
        return [Issue("answer_consistency", "high", None,
                      f"final answer {ans_val:g} != last computed result {last_result:g}")]
    return []


def grounding_issues(steps: list[Step], trace: str) -> list[Issue]:
    """The final answer should be *derived*, not merely declared.

    A grounded answer appears in the work and then again when stated (count >= 2).
    If the answer number shows up only once — in the "answer is X" line — it was
    pulled from nowhere.
    """
    ans = final_answer(trace)
    if ans is None:
        return [Issue("grounding", "low", None, "no final answer could be identified")]
    m = _NUMBER.search(ans)
    if not m:
        return []
    ans_num = m.group()
    body = " ".join(s.text for s in steps)
    if _NUMBER.findall(body).count(ans_num) < 2:
        return [Issue("grounding", "medium", None,
                      f"final answer {ans_num} is stated but never derived in the steps")]
    return []
