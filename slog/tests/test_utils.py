r"""
Test file for the `utils` module of the "slog" library.

Notes
-----
#.  Written by David C. Stauffer in March 2015.
#.  Adapted to slog library by David C. Stauffer in February 2022.

"""

# %% Imports
from collections.abc import Iterable, Iterator
import contextlib
import inspect
from io import StringIO
import os
import pathlib
import sys
from types import TracebackType
from typing import AnyStr, TextIO
import unittest

import slog as lg


class _Example_Consecutive(lg.IntEnumPlus):
    zero = 0
    one = 1
    two = 2


class _Example_Consecutive2(lg.IntEnumPlus):
    zero = 0
    one = 1
    skip = 9


class _Example_Consecutive3(lg.IntEnumPlus):
    zero = 0
    one = 1
    dup = 0


class _ExampleTextIOClass(TextIO):
    def __init__(self) -> None:
        self._text: list[str] = []

    def write(self, text: AnyStr) -> int:
        self._text.append(text)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
        return 0

    def close(self) -> None:
        self._text = []

    def readlines(self, hint: int = 0) -> list[str]:
        return self._text[hint:]

    def __enter__(self) -> TextIO:  # type: ignore[empty-body]  # ty: ignore[empty-body]
        pass

    def fileno(self) -> int:  # type: ignore[empty-body]  # ty: ignore[empty-body]
        pass

    def flush(self) -> None:
        pass

    def isatty(self) -> bool:  # type: ignore[empty-body]  # ty: ignore[empty-body]
        pass

    def read(self, n: int = ...) -> AnyStr:  # type: ignore[empty-body, type-var]  # ty: ignore[empty-body, invalid-parameter-default]
        pass

    def readable(self) -> bool:  # type: ignore[empty-body]  # ty: ignore[empty-body]
        pass

    def readline(self, limit: int = ...) -> AnyStr:  # type: ignore[empty-body, type-var]  # ty: ignore[empty-body, invalid-parameter-default]
        pass

    def seek(self, offset: int, whence: int = ...) -> int:  # type: ignore[empty-body]  # ty: ignore[empty-body, invalid-parameter-default]
        pass

    def seekable(self) -> bool:  # type: ignore[empty-body]  # ty: ignore[empty-body]
        pass

    def tell(self) -> int:  # type: ignore[empty-body]  # ty: ignore[empty-body]
        pass

    def truncate(self, size: int | None = ...) -> int:  # type: ignore[empty-body]  # ty: ignore[empty-body, invalid-parameter-default]
        pass

    def writable(self) -> bool:  # type: ignore[empty-body]  # ty: ignore[empty-body]
        pass

    def writelines(self, lines: Iterable[AnyStr]) -> None:
        pass

    def __next__(self) -> AnyStr:  # type: ignore[empty-body, type-var]  # ty: ignore[empty-body]
        pass

    def __iter__(self) -> Iterator[AnyStr]:  # type: ignore[empty-body]  # ty: ignore[empty-body]
        pass

    def __exit__(  # type: ignore[override]  # ty: ignore[invalid-method-override]
        self, t: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None
    ) -> bool | None:
        pass


# %% CaptureOutputResult
class Test_CaptureOutputResult(unittest.TestCase):
    r"""
    Tests the CaptureOutputResult class with the following cases:
        TBD
    """

    def test_close(self) -> None:
        out = StringIO()
        err = StringIO()
        ctx = lg.CaptureOutputResult(out, err)
        out.write("Works")
        err.write("Also works")
        ctx.close()
        with contextlib.suppress(ValueError):
            out.write("Fails")
        with contextlib.suppress(ValueError):
            err.write("Also fails")

    def test_get_output(self) -> None:
        out = StringIO()
        ctx = lg.CaptureOutputResult(out)
        exp = "Hello, World!"
        print(exp, file=out)
        output = ctx.get_output()
        error = ctx.get_error()
        self.assertEqual(output, exp)
        self.assertEqual(error, "")

    def test_get_error(self) -> None:
        err = StringIO()
        ctx = lg.CaptureOutputResult(stderr=err)
        exp = "Hello, World!"
        print(exp, file=err)
        output = ctx.get_output()
        error = ctx.get_error()
        self.assertEqual(output, "")
        self.assertEqual(error, exp)

    def test_get_stream(self) -> None:
        stream = _ExampleTextIOClass()
        stream.write("Testing")
        stream.write("More testing.")
        text = lg.CaptureOutputResult.get_stream(stream)
        self.assertEqual(text, "Testing\nMore testing.")


