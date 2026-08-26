"""
Vocabulary Building and Analysis Module
Extracts vocabulary from text and tracks learning progress
"""

import logging
from typing import Dict, List, Optional, Tuple
from collections import Counter
from src.utils import TextProcessor, DifficultyCalculator

logger = logging.getLogger(__name__)

COMMON_STOPWORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
    'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'or', 'that',
    'the', 'to', 'was', 'will', 'with', 'you',
}


class VocabularyAnalyzer:
    """Analyzes text and extracts vocabulary for learning"""

    def __init__(self):
        self.text_processor = TextProcessor()
        self.vocabulary_database: Dict[str, Dict] = {}

    def extract_words(
        self, text: str, filter_stopwords: bool = True
    ) -> List[Dict[str, any]]:
        """
        Extract words from text with difficulty level

        Args:
            text: Text to analyze
            filter_stopwords: Whether to filter common stopwords

        Returns:
            List of word dictionaries with metadata
        """
        words = self.text_processor.tokenize(text)
        word_freq = Counter(words)

        extracted = []
        for word, frequency in word_freq.items():
            if filter_stopwords and word in COMMON_STOPWORDS:
                continue

            difficulty = DifficultyCalculator.calculate_word_difficulty(word)
            extracted.append(
                {
                    "text": word,
                    "frequency": frequency,
                    "difficulty": difficulty,
                    "length": len(word),
                }
            )

        return sorted(extracted, key=lambda x: x["frequency"], reverse=True)

    def analyze_vocabulary_level(self, text: str) -> Dict[str, any]:
        """
        Analyze overall vocabulary level of text

        Args:
            text: Text to analyze

        Returns:
            Dictionary with vocabulary statistics
        """
        words = self.text_processor.tokenize(text)
        unique_words = set(words)

        difficulty_counts = {"beginner": 0, "intermediate": 0, "advanced": 0}
        total_length = 0

        for word in unique_words:
            difficulty = DifficultyCalculator.calculate_word_difficulty(word)
            difficulty_counts[difficulty] += 1
            total_length += len(word)

        lexical_diversity = len(unique_words) / len(words) if words else 0
        avg_word_length = total_length / len(unique_words) if unique_words else 0

        return {
            "total_words": len(words),
            "unique_words": len(unique_words),
            "lexical_diversity": round(lexical_diversity, 3),
            "avg_word_length": round(avg_word_length, 2),
            "difficulty_breakdown": difficulty_counts,
            "vocabulary_level": self._determine_vocab_level(difficulty_counts),
        }

    def _determine_vocab_level(self, difficulty_counts: Dict[str, int]) -> str:
        """Determine overall vocabulary level"""
        total = sum(difficulty_counts.values())
        if total == 0:
            return "unknown"

        advanced_ratio = difficulty_counts["advanced"] / total
        intermediate_ratio = difficulty_counts["intermediate"] / total

        if advanced_ratio > 0.3:
            return "advanced"
        elif intermediate_ratio > 0.3:
            return "intermediate"
        else:
            return "beginner"

    def add_to_learning_list(self, word: str, context: str = "") -> Dict[str, any]:
        """
        Add word to personal learning vocabulary

        Args:
            word: Word to learn
            context: Context sentence for the word

        Returns:
            Word entry dictionary
        """
        if word not in self.vocabulary_database:
            self.vocabulary_database[word] = {
                "word": word,
                "difficulty": DifficultyCalculator.calculate_word_difficulty(word),
                "contexts": [],
                "reviewed": 0,
                "correct_count": 0,
            }

        if context:
            self.vocabulary_database[word]["contexts"].append(context)

        return self.vocabulary_database[word]

    def get_learning_list(
        self, min_difficulty: Optional[str] = None
    ) -> List[Dict[str, any]]:
        """
        Get words from learning list

        Args:
            min_difficulty: Filter by minimum difficulty level

        Returns:
            List of words to learn
        """
        words = list(self.vocabulary_database.values())

        if min_difficulty:
            difficulty_order = {"beginner": 0, "intermediate": 1, "advanced": 2}
            min_level = difficulty_order.get(min_difficulty, 0)
            words = [
                w
                for w in words
                if difficulty_order.get(w["difficulty"], 0) >= min_level
            ]

        return sorted(words, key=lambda x: x["reviewed"])

    def mark_word_reviewed(self, word: str, correct: bool = True):
        """Mark a word as reviewed"""
        if word in self.vocabulary_database:
            self.vocabulary_database[word]["reviewed"] += 1
            if correct:
                self.vocabulary_database[word]["correct_count"] += 1
