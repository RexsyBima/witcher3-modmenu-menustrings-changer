"""Unittest templates for witcher3-modmenu-changer."""

import unittest
import PySide6


class TestMain(unittest.TestCase):
    """Test config file path is relative to cwd."""

    def setUp(self) -> None:
        return super().setUp()

    def test_get_pyside_version(self):
        print(PySide6.__version__)
        return self.assertEqual(PySide6.__version__, "6.11.0")


if __name__ == "__main__":
    unittest.main()
