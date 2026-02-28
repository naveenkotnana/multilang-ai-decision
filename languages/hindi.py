"""Hindi (हिंदी) language module."""

from .base import LanguageModule


class HindiModule(LanguageModule):
    @property
    def iso_code(self) -> str:
        return "hi"

    @property
    def native_name(self) -> str:
        return "हिंदी"

    @property
    def urgency_keywords(self) -> set[str]:
        return {
            "तुरंत", "जरूरी", "आपातकाल", "गंभीर", "फेल",
            "समस्या", "मदद", "रुका", "बंद", "खराब",
            "तत्काल", "अत्यावश्यक", "विफल", "आवश्यक", "कृपया",
        }

    @property
    def positive_sentiment_words(self) -> set[str]:
        return {
            "अच्छा", "धन्यवाद", "शुक्रिया", "बढ़िया", "खुश",
            "संतुष्ट", "उत्तम", "सराहनीय",
        }

    @property
    def negative_sentiment_words(self) -> set[str]:
        return {
            "बुरा", "खराब", "गुस्सा", "निराश", "परेशान",
            "असंतुष्ट", "भयानक", "बेकार", "घटिया",
        }

    @property
    def sample_texts(self) -> list[str]:
        return [
            "भुगतान 3 बार फेल हो गया, तुरंत मदद चाहिए",
            "मेरा दावा 2 हफ्ते से लंबित है, कृपया हल करें",
            "सिस्टम बंद है और मैं अपना खाता एक्सेस नहीं कर पा रहा",
            "धन्यवाद, मेरी समस्या जल्दी हल हो गई",
            "मुझे अपना पता अपडेट करना है",
        ]

    def urgency_template(self, urgency: str, confidence: float) -> str:
        return f"गंभीरता: {urgency} (विश्वास: {confidence:.1%})"

    def action_label(self, action: str) -> str:
        labels = {
            "RESOLVE_TIER1": "टियर 1 पर समाधान",
            "ESCALATE_TO_TIER2": "टियर 2 को भेजें",
            "ESCALATE_TO_TIER3": "टियर 3 को भेजें",
            "EMERGENCY": "आपातकालीन प्रतिक्रिया",
        }
        return labels.get(action, action)

    def explanation_template(
        self, urgency: str, confidence: float, action: str, reasons: list[str],
    ) -> str:
        reason_text = "; ".join(reasons) if reasons else "मानक प्रक्रिया"
        return (
            f"निर्णय: {urgency} गंभीरता ({confidence:.1%} विश्वास)। "
            f"कार्रवाई: {self.action_label(action)}। "
            f"कारण: {reason_text}।"
        )
