"""
Test pylint for simple functions
"""

def test_without_documentation() -> None:  # pylint: disable=missing-exception-doc
    """
    Hello world
    """
    raise ZeroDivisionError()

def test_with_documentation() -> None:
    """
    Hello world
    :raises ZeroDivisionError: for testing purposes
    """
    raise ZeroDivisionError()

def test_exceptions_are_already_handled() -> None:
    """
    Hello world
    """
    try:
        raise ZeroDivisionError()
    except ZeroDivisionError:
        pass

def test_multiple_exceptions(test: int) -> None:
    """
    Hello world
    :param test:
    :raises KeyError: test
    """
    if test < 0:
        raise ValueError()
    raise KeyError()
