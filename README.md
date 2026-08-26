# Language Learning AI Model

A comprehensive Python-based AI system for language learning, featuring neural machine translation, vocabulary building, and interactive language practice.

## Features

- **Neural Machine Translation**: Translate between multiple languages using transformer models
- **Vocabulary Builder**: Analyze and learn new words with context
- **Grammar Checker**: Identify and correct grammatical errors
- **Pronunciation Guide**: Phonetic transcriptions and audio guidance
- **Interactive Quiz System**: Test knowledge with adaptive difficulty
- **API Server**: RESTful API for integration with other applications
- **Multi-language Support**: English, Spanish, French, German, Mandarin, and more

## Installation

```bash
git clone https://github.com/jackieboi707/llm-language-learning.git
cd llm-language-learning
pip install -r requirements.txt
```

## Quick Start

### 1. Basic Translation

```python
from src.translator import Translator

translator = Translator()
result = translator.translate("Hello, how are you?", source_lang="en", target_lang="es")
print(result)
```

### 2. Vocabulary Analysis

```python
from src.vocabulary import VocabularyAnalyzer

analyzer = VocabularyAnalyzer()
words = analyzer.extract_words("The quick brown fox jumps over the lazy dog")
for word in words:
    print(f"{word['text']}: {word['difficulty']}")
```

### 3. Start the API Server

```bash
python -m src.api.server
```

The server will be available at `http://localhost:8000`

## Project Structure

```
llm-language-learning/
├── src/
│   ├── __init__.py
│   ├── translator.py          # Neural machine translation
│   ├── vocabulary.py          # Vocabulary building and analysis
│   ├── grammar.py             # Grammar checking
│   ├── pronunciation.py       # Pronunciation guide
│   ├── quiz.py                # Quiz and assessment system
│   ├── models.py              # Model management
│   ├── utils.py               # Utility functions
│   └── api/
│       ├── __init__.py
│       ├── server.py          # FastAPI server
│       └── routes.py          # API endpoints
├── data/
│   └── language_pairs.json    # Language pair configurations
├── tests/
│   └── test_*.py
├── notebooks/
│   └── demo.ipynb
├── requirements.txt
├���─ .env.example
├── README.md
└── main.py
```

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

## Usage Examples

### Grammar Checking

```python
from src.grammar import GrammarChecker

checker = GrammarChecker()
errors = checker.check("He go to the store yesterday")
for error in errors:
    print(f"Error: {error['message']} -> {error['correction']}")
```

### Quiz System

```python
from src.quiz import QuizSystem

quiz = QuizSystem()
questions = quiz.generate_quiz(language="es", difficulty="intermediate", count=10)
for q in questions:
    print(q.get_question())
```

## API Endpoints

- `POST /translate` - Translate text between languages
- `POST /vocabulary/extract` - Extract vocabulary from text
- `POST /grammar/check` - Check grammar and get corrections
- `POST /pronunciation` - Get pronunciation guide
- `POST /quiz/generate` - Generate quiz questions
- `GET /languages` - List supported languages
- `GET /health` - Health check

## Contributing

Pull requests are welcome! For major changes, please open an issue first.

## License

MIT License - see LICENSE file for details

## Roadmap

- [ ] Multi-language support expansion
- [ ] Audio processing and speech recognition
- [ ] Spaced repetition algorithm for vocabulary
- [ ] User progress tracking and analytics
- [ ] Mobile app integration
- [ ] Real-time dialogue practice with AI
