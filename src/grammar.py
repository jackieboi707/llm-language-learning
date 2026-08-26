"""
Grammar Checking Module
Identifies and corrects grammatical errors
"""

import logging
from typing import Dict, List, Optional
import re

logger = logging.getLogger(__name__)


class GrammarChecker:
    """Basic grammar checker using pattern matching and rules"""

    def __init__(self):
        self.error_rules = [
            self._check_subject_verb_agreement,
            self._check_article_usage,
            self._check_tense_consistency,
            self._check_capitalization,
        ]

    def check(self, text: str) -> List[Dict[str, any]]:
        """
        Check text for grammatical errors

        Args:
            text: Text to check

        Returns:
            List of error dictionaries
        """
        errors = []
        for rule in self.error_rules:
            errors.extend(rule(text))

        return sorted(errors, key=lambda x: x["position"])

    def _check_subject_verb_agreement(self, text: str) -> List[Dict[str, any]]:
        """Check subject-verb agreement"""
        errors = []
        # Simple pattern for common mistakes
        patterns = [
            (r"\b(he|she|it)\s+are\b", "is"),
            (r"\b(I|you|we|they)\s+is\b", "are"),
            (r"\bhe go\b", "he goes"),
            (r"\bshe go\b", "she goes"),
        ]

        for pattern, correction in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                errors.append(
                    {
                        "position": match.start(),
                        "text": match.group(),
                        "error_type": "subject_verb_agreement",
                        "message": "Subject-verb agreement error",
                        "correction": correction,
                    }
                )

        return errors

    def _check_article_usage(self, text: str) -> List[Dict[str, any]]:
        """Check article usage (a/an/the)"""
        errors = []
        # Simple patterns for common article mistakes
        patterns = [(r"\ba\s+[aeiou]", "an"), (r"\ban\s+[^aeiou]", "a")]

        for pattern, correction in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                errors.append(
                    {
                        "position": match.start(),
                        "text": match.group(),
                        "error_type": "article_usage",
                        "message": "Article usage error",
                        "correction": correction,
                    }
                )

        return errors

    def _check_tense_consistency(self, text: str) -> List[Dict[str, any]]:
        """Check tense consistency"""
        errors = []
        # This would require more sophisticated NLP
        # Placeholder for basic implementation
        return errors

    def _check_capitalization(self, text: str) -> List[Dict[str, any]]:
        """Check capitalization"""
        errors = []
        sentences = text.split(".")

        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if sentence and not sentence[0].isupper():
                errors.append(
                    {
                        "position": text.find(sentence),
                        "text": sentence[0] if sentence else "",
                        "error_type": "capitalization",
                        "message": "Sentence should start with capital letter",
                        "correction": sentence[0].upper() if sentence else "",
                    }
                )

        return errors

    def suggest_corrections(self, text: str) -> Dict[str, any]:
        """
        Suggest corrections for text

        Args:
            text: Text to correct

        Returns:
            Dictionary with original text and suggestions
        """
        errors = self.check(text)

        return {
            "original_text": text,
            "errors_found": len(errors),
            "errors": errors,
            "corrected_text": self._apply_corrections(text, errors),
        }

    def _apply_corrections(
        self, text: str, errors: List[Dict[str, any]]
    ) -> str:
        """Apply corrections to text"""
        corrected = text
        offset = 0

        for error in sorted(errors, key=lambda x: x["position"]):
            start = error["position"] + offset
            end = start + len(error["text"])
            correction = error["correction"]
            corrected = corrected[:start] + correction + corrected[end:]
            offset += len(correction) - len(error["text"])

        return corrected
