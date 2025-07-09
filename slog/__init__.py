r"""
The "slog" library extends the built-in Python logging module with some convenient functions and custom log levels.

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

Also adds generic read/write, and mkdir commands, along with string manipulation, enum, and logging support.

"""

# %% Imports
from .cli import main as main, print_help as print_help, print_version as print_version
from .enums import IntEnumPlus as IntEnumPlus, ReturnCodes as ReturnCodes, LogLevel as LogLevel
from .files import (
    read_text_file as read_text_file,
    write_text_file as write_text_file,
    make_dir as make_dir,
    wipe_dir as wipe_dir,
)
from .logs import (
    activate_logging as activate_logging,
    deactivate_logging as deactivate_logging,
    flush_logging as flush_logging,
    log_multiline as log_multiline,
)
from .paths import get_root_dir as get_root_dir, get_tests_dir as get_tests_dir
from .utils import (
    CaptureOutputResult as CaptureOutputResult,
    consecutive as consecutive,
    is_dunder as is_dunder,
    line_wrap as line_wrap,
    list_python_files as list_python_files,
    capture_output as capture_output,
)
from .version import version_info as version_info

# %% Constants
__version__ = ".".join(str(x) for x in version_info)

# %% Unit test
if __name__ == "__main__":
    pass
