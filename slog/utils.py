r"""
Supporting utilities for conducting unit tests.

Notes
-----
#.  Written by David C. Stauffer in March 2015.
#.  Copied to the slog library in February 2022 to avoid circular dependencies.
"""
#%% Imports
from contextlib import contextmanager
import doctest
from io import StringIO
import sys
from typing import Any, Callable, TypeVar
import unittest

#%% Constants
_F = TypeVar("_F", bound=Callable[..., Any])


#%% Decorators - consecutive
def consecutive(enumeration: _F) -> _F:
    r"""Class decorator for enumerations ensuring unique and consecutive member values that start from zero."""
    duplicates = []
    non_consecutive = []
    last_value = min(enumeration.__members__.values()) - 1  # type: ignore[attr-defined]
    if last_value != -1:
        raise ValueError(f"Bad starting value (should be zero): {last_value + 1}")
    for name, member in enumeration.__members__.items():  # type: ignore[attr-defined]
        if name != member.name:
            duplicates.append((name, member.name))
        if member != last_value + 1:
            non_consecutive.append((name, member))
        last_value = member
    if duplicates:
        alias_details = ", ".join(
            [f"{alias} -> {name}" for (alias, name) in duplicates]
        )
        raise ValueError(
            f"Duplicate values found in {enumeration.__name__}: {alias_details}"
        )
    if non_consecutive:
        alias_details = ", ".join(
            f"{name}: {int(member)}" for (name, member) in non_consecutive
        )
        raise ValueError(
            f"Non-consecutive values found in {enumeration.__name__}: {alias_details}"
        )
    return enumeration


#%% Functions - is_dunder
def is_dunder(name: str) -> bool:
    """
    Returns True if a __dunder__ name, False otherwise.

    Parameters
    ----------
    name : str
        Name of the file or method to determine if __dunder__ (Double underscore)

    Returns
    -------
    bool
        Whether the name is a dunder method or not

    Notes
    -----
    #.  Copied by David C. Stauffer in September 2020 from enum._is_dunder to allow it to be a
        public method.

    Examples
    --------
    >>> from slog import is_dunder
    >>> print(is_dunder('__init__'))
    True

    >>> print(is_dunder('_private'))
    False

    """
    # Note that this is copied from the enum library, as it is not part of their public API.
    return (
        len(name) > 4
        and name[:2] == name[-2:] == "__"
        and name[2] != "_"
        and name[-3] != "_"
    )


#%% Functions - capture_output
@contextmanager
def capture_output(mode: str = "out"):
    r"""
    Capture the stdout and stderr streams instead of displaying to the screen.

    Parameters
    ----------
    mode : str
        Mode to use when capturing output
            'out' captures just sys.stdout
            'err' captures just sys.stderr
            'all' captures both sys.stdout and sys.stderr

    Returns
    -------
    out : class StringIO
        stdout stream output
    err : class StringIO
        stderr stream output

    Notes
    -----
    #.  Written by David C. Stauffer in March 2015.

    Examples
    --------
    >>> from slog import capture_output
    >>> with capture_output() as out:
    ...     print('Hello, World!')
    >>> output = out.getvalue().strip()
    >>> out.close()
    >>> print(output)
    Hello, World!

    """
    # alias modes
    capture_out = mode in {"out", "all"}
    capture_err = mode in {"err", "all"}
    # create new string buffers
    new_out, new_err = StringIO(), StringIO()
    # alias the old string buffers for restoration afterwards
    old_out, old_err = sys.stdout, sys.stderr
    try:
        # override the system buffers with the new ones
        if capture_out:
            sys.stdout = new_out
        if capture_err:
            sys.stderr = new_err
        # yield results as desired
        if mode == "out":
            yield sys.stdout
        elif mode == "err":
            yield sys.stderr
        elif mode == "all":
            yield sys.stdout, sys.stderr
    finally:
        # restore the original buffers once all results are read
        sys.stdout, sys.stderr = old_out, old_err


#%% Unit test
if __name__ == "__main__":
    unittest.main(module="slog.tests.test_utils", exit=False)
    doctest.testmod(verbose=False)
