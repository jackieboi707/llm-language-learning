"""
FastAPI Server
Provides REST API endpoints for language learning AI
"""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from src.translator import Translator
from src.vocabulary import VocabularyAnalyzer
from src.grammar import GrammarChecker
from src.pronunciation import PronunciationGuide
from src.quiz import QuizSystem
from src.models import SUPPORTED_LANGUAGES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Language Learning AI API",
    description="REST API for language learning with AI",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize modules
translator = Translator()
vocab_analyzer = VocabularyAnalyzer()
grammar_checker = GrammarChecker()
pronunciation_guide = PronunciationGuide()
quiz_system = QuizSystem()


# Pydantic models
class TranslateRequest(BaseModel):
    text: str
    source_lang: str = "en"
    target_lang: str = "es"


class VocabularyRequest(BaseModel):
    text: str
    filter_stopwords: bool = True


class GrammarRequest(BaseModel):
    text: str


class PronunciationRequest(BaseModel):
    word: str
    language: str = "en"


class QuizRequest(BaseModel):
    language: str
    difficulty: str = "intermediate"
    count: int = 10


class QuizAnswerRequest(BaseModel):
    question_id: str
    answer: str


# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Language Learning AI API is running"}


# Translation endpoints
@app.post("/translate")
async def translate(request: TranslateRequest):
    """Translate text between languages"""
    try:
        result = translator.translate(
            text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
        )
        return result
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Vocabulary endpoints
@app.post("/vocabulary/extract")
async def extract_vocabulary(request: VocabularyRequest):
    """Extract vocabulary from text"""
    try:
        words = vocab_analyzer.extract_words(
            text=request.text, filter_stopwords=request.filter_stopwords
        )
        vocab_level = vocab_analyzer.analyze_vocabulary_level(request.text)
        return {"words": words, "analysis": vocab_level}
    except Exception as e:
        logger.error(f"Vocabulary extraction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Grammar endpoints
@app.post("/grammar/check")
async def check_grammar(request: GrammarRequest):
    """Check grammar and suggest corrections"""
    try:
        result = grammar_checker.suggest_corrections(request.text)
        return result
    except Exception as e:
        logger.error(f"Grammar checking error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Pronunciation endpoints
@app.post("/pronunciation")
async def get_pronunciation(request: PronunciationRequest):
    """Get pronunciation guide for a word"""
    try:
        phonetic = pronunciation_guide.get_phonetic_transcription(
            word=request.word, language=request.language
        )
        tips = pronunciation_guide.get_pronunciation_tips(request.word)
        return {**phonetic, "tips": tips}
    except Exception as e:
        logger.error(f"Pronunciation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Quiz endpoints
@app.post("/quiz/generate")
async def generate_quiz(request: QuizRequest):
    """Generate a quiz session"""
    try:
        quiz_session = quiz_system.generate_quiz_session(
            user_id="default",
            language=request.language,
            difficulty=request.difficulty,
            count=request.count,
        )
        return quiz_session
    except Exception as e:
        logger.error(f"Quiz generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Supported languages endpoint
@app.get("/languages")
async def get_languages():
    """Get list of supported languages"""
    return {"languages": SUPPORTED_LANGUAGES}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
