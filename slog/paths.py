r"""
Generic path functions that can be called independent of the current working directory.

Notes
-----
#.  Written by David C. Stauffer in March 2015.
#.  Moved out of utils and into paths.py file in February 2019 by David C. Stauffer.
#.  Adapted into slog library by David C. Stauffer in February 2022.
"""

#%% Imports
import doctest
from functools import lru_cache
from pathlib import Path
import unittest


#%% Functions - get_root_dir
@lru_cache
def get_root_dir() -> Path:
    r"""
    Return the folder that contains this source file and thus the root folder for the whole code.

    Returns
    -------
    class pathlib.Path
        Location of the folder that contains all the source files for the code.

    Notes
    -----
    #.  Written by David C. Stauffer in March 2015.

    Examples
    --------
    >>> from slog import get_root_dir
    >>> print("p = ", repr(get_root_dir()))  # doctest: +ELLIPSIS
    p = .../slog/slog')

    """
    # this folder is the root directory based on the location of this file (utils.py)
    return Path(__file__).resolve().parent


#%% Functions - get_tests_dir
@lru_cache
def get_tests_dir() -> Path:
    r"""
    Return the default test folder location.

    Returns
    -------
    class pathlib.Path
        Location of the folder that contains all the test files for the code.

    Notes
    -----
    #.  Written by David C. Stauffer in March 2015.

    Examples
    --------
    >>> from slog import get_tests_dir
    >>> print("p = ", repr(get_tests_dir()))  # doctest: +ELLIPSIS
    p = .../slog/tests')

    """
    # this folder is the "tests" subfolder
    return get_root_dir() / "tests"


#%% Unit test
if __name__ == "__main__":
    unittest.main(module="slog.tests.test_paths", exit=False)
    doctest.testmod(verbose=False)
