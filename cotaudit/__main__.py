"""Offline demo — audit a clean trace and a subtly broken one.

    python -m cotaudit
"""
from __future__ import annotations

from .audit import audit

CLEAN = (
    "Step 1: There are 3 shelves with 4 books each, so 3 * 4 = 12 books.\n"
    "Step 2: We remove 2 damaged books, so 12 - 2 = 10 books.\n"
    "Step 3: The final answer is 10."
)

BROKEN = (
    "Step 1: There are 3 shelves with 4 books each, so 3 * 4 = 14 books.\n"   # wrong
    "Step 2: Let n = 14.\n"
    "Step 3: Actually n = 10 after removing some.\n"                           # contradiction
    "Step 4: The final answer is 9."                                          # ungrounded + inconsistent
)


def show(label: str, trace: str) -> None:
    r = audit(trace)
    status = "VALID ✅" if r.valid else "INVALID ❌"
    print(f"\n=== {label}: {status}  score={r.score}  ({r.n_steps} steps) ===")
    if not r.issues:
        print("   no issues found")
    for i in r.issues:
        loc = f"step {i.step_index}" if i.step_index is not None else "trace"
        print(f"   [{i.severity:>6}] {i.check:<18} ({loc}): {i.message}")


def main() -> None:
    show("clean reasoning", CLEAN)
    show("broken reasoning", BROKEN)


if __name__ == "__main__":
    main()
