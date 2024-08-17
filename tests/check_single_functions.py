"""
Test pylint for simple functions
"""
import json

import requests

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

def test_general_errors() -> None:  # pylint: disable=missing-exception-doc
    """
    Hello world
    """
    try:
        raise KeyError()
    except ValueError:
        pass

def test_general_errors2() -> None:
    """
    Hello world
    """
    try:
        raise KeyError()
    except Exception:   # pylint: disable=broad-exception-caught
        pass

def test_multi_try_catch() -> None:     # pylint: disable=missing-exception-doc
    """
    Hello World
    """
    try:
        raise ValueError()
    except ValueError:
        pass
    raise ValueError()

def test_requests() -> None:
    """
    Hello world
    :raises TimeoutError: on timeout
    :raises ConnectionError: no internet
    """
    requests.get('http://www.google.com', timeout=1)

def test_requests_no_comments() -> None:    # pylint: disable=missing-exception-doc
    """
    Hello world
    """
    result = requests.get('http://www.google.com', timeout=1)
    print(result)

def test_json() -> None:
    """
    Hello world
    :raises JSONDecodeError: todo
    """
    a = json.loads('sdf')
    print(a)

def test_json_no_comments() -> None:  # pylint: disable=missing-exception-doc
    """
    Hello world
    """
    a = json.loads('sdf')
    print(a)
