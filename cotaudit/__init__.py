"""cot-reasoning-auditor — audit chain-of-thought traces for consistency.

Rule-based, deterministic checks for arithmetic errors, variable contradictions,
answer-vs-work inconsistency and ungrounded answers. Pure standard library.
"""
from .arithmetic import Equation, check_equations
from .audit import AuditReport, audit
from .checks import (
    Issue,
    answer_consistency_issues,
    arithmetic_issues,
    contradiction_issues,
    grounding_issues,
)
from .parse import Step, final_answer, parse_steps

__all__ = [
    "Equation", "check_equations",
    "AuditReport", "audit",
    "Issue", "answer_consistency_issues", "arithmetic_issues",
    "contradiction_issues", "grounding_issues",
    "Step", "final_answer", "parse_steps",
]
