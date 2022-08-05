r"""
The "slog" library extends the built-in Python logging module with some convenient functions and custom log levels.

"""

#%% Imports
from .cli import main, print_help, print_version
from .enums import IntEnumPlus, ReturnCodes, LogLevel
from .logs import activate_logging, deactivate_logging, flush_logging, log_multiline
from .paths import get_root_dir, get_tests_dir
from .utils import CaptureOutputResult, consecutive, is_dunder, capture_output
from .version import version_info

#%% Constants
__version__ = ".".join(str(x) for x in version_info)

#%% Unit test
if __name__ == "__main__":
    pass
