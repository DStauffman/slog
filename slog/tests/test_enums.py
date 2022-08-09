r"""
Test file for the `enums` module of the "slog" library.

Notes
-----
#.  Written by David C. Stauffer in July 2015.
"""

#%% Imports
from enum import unique
from typing import ClassVar
import unittest

import slog as lg


#%% Support
class _Example_Enum(lg.IntEnumPlus):
    field_one: ClassVar[int] = 1
    field_two: ClassVar[int] = 2
    field_ten: ClassVar[int] = 10


#%% IntEnumPlus
class Test_IntEnumPlus(unittest.TestCase):
    r"""
    Tests the IntEnumPlus class by making a enum instance and testing all the methods.
    """

    def test_printing_instance_str(self) -> None:
        with lg.capture_output() as ctx:
            print(_Example_Enum.field_one)
            print(_Example_Enum.field_two)
        output = ctx.get_output()
        ctx.close()
        self.assertEqual(output, "_Example_Enum.field_one: 1\n_Example_Enum.field_two: 2")

    def test_printing_instance_repr(self) -> None:
        with lg.capture_output() as ctx:
            print(repr(_Example_Enum.field_one))
            print(repr(_Example_Enum.field_two))
        output = ctx.get_output()
        ctx.close()
        self.assertEqual(output, "<_Example_Enum.field_one: 1>\n<_Example_Enum.field_two: 2>")

    def test_printing_class_str(self) -> None:
        with lg.capture_output() as ctx:
            print(_Example_Enum)
        output = ctx.get_output()
        ctx.close()
        self.assertEqual(
            output,
            "_Example_Enum.field_one: 1\n_Example_Enum.field_two: 2\n_Example_Enum.field_ten: 10",
        )

    def test_printing_class_repr(self) -> None:
        with lg.capture_output() as ctx:
            print(repr(_Example_Enum))
        output = ctx.get_output()
        ctx.close()
        self.assertEqual(
            output,
            "<_Example_Enum.field_one: 1>\n<_Example_Enum.field_two: 2>\n<_Example_Enum.field_ten: 10>",
        )

    def test_list_of_names(self) -> None:
        list_of_names = _Example_Enum.list_of_names()
        self.assertEqual(list_of_names, ["field_one", "field_two", "field_ten"])

    def test_list_of_values(self) -> None:
        list_of_values = _Example_Enum.list_of_values()
        self.assertEqual(list_of_values, [1, 2, 10])

    def test_num_values(self) -> None:
        num_values = _Example_Enum.num_values
        self.assertEqual(num_values, 3)

    def test_min_value(self) -> None:
        min_value = _Example_Enum.min_value
        self.assertEqual(min_value, 1)

    def test_max_value(self) -> None:
        max_value = _Example_Enum.max_value
        self.assertEqual(max_value, 10)

    def test_bad_attribute(self) -> None:
        with self.assertRaises(AttributeError):
            _Example_Enum.non_existant_field

    def test_bad_uniqueness(self) -> None:
        with self.assertRaises(ValueError):

            @unique
            class _BadUnique(lg.IntEnumPlus):
                a = 1
                b = 2
                c = 2


#%% ReturnCodes
class Test_ReturnCodes(unittest.TestCase):
    r"""
    Tests the ReturnCodes enumerator with the following cases:
        Clean code
        Not clean codes
    """

    def test_clean(self) -> None:
        # A clean exit should return zero
        self.assertEqual(lg.ReturnCodes.clean, 0)

    def test_not_clean(self) -> None:
        # All non-clean exists should return an integer greater than 0
        rc = lg.ReturnCodes
        for key in rc.__members__:
            if key == "clean":
                continue
            value = getattr(rc, key)
            self.assertGreater(value, 0)
            self.assertIsInstance(value, int)


#%% LogLevel
class Test_LogLevel(unittest.TestCase):
    r"""
    Tests the LogLevel enumerator with the following cases:
        TBD
    """

    pass


#%% Unit test execution
if __name__ == "__main__":
    unittest.main(exit=False)
