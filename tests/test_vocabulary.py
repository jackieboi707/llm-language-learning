"""
Vocabulary Tests
"""

import unittest
from src.vocabulary import VocabularyAnalyzer


class TestVocabularyAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = VocabularyAnalyzer()

    def test_extract_words(self):
        """Test word extraction"""
        text = "The quick brown fox jumps over the lazy dog"
        words = self.analyzer.extract_words(text)
        self.assertGreater(len(words), 0)

    def test_vocabulary_level(self):
        """Test vocabulary level analysis"""
        text = "The cat sat on the mat"
        analysis = self.analyzer.analyze_vocabulary_level(text)
        self.assertIn("vocabulary_level", analysis)
        self.assertIn("lexical_diversity", analysis)


if __name__ == "__main__":
    unittest.main()
