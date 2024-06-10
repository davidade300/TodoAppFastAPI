"""
tests file
to run it all that is needed to open the project folder in the terminal 
and run  "pytest" on the console
"""


def test_qual_or_not_equal():
    """tests"""

    assert 3 == 3
    assert 3 != 1
    # assert 3 == 2


def test_is_instance():
    """tests"""

    assert isinstance("this is a string", str)
    assert not isinstance("10", int)


def test_type():
    """tests for types"""
    assert type("world" is not int)
    assert type("world" is str)


def test_boolean():
    """tests for booleans"""
    validated = True
    assert validated is True
    assert ("hello" == "world") is False


def test_greater_and_less_than():
    """test for greater/lesser"""
    assert 7 > 3
    assert 4 < 10


def test_list():
    """test for lists"""
    num_list = [1, 2, 3, 4, 5]
    any_list = [False, False]
    assert all(num_list)
    assert not any(any_list)
