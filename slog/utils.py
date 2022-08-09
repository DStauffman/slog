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
from typing import Any, Callable, Iterator, Optional, TextIO, TypeVar, Union
import unittest

#%% Constants
_F = TypeVar("_F", bound=Callable[..., Any])


#%% Classes
class CaptureOutputResult:
    r"""Class used to keep track of the standard output and error streams to assist the capture_output function."""

    def __init__(self, stdout: Optional[Union[StringIO, TextIO]] = None, stderr: Optional[Union[StringIO, TextIO]] = None):
        self.stdout = stdout
        self.stderr = stderr

    def close(self) -> None:
        r"""Closes any open streams."""
        if self.stdout:
            self.stdout.close()

        if self.stderr:
            self.stderr.close()

    def get_output(self) -> str:
        r"""Returns what was captured in the output stream."""
        return CaptureOutputResult.get_stream(self.stdout)

    def get_error(self) -> str:
        r"""Returns what was captured in the error stream."""
        return CaptureOutputResult.get_stream(self.stderr)

    @staticmethod
    def get_stream(std: Optional[Union[StringIO, TextIO]]) -> str:
        r"""Gets the contents of the given stream."""
        if not std:
            return ""

        if isinstance(std, StringIO):
            return std.getvalue().strip()

        if isinstance(std, TextIO):
            return "\n".join(std.readlines())

        raise Exception(f"Unknown type {type(std)}")


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
        alias_details = ", ".join([f"{alias} -> {name}" for (alias, name) in duplicates])
        raise ValueError(f"Duplicate values found in {enumeration.__name__}: {alias_details}")
    if non_consecutive:
        alias_details = ", ".join(f"{name}: {int(member)}" for (name, member) in non_consecutive)
        raise ValueError(f"Non-consecutive values found in {enumeration.__name__}: {alias_details}")
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
    return len(name) > 4 and name[:2] == name[-2:] == "__" and name[2] != "_" and name[-3] != "_"


#%% Functions - capture_output
@contextmanager
def capture_output(mode: str = "out") -> Iterator[CaptureOutputResult]:
    r"""
    Capture the stdout and stderr streams instead of displaying to the screen.

    Parameters
    ----------
    mode : str
        Mode to use when capturing output
            "out" captures just sys.stdout
            "err" captures just sys.stderr
            "all" captures both sys.stdout and sys.stderr

    Returns
    -------
    out : class StringIO
        stdout stream output
    err : class StringIO
        stderr stream output

    Notes
    -----
    #.  Written by David C. Stauffer in March 2015.
    #.  Updated by David C. Stauffer in August 2022 based on stackoverflow answer by user rshepp.
        See: https://stackoverflow.com/questions/73228026/python-typing-for-context-manager-and-string-literal/

    Examples
    --------
    >>> from slog import capture_output
    >>> with capture_output() as ctx:
    ...     print('Hello, World!')
    >>> output = ctx.get_output()
    >>> ctx.close()
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
            yield CaptureOutputResult(stdout=sys.stdout)
        elif mode == "err":
            yield CaptureOutputResult(stderr=sys.stderr)
        elif mode == "all":
            yield CaptureOutputResult(stdout=sys.stdout, stderr=sys.stderr)
    finally:
        # restore the original buffers once all results are read
        sys.stdout, sys.stderr = old_out, old_err


#%% Unit test
if __name__ == "__main__":
    unittest.main(module="slog.tests.test_utils", exit=False)
    doctest.testmod(verbose=False)
