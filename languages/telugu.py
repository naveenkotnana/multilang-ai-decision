"""Telugu (తెలుగు) language module."""

from .base import LanguageModule


class TeluguModule(LanguageModule):
    @property
    def iso_code(self) -> str:
        return "te"

    @property
    def native_name(self) -> str:
        return "తెలుగు"

    @property
    def urgency_keywords(self) -> set[str]:
        return {
            "తొందరగా", "అత్యవసరం", "సమస్య", "విఫలం", "ఆపద",
            "సహాయం", "తక్షణ", "గంభీర", "చెడు", "ఆగిపోయింది",
            "పరిష్కరించండి", "కష్టం", "విఫలమైంది", "అవసరం", "దయచేసి",
        }

    @property
    def positive_sentiment_words(self) -> set[str]:
        return {
            "మంచి", "ధన్యవాదాలు", "బాగుంది", "సంతోషం", "సంతృప్తి",
            "అద్భుతం", "చాలా బాగుంది",
        }

    @property
    def negative_sentiment_words(self) -> set[str]:
        return {
            "చెడ్డ", "భయంకర", "కోపం", "నిరాశ", "ఇబ్బంది",
            "అసంతృప్తి", "పనికిరాదు", "అధ్వాన్నం",
        }

    @property
    def sample_texts(self) -> list[str]:
        return [
            "చెల్లింపు 3సార్లు విఫలమైంది, తొందరగా సహాయం కావాలి",
            "నా క్లెయిమ్ 2 వారాలుగా పెండింగ్‌లో ఉంది, దయచేసి పరిష్కరించండి",
            "సిస్టమ్ ఆగిపోయింది, నా ఖాతాను యాక్సెస్ చేయలేకపోతున్నాను",
            "ధన్యవాదాలు, నా సమస్య త్వరగా పరిష్కరించబడింది",
            "నా అడ్రస్ అప్‌డేట్ చేయాలి",
        ]

    def urgency_template(self, urgency: str, confidence: float) -> str:
        return f"అత్యవసరత: {urgency} (నమ్మకం: {confidence:.1%})"

    def action_label(self, action: str) -> str:
        labels = {
            "RESOLVE_TIER1": "టియర్ 1 వద్ద పరిష్కరించండి",
            "ESCALATE_TO_TIER2": "టియర్ 2 కు పంపండి",
            "ESCALATE_TO_TIER3": "టియర్ 3 కు పంపండి",
            "EMERGENCY": "అత్యవసర ప్రతిస్పందన",
        }
        return labels.get(action, action)

    def explanation_template(
        self, urgency: str, confidence: float, action: str, reasons: list[str],
    ) -> str:
        reason_text = "; ".join(reasons) if reasons else "ప్రామాణిక ప్రక్రియ"
        return (
            f"నిర్ణయం: {urgency} అత్యవసరత ({confidence:.1%} నమ్మకం). "
            f"చర్య: {self.action_label(action)}. "
            f"కారణం: {reason_text}."
        )
