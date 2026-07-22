"""Turn a free-form chain-of-thought string into structured steps.

Handles the common shapes: ``Step 1: …`` / ``1) …`` / ``1. …`` numbered lists,
plain newline-separated lines, or a single paragraph (sentence-split as a
fallback). Also pulls out the trace's stated final answer.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

_NUMBERED = re.compile(r"^\s*(?:step\s*)?\d+[.):]\s*", re.I)
_SENT = re.compile(r"[^.!?\n]+[.!?]?")
_ANSWER = re.compile(r"(?:final\s+)?answer\s*(?:is|:|=)\s*(.+?)(?:[.\n]|$)", re.I)
_BOXED = re.compile(r"\\boxed\{([^{}]*)\}")
_NUMBER = re.compile(r"-?\d+(?:\.\d+)?")


@dataclass
class Step:
    index: int
    text: str


def parse_steps(trace: str) -> list[Step]:
    lines = [ln.strip() for ln in trace.strip().splitlines() if ln.strip()]
    if any(_NUMBERED.match(ln) for ln in lines):
        steps = [_NUMBERED.sub("", ln).strip() for ln in lines if _NUMBERED.match(ln)]
    elif len(lines) > 1:
        steps = lines
    else:
        steps = [s.strip() for s in _SENT.findall(trace) if s.strip()]
    return [Step(i, s) for i, s in enumerate(steps)]


def final_answer(trace: str) -> str | None:
    m = _BOXED.search(trace) or _ANSWER.search(trace)
    if m:
        return m.group(1).strip().rstrip(".")
    nums = _NUMBER.findall(trace)
    return nums[-1] if nums else None
