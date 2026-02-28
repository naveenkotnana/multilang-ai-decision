"""Abstract base class for all language modules."""

from abc import ABC, abstractmethod


class LanguageModule(ABC):
    """Each language implements this interface to provide language-specific
    keywords, templates, sample texts, and translations."""

    @property
    @abstractmethod
    def iso_code(self) -> str:
        """ISO 639-1 language code, e.g. 'te' for Telugu."""

    @property
    @abstractmethod
    def native_name(self) -> str:
        """Language name in its own script, e.g. 'తెలుగు'."""

    @property
    @abstractmethod
    def urgency_keywords(self) -> set[str]:
        """Set of words/phrases that signal urgency in this language."""

    @property
    @abstractmethod
    def positive_sentiment_words(self) -> set[str]:
        """Words indicating positive sentiment."""

    @property
    @abstractmethod
    def negative_sentiment_words(self) -> set[str]:
        """Words indicating negative sentiment."""

    @property
    @abstractmethod
    def sample_texts(self) -> list[str]:
        """Sample input texts for demo / testing."""

    @abstractmethod
    def urgency_template(self, urgency: str, confidence: float) -> str:
        """Return a native-language urgency explanation string."""

    @abstractmethod
    def action_label(self, action: str) -> str:
        """Translate an action code (ESCALATE_TO_TIER2, etc.) to native text."""

    @abstractmethod
    def explanation_template(
        self,
        urgency: str,
        confidence: float,
        action: str,
        reasons: list[str],
    ) -> str:
        """Full native-language explanation of the decision."""
