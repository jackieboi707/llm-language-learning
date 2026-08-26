"""
Pronunciation Guide Module
Provides phonetic transcription and pronunciation guidance
"""

import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Basic phonetic alphabet mapping
IPAPHONETICS = {
    "en": {
        "th": "θ",
        "ch": "tʃ",
        "sh": "ʃ",
        "ng": "ŋ",
        "zh": "ʒ",
    }
}


class PronunciationGuide:
    """Provides pronunciation guides for words"""

    def __init__(self):
        self.word_stress_patterns = {
            # Common English patterns
            "photograph": "PHO-tuh-graf",
            "photography": "fuh-TAG-ruh-fee",
            "beautiful": "BEW-tuh-ful",
            "comfortable": "KUM-for-tuh-bul",
        }

    def get_phonetic_transcription(self, word: str, language: str = "en") -> Dict[str, any]:
        """
        Get IPA phonetic transcription for a word

        Args:
            word: Word to transcribe
            language: Language code

        Returns:
            Dictionary with phonetic information
        """
        # Simplified phonetic conversion
        phonetic = self._convert_to_phonetic(word, language)

        return {
            "word": word,
            "language": language,
            "phonetic_ipa": phonetic,
            "stress_pattern": self._get_stress_pattern(word),
            "syllable_count": self._count_syllables(word),
        }

    def _convert_to_phonetic(self, word: str, language: str) -> str:
        """Convert word to phonetic representation"""
        phonetic = word.lower()

        # Apply language-specific phonetic rules
        if language == "en" and language in IAPHONETCS:
            for pattern, replacement in IAPHONETCS[language].items():
                phonetic = phonetic.replace(pattern, replacement)

        return f"/{phonetic}/"

    def _get_stress_pattern(self, word: str) -> str:
        """Get syllable stress pattern"""
        if word.lower() in self.word_stress_patterns:
            return self.word_stress_patterns[word.lower()]
        # Default: return uppercase first syllable
        return word[0].upper() + word[1:]

    def _count_syllables(self, word: str) -> int:
        """Estimate syllable count"""
        vowels = "aeiou"
        syllable_count = 0
        previous_was_vowel = False

        for char in word.lower():
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel

        if word.lower().endswith("e"):
            syllable_count -= 1

        return max(1, syllable_count)

    def get_pronunciation_tips(self, word: str) -> List[str]:
        """
        Get pronunciation tips for a word

        Args:
            word: Word to get tips for

        Returns:
            List of pronunciation tips
        """
        tips = []
        word_lower = word.lower()

        # Common pronunciation rules
        if "th" in word_lower:
            tips.append("'th' sound: Place tongue between teeth, breathe out air")
        if "ch" in word_lower:
            tips.append("'ch' sound: Similar to 'tch', make a 'ch' sound")
        if "gh" in word_lower:
            tips.append("'gh' is often silent in English")
        if word_lower.endswith("ed"):
            tips.append("'ed' ending: Pronounced as 'id', 'd', or 't' sound")
        if word_lower.endswith("ing"):
            tips.append("'ing' ending: Pronounced as 'ng' sound (IŋGŋ)")

        return tips if tips else ["Practice with native speakers for best results"]
