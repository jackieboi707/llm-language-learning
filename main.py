"""
Main Entry Point
Language Learning AI Application
"""

import logging
from src.translator import Translator
from src.vocabulary import VocabularyAnalyzer
from src.grammar import GrammarChecker
from src.pronunciation import PronunciationGuide
from src.quiz import QuizSystem
from src.utils import DifficultyCalculator, TextProcessor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def demo_translation():
    """Demonstrate translation capabilities"""
    print("\n=== Translation Demo ===")
    translator = Translator()
    result = translator.translate(
        "Hello, how are you today?",
        source_lang="en",
        target_lang="es"
    )
    if result['success']:
        print(f"English: {result['source_text']}")
        print(f"Spanish: {result['translated_text']}")
    else:
        print(f"Error: {result['error']}")


def demo_vocabulary():
    """Demonstrate vocabulary analysis"""
    print("\n=== Vocabulary Analysis Demo ===")
    analyzer = VocabularyAnalyzer()
    text = "The quick brown fox jumps over the lazy dog."
    words = analyzer.extract_words(text)
    print(f"Text: {text}")
    print(f"\nTop 5 words:")
    for word in words[:5]:
        print(f"  {word['text']}: {word['difficulty']} (frequency: {word['frequency']})")
    
    analysis = analyzer.analyze_vocabulary_level(text)
    print(f"\nVocabulary Level: {analysis['vocabulary_level']}")
    print(f"Lexical Diversity: {analysis['lexical_diversity']}")


def demo_grammar():
    """Demonstrate grammar checking"""
    print("\n=== Grammar Checking Demo ===")
    checker = GrammarChecker()
    text = "He go to the store yesterday"
    result = checker.suggest_corrections(text)
    print(f"Original: {result['original_text']}")
    print(f"Errors found: {result['errors_found']}")
    if result['errors']:
        for error in result['errors']:
            print(f"  - {error['message']}: {error['correction']}")
    print(f"Corrected: {result['corrected_text']}")


def demo_pronunciation():
    """Demonstrate pronunciation guide"""
    print("\n=== Pronunciation Guide Demo ===")
    guide = PronunciationGuide()
    word = "beautiful"
    phonetic = guide.get_phonetic_transcription(word)
    tips = guide.get_pronunciation_tips(word)
    print(f"Word: {word}")
    print(f"Stress Pattern: {phonetic['stress_pattern']}")
    print(f"Syllables: {phonetic['syllable_count']}")
    print(f"Tips: {tips}")


def demo_quiz():
    """Demonstrate quiz system"""
    print("\n=== Quiz System Demo ===")
    quiz = QuizSystem()
    questions = quiz.generate_quiz(language="en", difficulty="beginner", count=2)
    print(f"Generated {len(questions)} questions:")
    for i, q in enumerate(questions, 1):
        print(f"\n  Question {i}: {q.question_text}")
        if q.options:
            for opt in q.options:
                print(f"    - {opt}")


def main():
    """Run demonstration"""
    print("\n" + "="*50)
    print("Language Learning AI - Demo")
    print("="*50)
    
    demo_translation()
    demo_vocabulary()
    demo_grammar()
    demo_pronunciation()
    demo_quiz()
    
    print("\n" + "="*50)
    print("To start the API server, run:")
    print("  python -m src.api.server")
    print("="*50 + "\n")


if __name__ == "__main__":
    main()
