import solution


def test_factorial_basic():
    assert solution.factorial(5) == 120


def test_factorial_zero():
    assert solution.factorial(0) == 1


def test_factorial_one():
    assert solution.factorial(1) == 1