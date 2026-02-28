"""English language module."""

from .base import LanguageModule


class EnglishModule(LanguageModule):
    @property
    def iso_code(self) -> str:
        return "en"

    @property
    def native_name(self) -> str:
        return "English"

    @property
    def urgency_keywords(self) -> set[str]:
        return {
            "urgent", "emergency", "critical", "immediately", "asap",
            "failed", "broken", "error", "crash", "down", "help",
            "serious", "severe", "escalate", "priority", "important",
        }

    @property
    def positive_sentiment_words(self) -> set[str]:
        return {
            "good", "great", "thanks", "resolved", "happy", "satisfied",
            "excellent", "wonderful", "perfect", "appreciate",
        }

    @property
    def negative_sentiment_words(self) -> set[str]:
        return {
            "bad", "terrible", "worst", "angry", "frustrated", "annoyed",
            "disappointed", "horrible", "unacceptable", "pathetic", "useless",
        }

    @property
    def sample_texts(self) -> list[str]:
        return [
            "Payment failed 3 times, urgent help needed",
            "My claim has been pending for 2 weeks, please resolve",
            "System is down and I cannot access my account",
            "Thank you, my issue was resolved quickly",
            "I need to update my address on file",
        ]

    def urgency_template(self, urgency: str, confidence: float) -> str:
        return f"Urgency: {urgency} (Confidence: {confidence:.1%})"

    def action_label(self, action: str) -> str:
        labels = {
            "RESOLVE_TIER1": "Resolve at Tier 1",
            "ESCALATE_TO_TIER2": "Escalate to Tier 2",
            "ESCALATE_TO_TIER3": "Escalate to Tier 3",
            "EMERGENCY": "Emergency Response",
        }
        return labels.get(action, action)

    def explanation_template(
        self, urgency: str, confidence: float, action: str, reasons: list[str],
    ) -> str:
        reason_text = "; ".join(reasons) if reasons else "Standard processing"
        return (
            f"Decision: {urgency} urgency ({confidence:.1%} confidence). "
            f"Action: {self.action_label(action)}. "
            f"Reasoning: {reason_text}."
        )
