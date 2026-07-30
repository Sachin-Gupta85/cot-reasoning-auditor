from cotaudit.arithmetic import check_equations
from cotaudit.parse import final_answer, parse_steps


def test_parse_numbered_steps():
    trace = "Step 1: do this.\nStep 2: do that.\nStep 3: done."
    steps = parse_steps(trace)
    assert len(steps) == 3
    assert steps[0].text == "do this."


def test_parse_plain_lines_and_paragraph():
    assert len(parse_steps("first line\nsecond line")) == 2
    assert len(parse_steps("One sentence. Two sentence. Three.")) == 3


def test_final_answer_variants():
    assert final_answer("blah \\boxed{42}") == "42"
    assert final_answer("The final answer is 10.") == "10"
    assert final_answer("just a 7 somewhere") == "7"


def test_check_equations_correct_and_wrong():
    assert check_equations("3 * 4 = 12")[0].ok
    bad = check_equations("3 * 4 = 11")[0]
    assert not bad.ok and bad.actual == 12.0


def test_check_equations_unicode_ops_and_div_zero():
    assert check_equations("6 × 7 = 42")[0].ok
    dz = check_equations("10 / 0 = 0")[0]
    assert not dz.ok and dz.actual is None


def test_check_equations_finds_multiple():
    eqs = check_equations("2 + 2 = 4 and later 5 * 5 = 25")
    assert len(eqs) == 2 and all(e.ok for e in eqs)
