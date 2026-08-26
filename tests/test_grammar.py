"""
Grammar Checker Tests
"""

import unittest
from src.grammar import GrammarChecker


class TestGrammarChecker(unittest.TestCase):
    def setUp(self):
        self.checker = GrammarChecker()

    def test_subject_verb_agreement(self):
        """Test subject-verb agreement checking"""
        text = "He go to the store"
        errors = self.checker.check(text)
        self.assertGreater(len(errors), 0)

    def test_capitalization(self):
        """Test capitalization checking"""
        text = "hello world"
        errors = self.checker.check(text)
        # Should find capitalization error
        self.assertTrue(any(e["error_type"] == "capitalization" for e in errors))


if __name__ == "__main__":
    unittest.main()
