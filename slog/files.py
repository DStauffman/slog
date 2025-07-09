r"""
File and folder reading and writing utilities.

Notes
-----
#.  Written by David C. Stauffer in March 2015.
#.  Moved to the slog library in June 2025 to simplify dependencies for only core python.

"""

# %% Imports
import contextlib
import doctest
import logging
from pathlib import Path
import unittest

from slog.enums import LogLevel

# %% Globals
logger = logging.getLogger(__name__)


# %% Functions - read_text_file
def read_text_file(filename: str | Path, encoding: str = "utf-8") -> str:
    r"""
    Open and read a complete text file.

    Parameters
    ----------
    filename : str or class pathlib.Path
        fullpath name of the file to read
    encoding : str, optional, default is "utf-8"
        Encoding used to write file

    Returns
    -------
    text : str
        text of the desired file

    Raises
    ------
    RuntimeError
        If unable to open, or unable to read file.

    See Also
    --------
    write_text_file, open

    Examples
    --------
    >>> from slog import read_text_file, write_text_file, get_tests_dir
    >>> import os
    >>> text = "Hello, World\n"
    >>> filename = get_tests_dir() / "temp_file.txt"
    >>> write_text_file(filename, text)
    >>> text2 = read_text_file(get_tests_dir() / "temp_file.txt")
    >>> print(text2)
    Hello, World
    <BLANKLINE>

    >>> filename.unlink()

    """
    try:
        # open file for reading
        with open(filename, "rt", encoding=encoding) as file:
            # read file
            text = file.read()
        # return results
        return text
    except Exception:
        # on any exceptions, print a message and re-raise the error
        logger.log(LogLevel.L2, 'Unable to open file "%s" for reading.', filename)
        raise


# %% Functions - write_text_file
def write_text_file(filename: str | Path, text: str, encoding: str = "utf-8", *, append: bool = False) -> None:
    r"""
    Open and write the specified text to a file.

    Parameters
    ----------
    filename : str
        fullpath name of the file to read
    text : str
        text to be written to the file
    encoding : str, optional, default is "utf-8"
        Encoding used to write file
    append : bool, optional, default is False
        Whether to append to an existing file

    Raises
    ------
    RuntimeError
        If unable to open, or unable to write file.

    See Also
    --------
    open_text_file, open

    Examples
    --------
    >>> from slog import write_text_file, get_tests_dir
    >>> import os
    >>> text = "Hello, World\n"
    >>> filename = get_tests_dir() / "temp_file.txt"
    >>> write_text_file(filename, text)

    >>> filename.unlink()

    """
    mode = "at" if append else "wt"
    try:
        # open file for writing
        with open(filename, mode, encoding=encoding) as file:
            # write file
            file.write(text)
    except Exception:
        # on any exceptions, print a message and re-raise the error
        logger.log(LogLevel.L2, 'Unable to open file "%s" for writing.', filename)
        raise


# %% Functions - make_dir
def make_dir(folder: str | Path) -> None:
    r"""
    Instantiates the directory if it doesn't exist.

    Parameters
    ----------
    folder : str
        Location of the folder to instantiate.

    See Also
    --------
    wipe_dir, os.makedirs, os.rmdir, os.remove, pathlib.Path.mkdir, pathlib.Path.rmdir

    Raises
    ------
    RuntimeError
        Problems creating or deleting a file or folder, likely due to permission issues.

    Notes
    -----
    #.  Written by David C. Stauffer in Feb 2015.
    #.  Split off to just make_dir version by David C. Stauffer in June 2025.

    Examples
    --------
    >>> from slog import make_dir
    >>> make_dir(r"C:\Temp\test_folder")  # doctest: +SKIP

    """
    # convert older string API to paths
    if isinstance(folder, str):
        # check for an empty string and exit
        if not folder:
            return
        folder = Path(folder)
    if folder.is_dir():
        return
    # create directory if it does not exist
    try:
        folder.mkdir(parents=True)
        logger.log(LogLevel.L1, 'Created directory: "%s"', folder)
    except Exception:  # pragma: no cover  # pylint: disable=try-except-raise
        # re-raise last exception, could try to handle differently in the future
        raise  # pragma: no cover


# %% Functions - wipe_dir
def wipe_dir(folder: str | Path, recursive: bool = False) -> None:
    r"""
    Clear the contents for existing folders or instantiates the directory if it doesn't exist.

    Parameters
    ----------
    folder : str
        Location of the folder to empty or instantiate.
    recursive : bool, optional
        Whether to recursively delete contents.

    See Also
    --------
    make_dir, os.makedirs, os.rmdir, os.remove, pathlib.Path.mkdir, pathlib.Path.rmdir

    Raises
    ------
    RuntimeError
        Problems creating or deleting a file or folder, likely due to permission issues.

    Notes
    -----
    #.  Written by David C. Stauffer in Feb 2015.
    #.  Moved to slog and made into wipe_dir by David C. Stauffer in June 2025.

    Examples
    --------
    >>> from slog import wipe_dir
    >>> wipe_dir(r"C:\Temp\test_folder")  # doctest: +SKIP

    """
    # convert older string API to paths
    if isinstance(folder, str):
        # check for an empty string and exit
        if not folder:
            return
        folder = Path(folder)
    if not folder.is_dir():
        make_dir(folder)
        return
    # Loop through the contained files/folders
    for this_elem in folder.glob("*"):
        # alias the fullpath of this file element
        this_full_elem = this_elem.resolve()
        # check if a folder or file
        if this_full_elem.is_dir():
            # if a folder, then delete recursively if recursive is True
            if recursive:
                wipe_dir(this_full_elem, recursive=recursive)
                with contextlib.suppress(FileNotFoundError):
                    this_full_elem.rmdir()
        elif this_full_elem.is_file():
            # if a file, then remove it
            this_full_elem.unlink(missing_ok=True)
        else:
            raise RuntimeError(f'Unexpected file type, neither file nor folder: "{this_full_elem}".')  # pragma: no cover
    logger.log(LogLevel.L1, 'Files/Sub-folders were removed from: "%s"', folder)


# %% Unit test
if __name__ == "__main__":
    unittest.main(module="slog.tests.test_files", exit=False)
    doctest.testmod(verbose=False)
