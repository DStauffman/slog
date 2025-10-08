r"""
Test file for the `files` module of the "slog" library.

Notes
-----
#.  Written by David C. Stauffer in March 2015.
#.  Adapted to slog library by David C. Stauffer in June 2025.

"""

# %% Imports
import contextlib
import pathlib
import platform
import time
import unittest
from unittest.mock import Mock, patch

import slog as lg


# %% read_text_file
class Test_read_text_file(unittest.TestCase):
    r"""
    Tests the read_text_file function with the following cases:
        read a file that exists
        read a file that does not exist (raise error)
    """

    folder: pathlib.Path
    contents: str
    filepath: pathlib.Path
    badpath: pathlib.Path

    @classmethod
    def setUpClass(cls) -> None:
        cls.folder = lg.get_tests_dir()
        cls.contents = "Hello, World!\n"
        cls.filepath = cls.folder / "temp_file.txt"
        cls.badpath = pathlib.Path(r"AA:\non_existent_path\bad_file.txt")
        with cls.filepath.open("wt") as file:
            file.write(cls.contents)

    def test_reading(self) -> None:
        text = lg.read_text_file(self.filepath)
        self.assertEqual(text, self.contents)

    def test_string(self) -> None:
        text = lg.read_text_file(str(self.filepath))
        self.assertEqual(text, self.contents)

    def test_bad_reading(self) -> None:
        with patch("slog.files.logger") as mock_logger, self.assertRaises((OSError, IOError, FileNotFoundError)):
            lg.read_text_file(self.badpath)
        mock_logger.log.assert_called_with(
            lg.LogLevel.L2, r'Unable to open file "%s" for reading.', pathlib.Path(r"AA:\non_existent_path\bad_file.txt")
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.filepath.unlink(missing_ok=True)


# %% write_text_file
class Test_write_text_file(unittest.TestCase):
    r"""
    Tests the write_text_file function with the following cases:
        write a file
        write a bad file location (raise error)
    """

    folder: pathlib.Path
    contents: str
    filepath: pathlib.Path
    badpath: pathlib.Path

    @classmethod
    def setUpClass(cls) -> None:
        cls.folder = lg.get_tests_dir()
        cls.contents = "Hello, World!\n"
        cls.filepath = cls.folder / "temp_file.txt"
        cls.badpath = pathlib.Path(r"AA:\non_existent_path\bad_file.txt")

    def test_writing(self) -> None:
        lg.write_text_file(self.filepath, self.contents)
        with self.filepath.open("rt") as file:
            text = file.read()
        self.assertEqual(text, self.contents)

    def test_str(self) -> None:
        lg.write_text_file(str(self.filepath), self.contents)
        with self.filepath.open("rt") as file:
            text = file.read()
        self.assertEqual(text, self.contents)

    def test_bad_writing(self) -> None:
        if platform.system() != "Windows":
            return  # pragma: noc windows
        with patch("slog.files.logger") as mock_logger, self.assertRaises((OSError, IOError, FileNotFoundError)):
            lg.write_text_file(self.badpath, self.contents)
        mock_logger.log.assert_called_with(
            lg.LogLevel.L2, r'Unable to open file "%s" for writing.', pathlib.Path(r"AA:\non_existent_path\bad_file.txt")
        )

    def test_append_file(self) -> None:
        lg.write_text_file(self.filepath, self.contents)
        with self.filepath.open("rt") as file:
            text = file.read()
        self.assertEqual(text, self.contents)
        lg.write_text_file(self.filepath, "New Contents\n")
        with self.filepath.open("rt") as file:
            text = file.read()
        self.assertEqual(text, "New Contents\n")
        lg.write_text_file(self.filepath, "Additional Notes.\n\n", append=True)
        with self.filepath.open("rt") as file:
            text = file.read()
        self.assertEqual(text, "New Contents\nAdditional Notes.\n\n")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.filepath.unlink(missing_ok=True)


# %% make_dir
@patch("slog.files.logger")
class Test_make_dir(unittest.TestCase):
    r"""
    Tests the make_dir function with the following cases:
        null case
        create a new folder
        create a new nested folder
        fail to create a folder due to permissions
        fail to create a folder due to a bad name
    """

    def setUp(self) -> None:
        self.folder = lg.get_tests_dir() / "temp_dir"
        self.subdir = lg.get_tests_dir().joinpath("temp_dir", "temp_dir2")
        self.filename = self.folder / "temp_file.txt"
        self.subfile = self.subdir / "temp_file.txt"
        self.text = "Hello, World!\n"

    def test_empty_string(self, mock_logger: Mock) -> None:
        lg.make_dir("")
        mock_logger.log.assert_not_called()

    def test_create_folder(self, mock_logger: Mock) -> None:
        lg.make_dir(self.folder)
        mock_logger.log.assert_called_once()
        mock_logger.log.assert_called_with(lg.LogLevel.L1, 'Created directory: "%s"', self.folder)

    def test_nested_folder(self, mock_logger: Mock) -> None:
        lg.make_dir(self.subdir)
        mock_logger.log.assert_called_once()
        mock_logger.log.assert_called_with(lg.LogLevel.L1, 'Created directory: "%s"', self.subdir)

    def test_fail_to_create_folder(self, mock_logger: Mock) -> None:
        pass  # TODO: write this test

    def test_bad_name_file_ext(self, mock_logger: Mock) -> None:
        pass  # TODO: write this test

    def tearDown(self) -> None:
        def _clean(self: Test_make_dir) -> None:
            self.filename.unlink(missing_ok=True)
            self.subfile.unlink(missing_ok=True)
            with contextlib.suppress(FileNotFoundError):
                self.subdir.rmdir()
            with contextlib.suppress(FileNotFoundError):
                self.folder.rmdir()

        try:
            _clean(self)
        except (PermissionError, OSError):  # pragma: no cover
            # pause to let Windows catch up and close files
            time.sleep(1)
            # retry
            _clean(self)


# %% wipe_dir
@patch("slog.files.logger")
class Test_wipe_dir(unittest.TestCase):
    r"""
    Tests the wipe_dir function with the following cases:
        null case
        create a new folder
        create a new nested folder
        delete the contents of an existing folder
        fail to create a folder due to permissions
        fail to delete the contents of an existing folder due to permissions
        fail to create a folder due to a bad name
        delete the contents of an existing folder recursively
    """

    def setUp(self) -> None:
        self.folder = lg.get_tests_dir() / "temp_dir"
        self.subdir = lg.get_tests_dir().joinpath("temp_dir", "temp_dir2")
        self.filename = self.folder / "temp_file.txt"
        self.subfile = self.subdir / "temp_file.txt"
        self.text = "Hello, World!\n"

    def test_empty_string(self, mock_logger: Mock) -> None:
        lg.wipe_dir("")
        mock_logger.log.assert_not_called()

    def test_create_folder(self, mock_logger: Mock) -> None:
        lg.wipe_dir(self.folder)
        mock_logger.log.assert_called_once()
        mock_logger.log.assert_called_with(lg.LogLevel.L1, 'Created directory: "%s"', self.folder)

    def test_nested_folder(self, mock_logger: Mock) -> None:
        lg.wipe_dir(self.subdir)
        mock_logger.log.assert_called_once()
        mock_logger.log.assert_called_with(lg.LogLevel.L1, 'Created directory: "%s"', self.subdir)

    def test_clean_up_folder(self, mock_logger: Mock) -> None:
        lg.wipe_dir(self.folder)
        lg.write_text_file(self.filename, self.text)
        with patch("slog.files.logger") as mock_logger2:
            lg.wipe_dir(self.folder)
            mock_logger2.log.assert_called_once()
            mock_logger2.log.assert_called_with(lg.LogLevel.L1, 'Files/Sub-folders were removed from: "%s"', self.folder)
        mock_logger.log.assert_called_once()

    def test_clean_up_partial(self, mock_logger: Mock) -> None:
        lg.wipe_dir(self.folder)
        lg.write_text_file(self.filename, "")
        lg.wipe_dir(self.subdir)
        lg.write_text_file(self.subfile, "")
        with patch("slog.files.logger") as mock_logger2:
            lg.wipe_dir(self.folder, recursive=False)
            mock_logger2.log.assert_called_once()
            mock_logger2.log.assert_called_with(lg.LogLevel.L1, 'Files/Sub-folders were removed from: "%s"', self.folder)
        self.assertEqual(mock_logger.log.call_count, 2)

    def test_fail_to_create_folder(self, mock_logger: Mock) -> None:
        pass  # TODO: write this test

    def test_fail_to_clean_folder(self, mock_logger: Mock) -> None:
        pass  # TODO: write this test

    def test_bad_name_file_ext(self, mock_logger: Mock) -> None:
        pass  # TODO: write this test

    def test_clean_up_recursively(self, mock_logger: Mock) -> None:  # noqa: ARG002
        lg.wipe_dir(self.subdir)
        lg.write_text_file(self.subfile, self.text)
        with patch("slog.files.logger") as mock_logger2:
            lg.wipe_dir(self.folder, recursive=True)
            self.assertEqual(mock_logger2.log.call_count, 2)
            mock_logger2.log.assert_any_call(lg.LogLevel.L1, 'Files/Sub-folders were removed from: "%s"', self.subdir)
            mock_logger2.log.assert_any_call(lg.LogLevel.L1, 'Files/Sub-folders were removed from: "%s"', self.subdir)

    def tearDown(self) -> None:
        def _clean(self: Test_wipe_dir) -> None:
            self.filename.unlink(missing_ok=True)
            self.subfile.unlink(missing_ok=True)
            with contextlib.suppress(FileNotFoundError):
                self.subdir.rmdir()
            with contextlib.suppress(FileNotFoundError):
                self.folder.rmdir()

        try:
            _clean(self)
        except (PermissionError, OSError):  # pragma: no cover
            # pause to let Windows catch up and close files
            time.sleep(1)
            # retry
            _clean(self)


# %% Unit test execution
if __name__ == "__main__":
    unittest.main(exit=False)
