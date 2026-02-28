"""Agent 2: NLP Pre-processing Agent.

Language-aware tokenization, urgency signal extraction, and
sentiment analysis using the language-specific keyword lists.
"""

from __future__ import annotations

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dataclasses import dataclass
from languages import LANGUAGE_REGISTRY


@dataclass
class NLPResult:
    """Output of NLP preprocessing."""
    tokens: list[str]
    urgency_signal: float        # 0.0 – 1.0
    sentiment_score: float       # -1.0 (neg) to +1.0 (pos)
    urgency_keyword_count: int
    negative_keyword_count: int
    positive_keyword_count: int
    token_count: int


class NLPAgent:
    """Language-aware NLP preprocessing agent."""

    name = "NLP_AGENT"

    def process(self, text: str, lang_code: str) -> NLPResult:
        lang = LANGUAGE_REGISTRY.get(lang_code, LANGUAGE_REGISTRY["en"])
        tokens = text.split()
        token_set = set(t.lower() for t in tokens)

        urgency_hits = len(token_set & lang.urgency_keywords)
        positive_hits = len(token_set & lang.positive_sentiment_words)
        negative_hits = len(token_set & lang.negative_sentiment_words)

        token_count = max(len(tokens), 1)
        urgency_signal = min(urgency_hits / token_count, 1.0)

        sentiment_total = positive_hits + negative_hits
        if sentiment_total == 0:
            sentiment_score = 0.0
        else:
            sentiment_score = (positive_hits - negative_hits) / sentiment_total

        return NLPResult(
            tokens=tokens,
            urgency_signal=urgency_signal,
            sentiment_score=sentiment_score,
            urgency_keyword_count=urgency_hits,
            negative_keyword_count=negative_hits,
            positive_keyword_count=positive_hits,
            token_count=token_count,
        )
