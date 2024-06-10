"""
tests file
to run it all that is needed to open the project folder in the terminal 
and run  "pytest" on the console
"""
import pytest


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


class Student:
    """student class for pytest"""

    def __init__(self, first_name: str, last_name: str,
                 major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

        """
        https://pylint.readthedocs.io/en/latest/user_guide/messages/warning/redefined-outer-name.html
        """


@pytest.fixture(name="default_student")
def default_student_fixture() -> Student:
    """fixture for test"""
    return Student("John", "Doe", "Computer Science", 3)


def test_person_initialization(default_student):
    """test for student"""
    assert default_student.first_name == "John", "First name should be John"
    assert default_student.last_name == "Doe", "Last name should be Doe"
    assert default_student.major == "Computer Science"
    assert default_student.years == 3
