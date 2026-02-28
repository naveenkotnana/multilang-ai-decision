"""Agent 1: Language Detection Agent.

Uses langdetect library with keyword-based fallback to identify
the input language from among the 8 supported Indian languages.
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from langdetect import detect, DetectorFactory
from languages import LANGUAGE_REGISTRY

# Make langdetect deterministic
DetectorFactory.seed = 42

# ISO code mapping from langdetect output to our internal codes
_LANGDETECT_MAP = {
    "te": "te",
    "hi": "hi",
    "ta": "ta",
    "ml": "ml",
    "kn": "kn",
    "or": "or",
    "mr": "mr",
    "en": "en",
}


class LangDetectorAgent:
    """Detects language from text using langdetect + keyword fallback."""

    name = "LANG_DETECTOR"

    def detect(self, text: str) -> str:
        """Return ISO code of the detected language.

        Strategy:
        1. Try langdetect library first
        2. If unrecognised, fall back to keyword scoring across all languages
        3. Default to English
        """
        # ---- primary: langdetect ----
        try:
            raw = detect(text)
            code = _LANGDETECT_MAP.get(raw)
            if code and code in LANGUAGE_REGISTRY:
                return code
        except Exception:
            pass

        # ---- fallback: keyword scoring ----
        best_code = "en"
        best_score = 0
        words = set(text.lower().split())

        for code, lang_module in LANGUAGE_REGISTRY.items():
            if code == "en":
                continue  # score English last as default
            score = len(words & lang_module.urgency_keywords)
            score += len(words & lang_module.negative_sentiment_words)
            score += len(words & lang_module.positive_sentiment_words)
            if score > best_score:
                best_score = score
                best_code = code

        return best_code
