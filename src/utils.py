"""
Utility Functions
General helper functions for the language learning AI
"""

import re
import string
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class TextProcessor:
    """Handles text preprocessing and normalization"""

    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    @staticmethod
    def tokenize(text: str) -> List[str]:
        """Simple tokenization into words"""
        text = text.lower()
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        return text.split()

    @staticmethod
    def get_sentences(text: str) -> List[str]:
        """Split text into sentences"""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]

    @staticmethod
    def remove_punctuation(text: str) -> str:
        """Remove punctuation from text"""
        return text.translate(str.maketrans('', '', string.punctuation))


class DifficultyCalculator:
    """Calculate text and word difficulty levels"""

    # Common words (high frequency)
    COMMON_WORDS = {
        'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have',
        'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you',
        'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they',
        'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my',
    }

    @staticmethod
    def calculate_word_difficulty(word: str) -> str:
        """Calculate difficulty level for a word"""
        word_lower = word.lower()

        # Check if it's a common word
        if word_lower in DifficultyCalculator.COMMON_WORDS:
            return "beginner"

        # Length-based heuristic
        if len(word) <= 4:
            return "beginner"
        elif len(word) <= 8:
            return "intermediate"
        else:
            return "advanced"

    @staticmethod
    def calculate_text_difficulty(text: str) -> Dict[str, any]:
        """Calculate overall text difficulty"""
        words = TextProcessor.tokenize(text)
        sentences = TextProcessor.get_sentences(text)

        avg_word_length = sum(len(w) for w in words) / len(words) if words else 0
        avg_sentence_length = len(words) / len(sentences) if sentences else 0

        # Flesch-Kincaid like score
        score = (0.39 * avg_sentence_length) + (11.8 * avg_word_length) - 15.59
        score = max(0, min(18, score))  # Clamp between 0-18

        if score < 6:
            level = "beginner"
        elif score < 12:
            level = "intermediate"
        else:
            level = "advanced"

        return {
            "level": level,
            "score": round(score, 2),
            "avg_word_length": round(avg_word_length, 2),
            "avg_sentence_length": round(avg_sentence_length, 2),
        }


class LanguageDetector:
    """Detect language of text"""

    LANGUAGE_PATTERNS = {
        "es": ["el", "la", "de", "que", "está"],
        "fr": ["le", "la", "de", "que", "est"],
        "de": ["der", "die", "das", "und", "ist"],
        "zh": ["的", "一", "是", "在", "了"],
    }

    @staticmethod
    def detect_language(text: str) -> Tuple[str, float]:
        """Detect language with confidence score"""
        text_lower = text.lower()
        words = TextProcessor.tokenize(text)

        lang_scores = {}
        for lang, patterns in LanguageDetector.LANGUAGE_PATTERNS.items():
            score = sum(1 for word in words if word in patterns)
            lang_scores[lang] = score

        if not any(lang_scores.values()):
            return "en", 0.5  # Default to English

        detected_lang = max(lang_scores, key=lang_scores.get)
        confidence = lang_scores[detected_lang] / len(words) if words else 0
        return detected_lang, min(1.0, confidence)


class MetricsCalculator:
    """Calculate various metrics for learning progress"""

    @staticmethod
    def calculate_accuracy(correct: int, total: int) -> float:
        """Calculate accuracy percentage"""
        if total == 0:
            return 0.0
        return (correct / total) * 100

    @staticmethod
    def calculate_retention_score(
        days_since_review: int, times_reviewed: int
    ) -> float:
        """Calculate vocabulary retention score using spaced repetition formula"""
        # Simplified leitner system
        base_retention = 0.9 ** (days_since_review / 7)
        review_bonus = min(0.2, times_reviewed * 0.05)
        return max(0, min(1.0, base_retention + review_bonus))

    @staticmethod
    def calculate_learning_speed(
        questions_answered: int, time_elapsed_seconds: int
    ) -> float:
        """Calculate learning speed (questions per minute)"""
        if time_elapsed_seconds == 0:
            return 0.0
        return (questions_answered / time_elapsed_seconds) * 60
