import unittest
from calendar import timegm
from datetime import datetime
from json import JSONDecodeError

from ..src.utils import read_json_file, validate_timestamp


class TestUtils(unittest.TestCase):
    def test_file_not_found(self) -> None:
        with self.assertRaises(FileNotFoundError):
            read_json_file("./app/reportgenerator/test/sample_files/dne.json")

    def test_invalid_json(self) -> None:
        with self.assertRaises(JSONDecodeError):
            read_json_file("./app/reportgenerator/test/sample_files/invalid.json")

    def test_validate_timestamp(self):
        self.assertEqual(True, validate_timestamp(0))
        self.assertEqual(False, validate_timestamp(-1))
        self.assertEqual(
            True, validate_timestamp(timegm(datetime.now().timetuple()))
        )  # Current timestamp
        self.assertEqual(
            False, validate_timestamp(timegm(datetime.now().timetuple()) + 43471)
        )  # Future timestamp
