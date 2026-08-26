import solution


def test_add_positive():
    assert solution.add(2, 3) == 5


def test_add_negative():
    assert solution.add(-1, -5) == -6


def test_add_zero():
    assert solution.add(10, 0) == 10