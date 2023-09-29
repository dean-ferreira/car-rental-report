import unittest
from json import JSONDecodeError

from ..src.utils import read_json_file


class TestUtils(unittest.TestCase):
    def test_file_not_found(self) -> None:
        with self.assertRaises(FileNotFoundError):
            read_json_file("./app/reportgenerator/test/sample_files/dne.json")

    def test_invalid_json(self) -> None:
        with self.assertRaises(JSONDecodeError):
            read_json_file("./app/reportgenerator/test/sample_files/invalid.json")
