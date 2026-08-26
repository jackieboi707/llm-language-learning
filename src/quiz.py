"""
Quiz and Assessment Module
Provides interactive quizzes for language learning
"""

import logging
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    FILL_BLANK = "fill_blank"
    TRANSLATION = "translation"
    MATCHING = "matching"


@dataclass
class Question:
    """Represents a quiz question"""

    id: str
    question_text: str
    question_type: QuestionType
    language: str
    difficulty: str
    options: List[str] = None
    correct_answer: str = None
    explanation: str = None

    def get_question(self) -> Dict[str, any]:
        """Get question as dictionary"""
        return {
            "id": self.id,
            "text": self.question_text,
            "type": self.question_type.value,
            "language": self.language,
            "difficulty": self.difficulty,
            "options": self.options,
        }


class QuizSystem:
    """Manages quiz generation and grading"""

    def __init__(self):
        self.question_bank = self._initialize_question_bank()
        self.user_scores = {}

    def _initialize_question_bank(self) -> Dict[str, List[Question]]:
        """Initialize question bank with sample questions"""
        return {
            "en": self._get_english_questions(),
            "es": self._get_spanish_questions(),
            "fr": self._get_french_questions(),
        }

    def _get_english_questions(self) -> List[Question]:
        """Get English questions"""
        return [
            Question(
                id="en_1",
                question_text="What is the past tense of 'go'?",
                question_type=QuestionType.MULTIPLE_CHOICE,
                language="en",
                difficulty="beginner",
                options=["go", "went", "going", "gone"],
                correct_answer="went",
            ),
            Question(
                id="en_2",
                question_text="Complete: 'I ___ to the store yesterday.'",
                question_type=QuestionType.FILL_BLANK,
                language="en",
                difficulty="beginner",
                correct_answer="went",
            ),
        ]

    def _get_spanish_questions(self) -> List[Question]:
        """Get Spanish questions"""
        return [
            Question(
                id="es_1",
                question_text="¿Cuál es el presente de 'ir'?",
                question_type=QuestionType.MULTIPLE_CHOICE,
                language="es",
                difficulty="beginner",
                options=["voy", "fui", "irá", "iba"],
                correct_answer="voy",
            ),
        ]

    def _get_french_questions(self) -> List[Question]:
        """Get French questions"""
        return [
            Question(
                id="fr_1",
                question_text="Quel est le présent de 'être'?",
                question_type=QuestionType.MULTIPLE_CHOICE,
                language="fr",
                difficulty="beginner",
                options=["suis", "étais", "serai", "sois"],
                correct_answer="suis",
            ),
        ]

    def generate_quiz(
        self,
        language: str,
        difficulty: str = "all",
        count: int = 10,
        question_types: Optional[List[QuestionType]] = None,
    ) -> List[Question]:
        """
        Generate a quiz with specified parameters

        Args:
            language: Language code
            difficulty: Difficulty level (beginner, intermediate, advanced, all)
            count: Number of questions
            question_types: Specific question types to include

        Returns:
            List of questions
        """
        if language not in self.question_bank:
            logger.warning(f"Language {language} not found in question bank")
            return []

        questions = self.question_bank[language]

        # Filter by difficulty
        if difficulty != "all":
            questions = [q for q in questions if q.difficulty == difficulty]

        # Filter by type
        if question_types:
            questions = [q for q in questions if q.question_type in question_types]

        # Sample and return
        return random.sample(questions, min(count, len(questions)))

    def grade_answer(
        self, question: Question, user_answer: str
    ) -> Dict[str, any]:
        """
        Grade a user's answer

        Args:
            question: Question object
            user_answer: User's answer

        Returns:
            Grading result dictionary
        """
        is_correct = user_answer.lower().strip() == question.correct_answer.lower().strip()

        return {
            "question_id": question.id,
            "correct": is_correct,
            "user_answer": user_answer,
            "correct_answer": question.correct_answer,
            "explanation": question.explanation,
        }

    def generate_quiz_session(
        self,
        user_id: str,
        language: str,
        difficulty: str = "intermediate",
        count: int = 10,
    ) -> Dict[str, any]:
        """
        Generate a complete quiz session for a user

        Args:
            user_id: User identifier
            language: Language code
            difficulty: Difficulty level
            count: Number of questions

        Returns:
            Quiz session dictionary
        """
        questions = self.generate_quiz(language, difficulty, count)

        session_id = f"{user_id}_{language}_{datetime.now().timestamp()}"

        return {
            "session_id": session_id,
            "user_id": user_id,
            "language": language,
            "difficulty": difficulty,
            "total_questions": len(questions),
            "questions": [q.get_question() for q in questions],
            "start_time": datetime.now().isoformat(),
        }
