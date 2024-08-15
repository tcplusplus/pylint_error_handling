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
    :raises ValueError: test < 0
    """
    if test < 0:
        raise ValueError()
    raise KeyError()

def test_multiple_exceptions2(test: int) -> None:
    """
    Hello world
    :param test:
    :raises ValueError: test < 0
    """
    if test < 0:
        raise ValueError()
    try:
        raise KeyError()
    except KeyError:
        pass

def hierarchical() -> None:
    """
    Hello world
    :raises KeyError: test
    :raises ZeroDivisionError: test
    """
    test_with_documentation()
    raise KeyError()

def hierarchical_with_error() -> None:  # pylint: disable=missing-exception-doc
    """
    Hello world
    :raises KeyError: test
    """
    test_with_documentation()
    raise KeyError()

def hierarchical_with_catch() -> None:
    """
    Hello world
    :raises KeyError:
    """
    try:
        test_with_documentation()
    except ZeroDivisionError:
        pass
    raise KeyError()

def test_general_errors() -> None:
    """
    Hello world
    """
    try:
        raise KeyError()
    except ValueError:
        pass
