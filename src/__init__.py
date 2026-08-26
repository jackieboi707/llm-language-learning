"""
Language Learning AI Model
A comprehensive Python-based AI system for language learning
"""

__version__ = "1.0.0"
__author__ = "Language Learning AI Team"

from src.translator import Translator
from src.vocabulary import VocabularyAnalyzer
from src.grammar import GrammarChecker
from src.pronunciation import PronunciationGuide
from src.quiz import QuizSystem

__all__ = [
    "Translator",
    "VocabularyAnalyzer",
    "GrammarChecker",
    "PronunciationGuide",
    "QuizSystem",
]
