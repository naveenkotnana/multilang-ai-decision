"""Agent 3: Feature Engineering Agent.

Combines NLP signals with customer context into a flat feature
vector suitable for the ML predictor.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from .nlp_agent import NLPResult

# All supported language ISO codes for one-hot encoding
_LANG_CODES = ["en", "hi", "te", "ta", "ml", "kn", "or", "mr"]


@dataclass
class FeatureVector:
    """Flat feature vector for the ML predictor."""
    urgency_signal: float
    sentiment_score: float
    urgency_keyword_count: int
    negative_keyword_count: int
    positive_keyword_count: int
    token_count: int
    customer_type_premium: int    # 1 = premium, 0 = regular
    interaction_count: int
    severity_score: int
    # one-hot language encoding
    lang_en: int
    lang_hi: int
    lang_te: int
    lang_ta: int
    lang_ml: int
    lang_kn: int
    lang_or: int
    lang_mr: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class FeatureAgent:
    """Builds a feature vector from NLP results + customer context."""

    name = "FEATURE_AGENT"

    def build(self, nlp: NLPResult, lang_code: str, context: dict) -> FeatureVector:
        lang_one_hot = {f"lang_{c}": int(c == lang_code) for c in _LANG_CODES}

        return FeatureVector(
            urgency_signal=nlp.urgency_signal,
            sentiment_score=nlp.sentiment_score,
            urgency_keyword_count=nlp.urgency_keyword_count,
            negative_keyword_count=nlp.negative_keyword_count,
            positive_keyword_count=nlp.positive_keyword_count,
            token_count=nlp.token_count,
            customer_type_premium=1 if context.get("customer_type") == "premium" else 0,
            interaction_count=context.get("interaction_count", 0),
            severity_score=context.get("severity_score", 5),
            **lang_one_hot,
        )
