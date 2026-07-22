"""Run every check over a trace and produce a scored audit report."""
from __future__ import annotations

from dataclasses import dataclass, field

from .checks import (
    Issue,
    answer_consistency_issues,
    arithmetic_issues,
    contradiction_issues,
    grounding_issues,
)
from .parse import parse_steps

_PENALTY = {"high": 0.5, "medium": 0.25, "low": 0.1}


@dataclass
class AuditReport:
    score: float                         # 1.0 = clean, 0.0 = badly broken
    valid: bool                          # no high-severity issues
    issues: list[Issue] = field(default_factory=list)
    n_steps: int = 0

    def by_severity(self, severity: str) -> list[Issue]:
        return [i for i in self.issues if i.severity == severity]


def audit(trace: str) -> AuditReport:
    steps = parse_steps(trace)
    issues: list[Issue] = []
    issues += arithmetic_issues(steps)
    issues += contradiction_issues(steps)
    issues += answer_consistency_issues(steps, trace)
    issues += grounding_issues(steps, trace)

    penalty = sum(_PENALTY.get(i.severity, 0.1) for i in issues)
    score = max(0.0, 1.0 - penalty)
    valid = not any(i.severity == "high" for i in issues)
    return AuditReport(score=round(score, 3), valid=valid, issues=issues, n_steps=len(steps))
