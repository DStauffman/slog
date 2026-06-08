r"""
Supporting utilities for conducting unit tests.

Notes
-----
#.  Written by David C. Stauffer in March 2015.
#.  Copied to the slog library in February 2022 to avoid circular dependencies.

"""

# %% Imports
from collections.abc import Callable, Iterator
from contextlib import contextmanager
import doctest
from io import StringIO
from pathlib import Path
import sys
from typing import Any, overload, TextIO, TypeVar
import unittest

# %% Constants
_F = TypeVar("_F", bound=Callable[..., Any])


# %% Classes
class CaptureOutputResult:
    r"""Class used to keep track of the standard output and error streams to assist the capture_output function."""

    def __init__(self, stdout: StringIO | TextIO | None = None, stderr: StringIO | TextIO | None = None) -> None:
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
    def get_stream(std: StringIO | TextIO | None) -> str:
        r"""Gets the contents of the given stream."""
        if not std:
            return ""

        if isinstance(std, StringIO):
            return std.getvalue().strip()

        if isinstance(std, TextIO):
            return "\n".join(std.readlines())

        raise Exception(f"Unknown type {type(std)}")  # pylint: disable=broad-exception-raised  # noqa: TRY002


# %% Decorators - consecutive
def consecutive(enumeration: _F) -> _F:
    r"""Class decorator for enumerations ensuring unique and consecutive member values that start from zero."""
    duplicates = []
    non_consecutive = []
    last_value = min(enumeration.__members__.values()) - 1  # type: ignore[attr-defined]  # ty: ignore[unresolved-attribute]
    if last_value != -1:
        raise ValueError(f"Bad starting value (should be zero): {last_value + 1}")
    for name, member in enumeration.__members__.items():  # type: ignore[attr-defined]  # ty: ignore[unresolved-attribute]
        if name != member.name:
            duplicates.append((name, member.name))
        if member != last_value + 1:
            non_consecutive.append((name, member))
        last_value = member
    if duplicates:
        alias_details = ", ".join([f"{alias} -> {name}" for (alias, name) in duplicates])
        raise ValueError(f"Duplicate values found in {enumeration.__name__}: {alias_details}")  # fmt: skip  # ty: ignore[unresolved-attribute]
    if non_consecutive:
        alias_details = ", ".join(f"{name}: {int(member)}" for (name, member) in non_consecutive)
        raise ValueError(f"Non-consecutive values found in {enumeration.__name__}: {alias_details}")  # fmt: skip  # ty: ignore[unresolved-attribute]
    return enumeration


# %% Functions - is_dunder
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
    return len(name) > 4 and name[:2] == name[-2:] == "__" and name[2] != "_" and name[-3] != "_"  # noqa: PLR2004


# %% line_wrap
@overload
def line_wrap(text: str, wrap: int = 80, min_wrap: int = 0, indent: int = 4, line_cont: str = "\\") -> str: ...
@overload
def line_wrap(text: list[str], wrap: int = 80, min_wrap: int = 0, indent: int = 4, line_cont: str = "\\") -> list[str]: ...
def line_wrap(
    text: str | list[str], wrap: int = 80, min_wrap: int = 0, indent: int = 4, line_cont: str = "\\"
) -> str | list[str]:
    r"""
    Wrap lines of text to the specified length, breaking at any whitespace characters.

    Parameters
    ----------
    text : str or list of str
        Text to be wrapped
    wrap : int, optional
        Number of characters to wrap text at, default is 80
    min_wrap : int, optional
        Minimum number of characters to wrap at, default is 0
    indent : int, optional
        Number of characters to indent the next line with, default is 4
    line_cont : str, optional
        Line continuation character, default is "\"

    Returns
    -------
    out : str or list of str
        wrapped form of text

    Examples
    --------
    >>> from slog import line_wrap
    >>> text = ("lots of repeated words " * 4).strip()
    >>> wrap = 40
    >>> out = line_wrap(text, wrap)
    >>> print(out)
    lots of repeated words lots of \
        repeated words lots of repeated \
        words lots of repeated words

    """
    # check if single str
    text_list = [text] if isinstance(text, str) else text
    # create the pad for any newline
    pad = " " * indent
    # initialize output
    out: list[str] = []
    # loop through text lines
    for this_line in text_list:
        # determine if too long
        while len(this_line) > wrap:
            # find the last whitespace to break on, possibly with a minimum start
            space_break = this_line.rfind(" ", min_wrap, wrap - 1)
            if space_break == -1 or space_break <= indent:
                raise ValueError(f'The specified min_wrap:wrap of "{min_wrap}:{wrap}" was too small.')
            # add the shorter line
            out.append(this_line[:space_break] + " " + line_cont)
            # reduce and repeat
            this_line = pad + this_line[space_break + 1 :]  # noqa: PLW2901
        # add the final shorter line
        out.append(this_line)
    if isinstance(text, str):
        return "\n".join(out)
    return out


# %% Functions - list_python_files
def list_python_files(folder: Path, recursive: bool = False, include_all: bool = False) -> list[Path]:
    r"""
    Returns a list of all non dunder python files in the folder.

    Parameters
    ----------
    folder : class pathlib.Path
        Folder location
    recursive : bool, optional
        Whether to search recursively, default is False
    include_all : bool, optional
        Whether to include all files, even the __dunder__ ones

    Returns
    -------
    files : list
        All *.py files that don't start with __

    Notes
    -----
    #.  Written by David C. Stauffer in March 2020.

    Examples
    --------
    >>> from slog import list_python_files, get_root_dir
    >>> folder = get_root_dir()
    >>> files = list_python_files(folder)

    """
    # find all the files that end in .py and are not dunder (__name__) files
    if not folder.is_dir():
        return []
    files = list(folder.glob("*.py")) if include_all else [file for file in folder.glob("*.py") if not is_dunder(file.stem)]  # fmt: skip
    if recursive:
        dirs = [x for x in folder.glob("*") if x.is_dir()]
        for this_folder in sorted(dirs):
            files.extend(list_python_files(this_folder, recursive=recursive, include_all=include_all))
    return files


# %% Functions - capture_output
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


# %% Unit test
if __name__ == "__main__":
    unittest.main(module="slog.tests.test_utils", exit=False)
    doctest.testmod(verbose=False)
