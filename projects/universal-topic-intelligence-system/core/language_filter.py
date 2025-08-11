#!/usr/bin/env python3
"""
Language Detection and Filtering Module
Provides language detection capabilities for content filtering
"""

from typing import Optional, List, Tuple
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
import logging
from dataclasses import dataclass

# Set seed for consistent results
DetectorFactory.seed = 0

@dataclass
class LanguageResult:
    """Result of language detection"""
    language: str
    confidence: float
    is_english: bool
    should_include: bool

class LanguageFilter:
    """
    Language detection and filtering for content items
    """
    
    def __init__(self, target_languages: List[str] = None, min_confidence: float = 0.7):
        """
        Initialize language filter
        
        Args:
            target_languages: List of language codes to include (default: ['en'])
            min_confidence: Minimum confidence threshold for language detection
        """
        self.target_languages = target_languages or ['en']
        self.min_confidence = min_confidence
        self.logger = logging.getLogger("LanguageFilter")
        
    def detect_language(self, text: str) -> LanguageResult:
        """
        Detect language of given text
        
        Args:
            text: Text to analyze
            
        Returns:
            LanguageResult with detection details
        """
        if not text or len(text.strip()) < 10:
            # Too short to reliably detect, assume English for short content
            return LanguageResult(
                language='en',
                confidence=0.5,
                is_english=True,
                should_include=True
            )
        
        try:
            # Clean text for better detection
            clean_text = self._clean_text_for_detection(text)
            
            # Detect language
            detected_lang = detect(clean_text)
            
            # Calculate confidence (langdetect doesn't provide confidence directly)
            # We use a heuristic based on text characteristics
            confidence = self._estimate_confidence(clean_text, detected_lang)
            
            is_english = detected_lang == 'en'
            should_include = (
                detected_lang in self.target_languages and 
                confidence >= self.min_confidence
            )
            
            self.logger.debug(f"Detected language: {detected_lang}, confidence: {confidence:.2f}")
            
            return LanguageResult(
                language=detected_lang,
                confidence=confidence,
                is_english=is_english,
                should_include=should_include
            )
            
        except LangDetectException as e:
            self.logger.warning(f"Language detection failed: {str(e)}, defaulting to English")
            # Default to English if detection fails
            return LanguageResult(
                language='en',
                confidence=0.3,
                is_english=True,
                should_include=True
            )
    
    def _clean_text_for_detection(self, text: str) -> str:
        """Clean text to improve language detection accuracy"""
        # Remove URLs, mentions, hashtags, and technical symbols that might confuse detection
        import re
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        
        # Remove technical terms that are common across languages
        technical_terms = ['API', 'SDK', 'CLI', 'JSON', 'HTTP', 'REST', 'GraphQL', 'npm', 'pip', 'git']
        for term in technical_terms:
            text = re.sub(r'\b' + term + r'\b', '', text, flags=re.IGNORECASE)
        
        # Remove code snippets (simple heuristic)
        text = re.sub(r'`[^`]*`', '', text)
        text = re.sub(r'```[\s\S]*?```', '', text)
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _estimate_confidence(self, text: str, detected_lang: str) -> float:
        """
        Estimate confidence based on text characteristics
        This is a heuristic since langdetect doesn't provide confidence scores
        """
        base_confidence = 0.8
        
        # Reduce confidence for very short text
        if len(text) < 50:
            base_confidence *= 0.7
        elif len(text) < 20:
            base_confidence *= 0.5
        
        # Reduce confidence if text contains mixed scripts
        has_latin = any(ord(c) < 256 for c in text)
        has_non_latin = any(ord(c) >= 256 for c in text)
        
        if has_latin and has_non_latin:
            base_confidence *= 0.8
        
        # Increase confidence for longer, well-formed text
        if len(text) > 200:
            base_confidence = min(0.95, base_confidence * 1.1)
        
        return base_confidence
    
    def should_include_content(self, title: str, description: str = "") -> Tuple[bool, LanguageResult]:
        """
        Determine if content should be included based on language
        
        Args:
            title: Content title
            description: Content description/summary
            
        Returns:
            Tuple of (should_include, language_result)
        """
        # Combine title and description for better detection
        combined_text = f"{title} {description}".strip()
        
        result = self.detect_language(combined_text)
        
        return result.should_include, result
    
    def filter_content_batch(self, content_items: List[dict]) -> Tuple[List[dict], List[dict]]:
        """
        Filter a batch of content items by language
        
        Args:
            content_items: List of content dictionaries with 'title' and optional 'description'
            
        Returns:
            Tuple of (included_items, excluded_items)
        """
        included = []
        excluded = []
        
        for item in content_items:
            title = item.get('title', '')
            description = item.get('description', item.get('summary', ''))
            
            should_include, lang_result = self.should_include_content(title, description)
            
            # Add language information to item
            item['detected_language'] = lang_result.language
            item['language_confidence'] = lang_result.confidence
            item['is_english'] = lang_result.is_english
            
            if should_include:
                included.append(item)
            else:
                excluded.append(item)
                self.logger.info(
                    f"Excluded non-English content: '{title[:50]}...' "
                    f"(detected: {lang_result.language}, confidence: {lang_result.confidence:.2f})"
                )
        
        return included, excluded
    
    def get_stats(self) -> dict:
        """Get language filter statistics"""
        return {
            "target_languages": self.target_languages,
            "min_confidence": self.min_confidence,
            "filter_active": True
        }

# Convenience function for quick language detection
def detect_content_language(text: str) -> str:
    """Quick language detection for content"""
    filter_instance = LanguageFilter()
    result = filter_instance.detect_language(text)
    return result.language

# Convenience function for English filtering
def is_english_content(title: str, description: str = "") -> bool:
    """Check if content is in English"""
    filter_instance = LanguageFilter()
    should_include, _ = filter_instance.should_include_content(title, description)
    return should_include