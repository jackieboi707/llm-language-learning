"""
Model Management Module
Handles loading, caching, and managing language models
"""

import os
from typing import Dict, Optional, List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch
from functools import lru_cache
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelManager:
    """Manages loading and caching of language models"""

    def __init__(self, cache_dir: str = "./models"):
        self.cache_dir = cache_dir
        self.models_cache: Dict = {}
        self.tokenizers_cache: Dict = {}
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")

    def get_translation_model(self, model_name: str = "Helsinki-NLP/opus-mt-en-es"):
        """Load a translation model"""
        if model_name not in self.models_cache:
            logger.info(f"Loading model: {model_name}")
            tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=self.cache_dir)
            model = AutoModelForSeq2SeqLM.from_pretrained(
                model_name, cache_dir=self.cache_dir
            ).to(self.device)
            self.models_cache[model_name] = model
            self.tokenizers_cache[model_name] = tokenizer
        return self.models_cache[model_name], self.tokenizers_cache[model_name]

    def get_ner_pipeline(self, model_name: str = "dslim/bert-base-NER"):
        """Get Named Entity Recognition pipeline"""
        if model_name not in self.models_cache:
            logger.info(f"Loading NER pipeline: {model_name}")
            pipe = pipeline(
                "ner",
                model=model_name,
                device=0 if torch.cuda.is_available() else -1,
            )
            self.models_cache[model_name] = pipe
        return self.models_cache[model_name]

    def get_grammar_pipeline(self, model_name: str = "oliverguhr/spelling-correction-english-base"):
        """Get grammar correction pipeline"""
        if model_name not in self.models_cache:
            logger.info(f"Loading grammar pipeline: {model_name}")
            pipe = pipeline(
                "text2text-generation",
                model=model_name,
                device=0 if torch.cuda.is_available() else -1,
            )
            self.models_cache[model_name] = pipe
        return self.models_cache[model_name]

    def clear_cache(self):
        """Clear model cache"""
        self.models_cache.clear()
        self.tokenizers_cache.clear()
        logger.info("Model cache cleared")


LANGUAGE_MODELS = {
    "en-es": "Helsinki-NLP/opus-mt-en-es",
    "en-fr": "Helsinki-NLP/opus-mt-en-fr",
    "en-de": "Helsinki-NLP/opus-mt-en-de",
    "en-zh": "Helsinki-NLP/opus-mt-en-zh",
    "es-en": "Helsinki-NLP/opus-mt-es-en",
    "fr-en": "Helsinki-NLP/opus-mt-fr-en",
    "de-en": "Helsinki-NLP/opus-mt-de-en",
    "zh-en": "Helsinki-NLP/opus-mt-zh-en",
}

SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "zh": "Mandarin Chinese",
    "ja": "Japanese",
    "pt": "Portuguese",
    "it": "Italian",
}
