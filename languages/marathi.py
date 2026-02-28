"""Marathi (मराठी) language module."""

from .base import LanguageModule


class MarathiModule(LanguageModule):
    @property
    def iso_code(self) -> str:
        return "mr"

    @property
    def native_name(self) -> str:
        return "मराठी"

    @property
    def urgency_keywords(self) -> set[str]:
        return {
            "तातडी", "महत्त्वाचे", "समस्या", "अयशस्वी", "त्वरित",
            "मदत", "गंभीर", "बंद", "चालत_नाही",
            "सोडवा", "अडचण", "आवश्यक", "कृपया",
        }

    @property
    def positive_sentiment_words(self) -> set[str]:
        return {
            "धन्यवाद", "चांगले", "आनंद", "समाधानी", "उत्कृष्ट",
            "अप्रतिम", "छान",
        }

    @property
    def negative_sentiment_words(self) -> set[str]:
        return {
            "वाईट", "राग", "निराशा", "त्रास", "असमाधानी",
            "भयंकर", "निरुपयोगी",
        }

    @property
    def sample_texts(self) -> list[str]:
        return [
            "पेमेंट 3 वेळा अयशस्वी झाले, तातडीने मदत हवी",
            "माझा दावा 2 आठवड्यांपासून प्रलंबित आहे, कृपया सोडवा",
            "सिस्टम बंद आहे, माझे खाते ऍक्सेस करता येत नाही",
            "धन्यवाद, माझी समस्या लवकर सोडवली गेली",
            "माझा पत्ता अपडेट करायचा आहे",
        ]

    def urgency_template(self, urgency: str, confidence: float) -> str:
        return f"तातडी: {urgency} (विश्वास: {confidence:.1%})"

    def action_label(self, action: str) -> str:
        labels = {
            "RESOLVE_TIER1": "टियर 1 वर सोडवा",
            "ESCALATE_TO_TIER2": "टियर 2 ला पाठवा",
            "ESCALATE_TO_TIER3": "टियर 3 ला पाठवा",
            "EMERGENCY": "आणीबाणी कार्यवाही",
        }
        return labels.get(action, action)

    def explanation_template(
        self, urgency: str, confidence: float, action: str, reasons: list[str],
    ) -> str:
        reason_text = "; ".join(reasons) if reasons else "मानक प्रक्रिया"
        return (
            f"निर्णय: {urgency} तातडी ({confidence:.1%} विश्वास). "
            f"कार्यवाही: {self.action_label(action)}. "
            f"कारण: {reason_text}."
        )
