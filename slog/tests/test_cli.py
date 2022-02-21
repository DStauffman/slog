r"""
Test file for the `cli` module of the "slog" library.

Notes
-----
#.  Written by David C. Stauffer in March 2020.
#.  Adapted to slog library by David C. Stauffer in February 2022.
"""

#%% Imports
import unittest

import slog as lg


#%% main
class Test_main(unittest.TestCase):
    r"""
    Tests the main function with the following cases:
        TBD
    """

    pass  # TODO: write this


#%% print_help
class Test_print_help(unittest.TestCase):
    r"""
    Tests the print_help function with the following cases:
        Nominal
        Specified file
    """

    def test_nominal(self) -> None:
        with lg.capture_output() as out:
            lg.print_help()
        output = out.getvalue().strip()
        out.close()
        self.assertTrue(output.startswith('####\nslog\n####\n'))

    def test_specify_file(self) -> None:
        help_file = lg.get_tests_dir() / 'test_cli.py'
        with lg.capture_output() as out:
            lg.print_help(help_file)
        output = out.getvalue().strip()
        out.close()
        self.assertTrue(output.startswith('r"""\nTest file for the `cli` module'))


#%% print_version
class Test_print_version(unittest.TestCase):
    r"""
    Tests the print_version function with the following cases:
        Nominal
    """

    def test_nominal(self) -> None:
        with lg.capture_output() as out:
            lg.print_version()
        output = out.getvalue().strip()
        out.close()
        self.assertIn('.', output)


#%% Unit test execution
if __name__ == '__main__':
    unittest.main(exit=False)
