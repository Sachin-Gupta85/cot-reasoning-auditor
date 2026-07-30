from cotaudit.checks import (
    answer_consistency_issues,
    arithmetic_issues,
    contradiction_issues,
    grounding_issues,
)
from cotaudit.parse import parse_steps


def test_arithmetic_issue_flagged():
    issues = arithmetic_issues(parse_steps("3 * 4 = 11 apples"))
    assert len(issues) == 1 and issues[0].severity == "high"


def test_no_arithmetic_issue_when_correct():
    assert arithmetic_issues(parse_steps("3 * 4 = 12 apples")) == []


def test_contradiction_on_conflicting_variable():
    issues = contradiction_issues(parse_steps("Let x = 5\nNow x = 7"))
    assert len(issues) == 1 and issues[0].check == "contradiction"


def test_no_contradiction_on_consistent_variable():
    assert contradiction_issues(parse_steps("x = 5\nx = 5 still")) == []


def test_answer_inconsistent_with_work():
    trace = "2 + 2 = 4\nThe answer is 5"
    issues = answer_consistency_issues(parse_steps(trace), trace)
    assert len(issues) == 1 and issues[0].severity == "high"


def test_answer_consistent_with_work():
    trace = "2 + 2 = 4\nThe answer is 4"
    assert answer_consistency_issues(parse_steps(trace), trace) == []


def test_ungrounded_answer_flagged():
    trace = "We use 7 and 8 here\nThe answer is 42"
    issues = grounding_issues(parse_steps(trace), trace)
    assert len(issues) == 1 and issues[0].check == "grounding"


def test_grounded_answer_ok():
    trace = "It is 42 from the table\nThe answer is 42"
    assert grounding_issues(parse_steps(trace), trace) == []
