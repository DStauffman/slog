r"""
Test file for the `logs` module of the "slog" library.

Notes
-----
#.  Written by David C. Stauffer in July 2019.
"""

#%% Imports
import logging
import unittest

import slog as lg

try:
    import numpy as np
except ImportError:
    HAVE_NUMPY = False
else:
    HAVE_NUMPY = True


#%% activate_logging, deactivate_logging and flush_logging
class Test_act_deact_logging(unittest.TestCase):
    r"""
    Tests the activate_logging and deactivate_logging functions with the following cases:
        Nominal
        With file output
        Flushing
    """

    def setUp(self) -> None:
        self.level = lg.LogLevel.L5
        self.filename = lg.get_tests_dir() / "test_log.txt"

    def test_nominal(self) -> None:
        pass

    def test_file_output(self) -> None:
        self.assertFalse(self.filename.is_file())
        lg.activate_logging(self.level, self.filename)
        self.assertTrue(self.filename.is_file())
        self.assertTrue(lg.logs.root_logger.hasHandlers())
        with self.assertLogs(level="L5") as logs:
            logger = logging.getLogger("Test")
            logger.log(lg.LogLevel.L5, "Test message")
        lines = logs.output
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], "L5:Test:Test message")
        lg.deactivate_logging()
        self.assertFalse(lg.logs.root_logger.handlers)

    def test_flushing(self) -> None:
        lg.activate_logging(self.level)
        with self.assertLogs(level="L5") as logs:
            logger = logging.getLogger("Test")
            for i in range(10):
                logger.log(lg.LogLevel.L5, "Message {}".format(i))
            lg.flush_logging()
        lines = logs.output
        self.assertEqual(len(lines), 10)

    def tearDown(self) -> None:
        lg.deactivate_logging()
        self.filename.unlink(missing_ok=True)


#%% log_multiline
class Test_log_multiline(unittest.TestCase):
    r"""
    Tests the log_multiline function with the following cases:
        TBD
    """
    level: int
    logger: logging.Logger

    @classmethod
    def setUpClass(cls) -> None:
        cls.level = lg.LogLevel.L5
        cls.logger = logging.getLogger("Test")
        lg.activate_logging(cls.level)

    def test_normal(self) -> None:
        with self.assertLogs(logger=self.logger, level=self.level) as logs:
            lg.log_multiline(self.logger, self.level, "Normal message.")
        lines = logs.output
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], "L5:Test:Normal message.")

    def test_multiline1(self) -> None:
        with self.assertLogs(logger=self.logger, level=self.level) as logs:
            lg.log_multiline(self.logger, self.level, "Multi-line\nMessage.")
        lines = logs.output
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0], "L5:Test:Multi-line")
        self.assertEqual(lines[1], "L5:Test:Message.")

    def test_multiline2(self) -> None:
        with self.assertLogs(logger=self.logger, level=self.level) as logs:
            lg.log_multiline(self.logger, self.level, "Multi-line", "Message.")
        lines = logs.output
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0], "L5:Test:Multi-line")
        self.assertEqual(lines[1], "L5:Test:Message.")

    def test_multiline3(self) -> None:
        with self.assertLogs(logger=self.logger, level=self.level) as logs:
            lg.log_multiline(self.logger, self.level, "List value:", [1, 2, 3])
        lines = logs.output
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0], "L5:Test:List value:")
        self.assertEqual(lines[1], "L5:Test:[1, 2, 3]")

    @unittest.skipIf(not HAVE_NUMPY, "Skipping due to missing numpy dependency.")
    def test_numpy1(self) -> None:
        with self.assertLogs(logger=self.logger, level=self.level) as logs:
            lg.log_multiline(
                self.logger, self.level, np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
            )
        lines = logs.output
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0], "L5:Test:[[1 2 3]")
        self.assertEqual(lines[1], "L5:Test: [4 5 6]")
        self.assertEqual(lines[2], "L5:Test: [7 8 9]]")

    @unittest.skipIf(not HAVE_NUMPY, "Skipping due to missing numpy dependency.")
    def test_numpy2(self) -> None:
        with self.assertLogs(logger=self.logger, level=self.level) as logs:
            lg.log_multiline(
                self.logger,
                self.level,
                "Numpy solution:",
                np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
            )
        lines = logs.output
        self.assertEqual(len(lines), 4)
        self.assertEqual(lines[0], "L5:Test:Numpy solution:")
        self.assertEqual(lines[1], "L5:Test:[[1 2 3]")
        self.assertEqual(lines[2], "L5:Test: [4 5 6]")
        self.assertEqual(lines[3], "L5:Test: [7 8 9]]")

    @classmethod
    def tearDownClass(cls) -> None:
        lg.deactivate_logging()


#%% Unit test execution
if __name__ == "__main__":
    unittest.main(exit=False)