# %% consecutive
class Test_consecutive(unittest.TestCase):
    r"""
    Tests the consecutive function with the following cases:
        Nominal consecutive enum
        Unique, but not consecutive
        Not unique
    """

    def setUp(self) -> None:
        self.enum = lg.IntEnumPlus("Enum1", "one two three")  # type: ignore[call-overload]

    def test_consecutive(self) -> None:
        enum = lg.consecutive(_Example_Consecutive)
        self.assertTrue(isinstance(enum, lg.enums._EnumMetaPlus))  # noqa: SLF001

    def test_consecutive_but_not_zero(self) -> None:
        with self.assertRaises(ValueError) as context:
            lg.consecutive(self.enum)  # ty: ignore[invalid-argument-type]
        self.assertEqual(str(context.exception), "Bad starting value (should be zero): 1")

    def test_unique_but_non_consecutive(self) -> None:
        with self.assertRaises(ValueError) as context:
            lg.consecutive(_Example_Consecutive2)
        self.assertEqual(str(context.exception), "Non-consecutive values found in _Example_Consecutive2: skip: 9")

    def test_not_unique(self) -> None:
        with self.assertRaises(ValueError) as context:
            lg.consecutive(_Example_Consecutive3)
        self.assertEqual(str(context.exception), "Duplicate values found in _Example_Consecutive3: dup -> zero")


# %% is_dunder
class Test_is_dunder(unittest.TestCase):
    r"""
    Tests the is_dunder function with the following cases:
        True
        False
    """

    def setUp(self) -> None:
        self.true = ["__dunder__", "__init__", "__a__"]
        self.false = ["init", "__init__.py", "_private", "__private", "private__", "____"]

    def test_trues(self) -> None:
        for key in self.true:
            self.assertTrue(lg.is_dunder(key), key + " Should be a __dunder__ method")

    def test_falses(self) -> None:
        for key in self.false:
            self.assertFalse(lg.is_dunder(key), key + " Should not be considered dunder.")


# %% line_wrap
class Test_line_wrap(unittest.TestCase):
    r"""
    Tests the line_wrap function with the following cases:
        TBD
    """

    def setUp(self) -> None:
        self.text = ("lots of repeated words " * 4).strip()
        self.wrap = 40
        self.min_wrap = 0
        self.indent = 4
        self.out = [
            "lots of repeated words lots of \\",
            "    repeated words lots of repeated \\",
            "    words lots of repeated words",
        ]

    def test_str(self) -> None:
        out = lg.line_wrap(self.text, self.wrap, self.min_wrap, self.indent)
        self.assertEqual(out, "\n".join(self.out))

    def test_list(self) -> None:
        out = lg.line_wrap([self.text], self.wrap, self.min_wrap, self.indent)
        self.assertEqual(out, self.out)

    def test_list2(self) -> None:
        out = lg.line_wrap(3 * ["aaaaaaaaaa bbbbbbbbbb cccccccccc"], wrap=25, min_wrap=15, indent=2)
        self.assertEqual(out, 3 * ["aaaaaaaaaa bbbbbbbbbb \\", "  cccccccccc"])

    def test_min_wrap(self) -> None:
        out = lg.line_wrap("aaaaaaaaaaaaaaaaaaaa bbbbbbbbbb", 25, 18, 0)
        self.assertEqual(out, "aaaaaaaaaaaaaaaaaaaa \\\nbbbbbbbbbb")

    def test_min_wrap2(self) -> None:
        with self.assertRaises(ValueError) as context:
            lg.line_wrap("aaaaaaaaaaaaaaaaaaaa bbbbbbbbbb", 25, 22, 0)
        self.assertEqual(str(context.exception), 'The specified min_wrap:wrap of "22:25" was too small.')


# %% list_python_files
class Test_list_python_files(unittest.TestCase):
    r"""
    Tests the list_python_files function with the following cases:
        TBD
    """

    def setUp(self) -> None:
        self.folder = lg.get_root_dir()
        self.expected = tuple(
            self.folder / x for x in ("cli.py", "enums.py", "files.py", "logs.py", "paths.py", "utils.py", "version.py")
        )

    def test_nominal(self) -> None:
        files = lg.list_python_files(self.folder)
        for file, exp in zip(sorted(files), self.expected, strict=True):
            self.assertEqual(file, exp)


# %% get_root_dir
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


# %% capture_output
class Test_capture_output(unittest.TestCase):
    r"""
    Tests the capture_output function with the following cases:
        capture standard output
        capture standard error
    """

    def test_std_out(self) -> None:
        with lg.capture_output() as ctx:
            print("Hello, World!")
        output = ctx.get_output()
        ctx.close()
        self.assertEqual(output, "Hello, World!")

    def test_std_err(self) -> None:
        with lg.capture_output("err") as ctx:
            print("Error Raised.", file=sys.stderr)
        error = ctx.get_error()
        ctx.close()
        self.assertEqual(error, "Error Raised.")

    def test_all(self) -> None:
        with lg.capture_output("all") as ctx:
            print("Hello, World!")
            print("Error Raised.", file=sys.stderr)
        output = ctx.get_output()
        error = ctx.get_error()
        ctx.close()
        self.assertEqual(output, "Hello, World!")
        self.assertEqual(error, "Error Raised.")

    def test_bad_value(self) -> None:
        with self.assertRaises(RuntimeError), lg.capture_output("bad"):
            print("Lost values")  # pragma: no cover


# %% Unit test execution
if __name__ == "__main__":
    unittest.main(exit=False)
