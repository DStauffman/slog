r"""
Test file for the `cli` module of the "slog" library.

Notes
-----
#.  Written by David C. Stauffer in March 2020.
#.  Adapted to slog library by David C. Stauffer in February 2022.

"""

# %% Imports
import contextlib
import io
import unittest
from unittest.mock import patch

import slog as lg


# %% main
class Test_main(unittest.TestCase):
    r"""
    Tests the main function with the following cases:
        Help (good and bad)
        Version (good and bad)
        Doctests (pass and fail)
        Unit Tests (pass and fail)
    """

    def test_help(self) -> None:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer), patch("sys.argv", ["name.py", "help"]), self.assertRaises(SystemExit) as exc:
            lg.main()
        output = buffer.getvalue()
        buffer.close()
        self.assertEqual(exc.exception.code, 0)
        self.assertTrue(output.startswith("####\nslog\n####\n"))

    def test_bad_help(self) -> None:
        with (
            patch("slog.cli.print_help", return_value=lg.ReturnCodes.bad_help_file),
            patch("sys.argv", ["name.py", "--help"]),
            self.assertRaises(SystemExit) as exc,
        ):
            lg.main()
        self.assertEqual(exc.exception.code, 3)

    def test_version(self) -> None:
        buffer = io.StringIO()
        with (
            contextlib.redirect_stdout(buffer),
            patch("sys.argv", ["name.py", "version"]),
            self.assertRaises(SystemExit) as exc,
        ):
            lg.main()
        output = buffer.getvalue()
        buffer.close()
        self.assertEqual(exc.exception.code, 0)
        self.assertIn(".", output)

    def test_bad_version(self) -> None:
        with (
            patch("slog.cli.print_version", return_value=lg.ReturnCodes.bad_version),
            patch("sys.argv", ["name.py", "--version"]),
            self.assertRaises(SystemExit) as exc,
        ):
            lg.main()
        self.assertEqual(exc.exception.code, 4)

    def test_doctests(self) -> None:
        with (
            patch("slog.cli.doctest.testfile", return_value=(0, "")) as mock_tester,
            patch("sys.argv", ["name.py", "doctests", "-v"]),
            self.assertRaises(SystemExit) as exc,
        ):
            lg.main()
        self.assertEqual(exc.exception.code, 0)
        mock_tester.assert_any_call(str(lg.get_root_dir().joinpath("cli.py")), report=True, verbose=True, module_relative=False)  # fmt: skip

    def test_doctest_fails(self) -> None:
        with (
            patch("slog.cli.doctest.testfile", return_value=(1, "")) as mock_tester,
            patch("sys.argv", ["name.py", "doctests"]),
            self.assertRaises(SystemExit) as exc,
        ):
            lg.main()
        self.assertEqual(exc.exception.code, 5)
        mock_tester.assert_any_call(str(lg.get_root_dir().joinpath("cli.py")), report=True, verbose=False, module_relative=False)  # fmt: skip

    def test_unittests(self) -> None:
        with (
            patch("pytest.main", return_value=0) as mock_tester,
            patch("sys.argv", ["name.py", "tests"]),
            self.assertRaises(SystemExit) as exc,
        ):
            lg.main()
        self.assertEqual(exc.exception.code, 0)
        mock_tester.assert_called_with([str(lg.get_root_dir().joinpath("tests")), "-rfEsP"])

    def test_bad_unittests(self) -> None:
        with (
            patch("pytest.main", return_value=-1) as mock_tester,
            patch("sys.argv", ["name.py", "tests", "--extra"]),
            self.assertRaises(SystemExit) as exc,
        ):
            lg.main()
        self.assertEqual(exc.exception.code, 5)
        mock_tester.assert_called_with([str(lg.get_root_dir().joinpath("tests")), "-rfEsP", "--extra"])


# %% print_help
class Test_print_help(unittest.TestCase):
    r"""
    Tests the print_help function with the following cases:
        Nominal
        Specified file
    """

    def test_nominal(self) -> None:
        with lg.capture_output() as ctx:
            lg.print_help()
        output = ctx.get_output()
        ctx.close()
        self.assertTrue(output.startswith("####\nslog\n####\n"))

    def test_specify_file(self) -> None:
        help_file = lg.get_tests_dir() / "test_cli.py"
        with lg.capture_output() as ctx:
            lg.print_help(help_file)
        output = ctx.get_output()
        ctx.close()
        self.assertTrue(output.startswith('r"""\nTest file for the `cli` module'))


# %% print_version
class Test_print_version(unittest.TestCase):
    r"""
    Tests the print_version function with the following cases:
        Nominal
    """

    def test_nominal(self) -> None:
        with lg.capture_output() as ctx:
            lg.print_version()
        output = ctx.get_output()
        ctx.close()
        self.assertIn(".", output)


# %% Unit test execution
if __name__ == "__main__":
    unittest.main(exit=False)
