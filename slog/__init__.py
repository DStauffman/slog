r"""
The "slog" library extends the built-in Python logging module with some convenient functions and custom log levels.

"""

# %% Imports
from .cli import main as main, print_help as print_help, print_version as print_version
from .enums import IntEnumPlus as IntEnumPlus, ReturnCodes as ReturnCodes, LogLevel as LogLevel
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
    capture_output as capture_output,
)
from .version import version_info as version_info

# %% Constants
__version__ = ".".join(str(x) for x in version_info)

# %% Unit test
if __name__ == "__main__":
    pass
