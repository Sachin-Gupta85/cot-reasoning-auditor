# 🔬 cot-reasoning-auditor — audit chain-of-thought for consistency

> A deterministic auditor for chain-of-thought traces. It parses the reasoning
> into steps and flags **concrete** defects — a wrong sum, a variable asserted
> two ways, a final answer that doesn't follow from the work, an answer pulled
> from nowhere — then scores the trace. Rule-based and reproducible; no
> model-in-the-loop, zero dependencies.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Focus](https://img.shields.io/badge/focus-reasoning%20verification-6f42c1)
![Tests](https://img.shields.io/badge/tests-pytest%20(17)-brightgreen)

## 🧩 The checks
| Check | Severity | Catches |
|---|---|---|
| **arithmetic** | high | inline equations that don't compute (`3 * 4 = 14`) — recomputed exactly |
| **answer_consistency** | high | the stated answer ≠ the last computed result |
| **contradiction** | medium | a variable asserted with two different values (`n = 14` … `n = 10`) |
| **grounding** | medium | a final answer that is *declared* but never *derived* in the steps |

## 🧠 Why rule-based
LLM-as-judge auditing is itself unreliable and non-deterministic. These checks
are **exact and reproducible**: they recompute arithmetic, track variable
bindings, and trace the answer back to the work — so the same trace always gets
the same verdict. That's what makes the auditor usable as a reward signal or a
CI gate rather than another fuzzy score.

```
=== broken reasoning: INVALID ❌  score=0.0  (4 steps) ===
   [  high] arithmetic         (step 0): '3 * 4 = 14' but actual is 12
   [medium] contradiction      (step 2): 'n' = 14 (step 1) but = 10 here
   [  high] answer_consistency (trace): final answer 9 != last computed result 12
   [medium] grounding          (trace): final answer 9 is stated but never derived
```

## 🚀 Run
```bash
python -m cotaudit        # offline demo: a clean trace vs a subtly broken one
```

## ✅ Test
```bash
pip install -r requirements-dev.txt && python -m pytest -q
```

## Where it fits
Pairs naturally with [`rlvr-verifiers`](https://github.com/Sachin-Gupta85/rlvr-verifiers):
that one rewards a *correct answer*; this one checks whether the *reasoning that
produced it* actually holds together — process verification, not just outcome.

---
MIT licensed. Part of a portfolio of agent-evaluation and LLM-infra projects.
