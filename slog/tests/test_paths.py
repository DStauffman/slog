r"""
Test file for the `paths` module of the "slog" library.

Notes
-----
#.  Written by David C. Stauffer in February 2019.
#.  Adapted by David C. Stauffer in February 2022 for slog library.
"""

#%% Imports
import inspect
import os
import pathlib
import unittest

import slog as lg


#%% get_root_dir
class Test_get_root_dir(unittest.TestCase):
    r"""
    Tests the get_root_dir function with the following cases:
        call the function
    """

    def test_function(self) -> None:
        filepath = inspect.getfile(lg.get_root_dir.__wrapped__)
        expected_root = pathlib.Path(os.path.split(filepath)[0])
        folder = lg.get_root_dir()
        self.assertEqual(folder, expected_root)
        self.assertTrue(folder.is_dir())


#%% get_tests_dir
class Test_get_tests_dir(unittest.TestCase):
    r"""
    Tests the get_tests_dir function with the following cases:
        call the function
    """

    def test_function(self) -> None:
        folder = lg.get_tests_dir()
        self.assertEqual(str(folder), os.path.join(str(lg.get_root_dir()), 'tests'))


#%% Unit test execution
if __name__ == '__main__':
    unittest.main(exit=False)
