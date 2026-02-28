"""Tamil (தமிழ்) language module."""

from .base import LanguageModule


class TamilModule(LanguageModule):
    @property
    def iso_code(self) -> str:
        return "ta"

    @property
    def native_name(self) -> str:
        return "தமிழ்"

    @property
    def urgency_keywords(self) -> set[str]:
        return {
            "அவசர", "முக்கிய", "பிரச்சனை", "தோல்வி", "உடனடி",
            "உதவி", "அவசரம்", "தீவிர", "நிறுத்தம்", "செயலிழப்பு",
            "தீர்வு", "கஷ்டம்", "தேவை", "துரிதம்", "தயவுசெய்து",
        }

    @property
    def positive_sentiment_words(self) -> set[str]:
        return {
            "நன்றி", "நல்ல", "மகிழ்ச்சி", "திருப்தி", "அருமை",
            "சிறந்த", "நன்று",
        }

    @property
    def negative_sentiment_words(self) -> set[str]:
        return {
            "மோசமான", "கோபம்", "ஏமாற்றம்", "தொல்லை", "அதிருப்தி",
            "பயங்கரமான", "பயனற்ற", "மிகவும்_கெட்ட",
        }

    @property
    def sample_texts(self) -> list[str]:
        return [
            "கட்டணம் 3 முறை தோல்வியடைந்தது, உடனடி உதவி தேவை",
            "எனது கோரிக்கை 2 வாரங்களாக நிலுவையில் உள்ளது, தயவுசெய்து தீர்வு காணுங்கள்",
            "அமைப்பு செயலிழந்தது, எனது கணக்கை அணுக முடியவில்லை",
            "நன்றி, எனது சிக்கல் விரைவாக தீர்க்கப்பட்டது",
            "எனது முகவரியை புதுப்பிக்க வேண்டும்",
        ]

    def urgency_template(self, urgency: str, confidence: float) -> str:
        return f"அவசரநிலை: {urgency} (நம்பிக்கை: {confidence:.1%})"

    def action_label(self, action: str) -> str:
        labels = {
            "RESOLVE_TIER1": "நிலை 1 இல் தீர்க்கவும்",
            "ESCALATE_TO_TIER2": "நிலை 2 க்கு அனுப்பவும்",
            "ESCALATE_TO_TIER3": "நிலை 3 க்கு அனுப்பவும்",
            "EMERGENCY": "அவசர நடவடிக்கை",
        }
        return labels.get(action, action)

    def explanation_template(
        self, urgency: str, confidence: float, action: str, reasons: list[str],
    ) -> str:
        reason_text = "; ".join(reasons) if reasons else "நிலையான செயல்முறை"
        return (
            f"முடிவு: {urgency} அவசரநிலை ({confidence:.1%} நம்பிக்கை). "
            f"நடவடிக்கை: {self.action_label(action)}. "
            f"காரணம்: {reason_text}."
        )
