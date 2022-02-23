r"""
Define custom log levels and return codes.

Notes
-----
#.  Written by David C. Stauffer in July 2015.
#.  Modified by David C. Stauffer in March 2020 to add ReturnCode class for use in commands, and as
    a great example use case.
#.  Split into a stand-alone library by David C. Stauffer in February 2022.
"""

#%% Imports
import doctest
from enum import Enum, EnumMeta
import logging
from typing import ClassVar, List
import unittest

from slog.utils import consecutive, is_dunder


#%% MetaClasses - _EnumMetaPlus
class _EnumMetaPlus(EnumMeta):
    r"""
    Overrides the repr/str methods of the EnumMeta class to display all possible values.

    Also makes the __getattr__ attribute error more explicit.
    """

    def __repr__(cls) -> str:
        return "\n".join((repr(field) for field in cls))  # type: ignore[var-annotated]

    def __str__(cls) -> str:
        return "\n".join((str(field) for field in cls))  # type: ignore[var-annotated]

    def __getattr__(cls, name: str) -> int:
        r"""Return the enum member matching `name`."""
        if is_dunder(name):
            raise AttributeError(name)
        try:
            return cls._member_map_[name]  # type: ignore[return-value]
        except KeyError:
            text = '"{}" does not have an attribute of "{}"'.format(cls.__name__, name)
            raise AttributeError(text) from None

    def list_of_names(cls) -> List[str]:
        r"""Return a list of all the names within the enumerator."""
        # look for class.name: pattern, ignore class, return names only
        names = list(cls.__members__)
        return names

    def list_of_values(cls) -> List[int]:
        r"""Return a list of all the values within the enumerator."""
        values = list(cls.__members__.values())  # type: ignore[var-annotated]
        return values

    @property
    def num_values(cls) -> int:
        r"""Return the number of values within the enumerator."""
        return len(cls)

    @property
    def min_value(cls) -> int:
        r"""Return the minimum value of the enumerator."""
        return min(cls.__members__.values())

    @property
    def max_value(cls) -> int:
        r"""Return the maximum value of the enumerator."""
        return max(cls.__members__.values())


#%% Classes - IntEnumPlus
class IntEnumPlus(int, Enum, metaclass=_EnumMetaPlus):
    r"""
    Custom IntEnum class based on _EnumMetaPlus metaclass to get more details from repr/str.
    Plus it includes additional methods for convenient retrieval of number of values, their names,
    mins and maxes.
    """

    def __str__(self) -> str:
        r"""Return string representation."""
        return "{}.{}: {}".format(self.__class__.__name__, self.name, self.value)


#%% Enums - ReturnCodes
@consecutive
class ReturnCodes(IntEnumPlus):
    r"""
    Return codes for use as outputs in the command line API.

    Examples
    --------
    >>> from slog import ReturnCodes
    >>> rc = ReturnCodes.clean
    >>> print(rc)
    ReturnCodes.clean: 0

    """
    clean: ClassVar[int]            = 0  # Clean exit
    bad_command: ClassVar[int]      = 1  # Unexpected command
    bad_folder: ClassVar[int]       = 2  # Folder to execute a command in doesn't exist
    bad_help_file: ClassVar[int]    = 3  # help file doesn't exist
    bad_version: ClassVar[int]      = 4  # version information cannot be determined
    test_failures: ClassVar[int]    = 5  # A test ran to completion, but failed its criteria
    no_coverage_tool: ClassVar[int] = 6  # Coverage tool is not installed


#%% Enums - LogLevel
class LogLevel(IntEnumPlus):
    r"""
    Add 10-ish custom levels that give more degradation beween WARNING, INFO and DEBUG.
        50 (CRITICAL, FATAL)
        40 (ERROR)
    L0  35
    L1  30 (WARNING, WARN)
    L2  28
    L3  26
    L4  24
    L5  20 (INFO)
    L6  18
    L7  16
    L8  14
    L9  12
    L10 10 (DEBUG)
    L11  9
    L12  8
    L20  0  (NOTSET)

    Examples
    --------
    >>> from slog import LogLevel
    >>> print(LogLevel.L5)
    LogLevel.L5: 20

    """
    L0: ClassVar[int] = 35
    L1: ClassVar[int] = 30
    L2: ClassVar[int] = 28
    L3: ClassVar[int] = 26
    L4: ClassVar[int] = 24
    L5: ClassVar[int] = 20
    L6: ClassVar[int] = 18
    L7: ClassVar[int] = 16
    L8: ClassVar[int] = 14
    L9: ClassVar[int] = 12
    L10: ClassVar[int] = 10
    L11: ClassVar[int] = 9
    L12: ClassVar[int] = 8
    L20: ClassVar[int] = 0


#%% Register custom logging levels
logging.addLevelName(LogLevel.L0, "L0")
logging.addLevelName(LogLevel.L1, "L1")
logging.addLevelName(LogLevel.L2, "L2")
logging.addLevelName(LogLevel.L3, "L3")
logging.addLevelName(LogLevel.L4, "L4")
logging.addLevelName(LogLevel.L5, "L5")
logging.addLevelName(LogLevel.L6, "L6")
logging.addLevelName(LogLevel.L7, "L7")
logging.addLevelName(LogLevel.L8, "L8")
logging.addLevelName(LogLevel.L9, "L9")
logging.addLevelName(LogLevel.L10, "L10")
logging.addLevelName(LogLevel.L11, "L11")
logging.addLevelName(LogLevel.L12, "L12")
logging.addLevelName(LogLevel.L20, "L20")

#%% Configure default logging if not already set
logging.basicConfig(level=logging.WARNING)


#%% Unit test
if __name__ == "__main__":
    unittest.main(module="slog.tests.test_enums", exit=False)
    doctest.testmod(verbose=False)
