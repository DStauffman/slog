r"""
Functions related to the command-line interface (CLI) for the slog library.

Notes
-----
#.  Written by David C. Stauffer in March 2020.
#.  Adapted to the slog library by David C. Stauffer in February 2022.
"""

#%% Imports
import doctest
from pathlib import Path
import sys
import unittest

from slog.enums import ReturnCodes
from slog.paths import get_root_dir
from slog.version import version_info


#%% Functions - main
def main() -> int:
    r"""Main function called when executed using the command line api."""
    # check for no command option
    if len(sys.argv) >= 2:
        command = sys.argv[1].lower()
    else:
        command = "help"
    # check for alternative forms of help with the base dcs command
    if command in {"help", "--help", "-h"}:
        try:
            return_code = print_help()
        except:
            return_code = ReturnCodes.bad_help_file
    elif command in {"version", "--version", "-v"}:
        try:
            return_code = print_version()
        except:
            return_code = ReturnCodes.clean
    elif command == "tests":
        # run tests using pytest
        import pytest  # pylint: disable=import-outside-toplevel

        exit_code = pytest.main(
            [str(get_root_dir() / "tests"), "-rfEsP"] + sys.argv[2:]
        )
        return_code = ReturnCodes.clean if exit_code == 0 else ReturnCodes.test_failures
    else:
        print(f'Unknown command: "{command}"')
        return_code = ReturnCodes.bad_command
    return sys.exit(return_code)


#%% Functions - print_help
def print_help(help_file: Path = None) -> int:
    r"""
    Prints the contents of the README.rst file.

    Returns
    -------
    return_code : int
        Return code for whether the help file was successfully loaded

    Examples
    --------
    >>> from slog import print_help
    >>> print_help() # doctest: +SKIP

    """
    if help_file is None:
        help_file = get_root_dir().parent / "README.rst"
    if not help_file.is_file():
        print(f'Warning: help file at "{help_file}" was not found.')
        return ReturnCodes.bad_help_file
    with open(help_file, encoding="utf-8") as file:
        text = file.read()
    print(text)
    return ReturnCodes.clean


#%% Functions - print_version
def print_version() -> int:
    r"""Prints the version of the library.

    Returns
    -------
    return_code : int
        Return code for whether the version was successfully read

    Examples
    --------
    >>> from slog import print_version
    >>> print_version()  # doctest: +SKIP

    """
    try:
        version = ".".join(str(x) for x in version_info)
        return_code = ReturnCodes.clean
    except:
        version = "unknown"
        return_code = ReturnCodes.bad_version
    print(version)
    return return_code


#%% Unit test
if __name__ == "__main__":
    unittest.main(module="slog.tests.test_cli", exit=False)
    doctest.testmod(verbose=False)
