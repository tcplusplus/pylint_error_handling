"""
Test pylint for simple functions
"""

def test_without_documentation() -> None:
    """
    Hello world
    """
    raise ZeroDivisionError()  # pylint: disable=missing-exception-doc

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
