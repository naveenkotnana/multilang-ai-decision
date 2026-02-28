"""Kannada (ಕನ್ನಡ) language module."""

from .base import LanguageModule


class KannadaModule(LanguageModule):
    @property
    def iso_code(self) -> str:
        return "kn"

    @property
    def native_name(self) -> str:
        return "ಕನ್ನಡ"

    @property
    def urgency_keywords(self) -> set[str]:
        return {
            "ತುರ್ತು", "ಮುಖ್ಯ", "ಸಮಸ್ಯೆ", "ವಿಫಲ", "ತಕ್ಷಣ",
            "ಸಹಾಯ", "ಗಂಭೀರ", "ನಿಂತಿದೆ", "ಕೆಲಸಮಾಡುತ್ತಿಲ್ಲ",
            "ಪರಿಹರಿಸಿ", "ಕಷ್ಟ", "ಅವಶ್ಯಕ", "ದಯವಿಟ್ಟು",
        }

    @property
    def positive_sentiment_words(self) -> set[str]:
        return {
            "ಧನ್ಯವಾದ", "ಒಳ್ಳೆಯ", "ಸಂತೋಷ", "ತೃಪ್ತಿ", "ಅದ್ಭುತ",
            "ಶ್ರೇಷ್ಠ", "ಚೆನ್ನಾಗಿ",
        }

    @property
    def negative_sentiment_words(self) -> set[str]:
        return {
            "ಕೆಟ್ಟ", "ಕೋಪ", "ನಿರಾಶೆ", "ತೊಂದರೆ", "ಅಸಮಾಧಾನ",
            "ಭಯಂಕರ", "ನಿಷ್ಪ್ರಯೋಜಕ",
        }

    @property
    def sample_texts(self) -> list[str]:
        return [
            "ಪಾವತಿ 3 ಬಾರಿ ವಿಫಲವಾಗಿದೆ, ತುರ್ತು ಸಹಾಯ ಬೇಕು",
            "ನನ್ನ ಕ್ಲೈಮ್ 2 ವಾರಗಳಿಂದ ಬಾಕಿ ಇದೆ, ದಯವಿಟ್ಟು ಪರಿಹರಿಸಿ",
            "ಸಿಸ್ಟಮ್ ನಿಂತಿದೆ, ನನ್ನ ಖಾತೆಯನ್ನು ಪ್ರವೇಶಿಸಲು ಸಾಧ್ಯವಿಲ್ಲ",
            "ಧನ್ಯವಾದ, ನನ್ನ ಸಮಸ್ಯೆ ತ್ವರಿತವಾಗಿ ಪರಿಹಾರವಾಯಿತು",
            "ನನ್ನ ವಿಳಾಸವನ್ನು ಅಪ್ಡೇಟ್ ಮಾಡಬೇಕು",
        ]

    def urgency_template(self, urgency: str, confidence: float) -> str:
        return f"ತುರ್ತುಸ್ಥಿತಿ: {urgency} (ವಿಶ್ವಾಸ: {confidence:.1%})"

    def action_label(self, action: str) -> str:
        labels = {
            "RESOLVE_TIER1": "ಟಿಯರ್ 1 ರಲ್ಲಿ ಪರಿಹರಿಸಿ",
            "ESCALATE_TO_TIER2": "ಟಿಯರ್ 2 ಗೆ ಕಳುಹಿಸಿ",
            "ESCALATE_TO_TIER3": "ಟಿಯರ್ 3 ಗೆ ಕಳುಹಿಸಿ",
            "EMERGENCY": "ತುರ್ತು ಕ್ರಮ",
        }
        return labels.get(action, action)

    def explanation_template(
        self, urgency: str, confidence: float, action: str, reasons: list[str],
    ) -> str:
        reason_text = "; ".join(reasons) if reasons else "ಪ್ರಮಾಣಿತ ಪ್ರಕ್ರಿಯೆ"
        return (
            f"ನಿರ್ಧಾರ: {urgency} ತುರ್ತುಸ್ಥಿತಿ ({confidence:.1%} ವಿಶ್ವಾಸ). "
            f"ಕ್ರಮ: {self.action_label(action)}. "
            f"ಕಾರಣ: {reason_text}."
        )
