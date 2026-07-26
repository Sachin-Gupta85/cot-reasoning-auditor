from cotaudit.audit import audit

CLEAN = (
    "Step 1: 3 boxes of 4 apples, so 3 * 4 = 12 apples.\n"
    "Step 2: He eats 2, so 12 - 2 = 10.\n"
    "Step 3: The final answer is 10."
)

BROKEN = (
    "Step 1: 3 boxes of 4 apples, so 3 * 4 = 11 apples.\n"   # wrong product
    "Step 2: The final answer is 11."
)


def test_clean_trace_scores_perfect():
    report = audit(CLEAN)
    assert report.valid
    assert report.score == 1.0
    assert report.issues == []
    assert report.n_steps == 3


def test_broken_trace_is_flagged():
    report = audit(BROKEN)
    assert not report.valid                      # has a high-severity issue
    assert report.score < 1.0
    assert any(i.check == "arithmetic" for i in report.by_severity("high"))


def test_score_floors_at_zero():
    report = audit(BROKEN)
    assert report.score >= 0.0
