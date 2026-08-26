"""
Translator Tests
"""

import unittest
from src.translator import Translator


class TestTranslator(unittest.TestCase):
    def setUp(self):
        self.translator = Translator()

    def test_initialization(self):
        """Test translator initialization"""
        self.assertIsNotNone(self.translator)

    def test_supported_languages(self):
        """Test supported language pairs"""
        languages = self.translator.get_supported_languages()
        self.assertIn("en-es", languages)
        self.assertIn("en-fr", languages)


if __name__ == "__main__":
    unittest.main()
