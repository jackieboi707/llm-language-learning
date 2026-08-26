"""
Neural Machine Translation Module
Provides translation capabilities between multiple languages
"""

import logging
from typing import Dict, List, Optional
from src.models import ModelManager, LANGUAGE_MODELS
from src.utils import TextProcessor

logger = logging.getLogger(__name__)


class Translator:
    """Handles translation between languages using pre-trained models"""

    def __init__(self):
        self.model_manager = ModelManager()
        self.text_processor = TextProcessor()

    def translate(
        self,
        text: str,
        source_lang: str = "en",
        target_lang: str = "es",
        batch_size: int = 32,
    ) -> Dict[str, any]:
        """
        Translate text from source language to target language

        Args:
            text: Text to translate
            source_lang: Source language code (e.g., 'en')
            target_lang: Target language code (e.g., 'es')
            batch_size: Batch size for processing

        Returns:
            Dictionary with translation results
        """
        try:
            text = self.text_processor.clean_text(text)

            model_key = f"{source_lang}-{target_lang}"
            if model_key not in LANGUAGE_MODELS:
                return {
                    "success": False,
                    "error": f"Translation pair {model_key} not supported",
                }

            model_name = LANGUAGE_MODELS[model_key]
            model, tokenizer = self.model_manager.get_translation_model(model_name)

            # Tokenize and translate
            inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
            translated = model.generate(**inputs, max_length=512, num_beams=4)
            translation = tokenizer.decode(translated[0], skip_special_tokens=True)

            return {
                "success": True,
                "source_text": text,
                "source_lang": source_lang,
                "target_lang": target_lang,
                "translated_text": translation,
                "model_used": model_name,
            }

        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
            }

    def batch_translate(
        self,
        texts: List[str],
        source_lang: str = "en",
        target_lang: str = "es",
    ) -> Dict[str, any]:
        """
        Translate multiple texts

        Args:
            texts: List of texts to translate
            source_lang: Source language code
            target_lang: Target language code

        Returns:
            Dictionary with batch translation results
        """
        translations = []
        for text in texts:
            result = self.translate(text, source_lang, target_lang)
            translations.append(result)

        return {
            "success": all(t.get("success", False) for t in translations),
            "translations": translations,
        }

    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported language pairs"""
        return LANGUAGE_MODELS

    def back_translate(
        self, text: str, source_lang: str = "en", intermediate_lang: str = "es"
    ) -> Dict[str, any]:
        """
        Translate text and back-translate to check quality

        Args:
            text: Original text
            source_lang: Source language
            intermediate_lang: Language to translate to and from

        Returns:
            Dictionary with original, intermediate, and back-translated text
        """
        # Forward translation
        forward = self.translate(text, source_lang, intermediate_lang)
        if not forward.get("success"):
            return forward

        # Back translation
        back = self.translate(
            forward["translated_text"], intermediate_lang, source_lang
        )

        return {
            "success": back.get("success", False),
            "original_text": text,
            "intermediate_text": forward["translated_text"],
            "back_translated_text": back.get("translated_text", ""),
            "source_lang": source_lang,
            "intermediate_lang": intermediate_lang,
        }
