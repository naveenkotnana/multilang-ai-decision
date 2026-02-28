"""Malayalam (മലയാളം) language module."""

from .base import LanguageModule


class MalayalamModule(LanguageModule):
    @property
    def iso_code(self) -> str:
        return "ml"

    @property
    def native_name(self) -> str:
        return "മലയാളം"

    @property
    def urgency_keywords(self) -> set[str]:
        return {
            "അടിയന്തിരം", "പ്രധാനം", "പ്രശ്നം", "പരാജയം", "ഉടൻ",
            "സഹായം", "ഗുരുതരം", "നിലച്ചു", "പ്രവർത്തനരഹിതം",
            "പരിഹരിക്കുക", "ബുദ്ധിമുട്ട്", "ആവശ്യം", "ദയവായി",
        }

    @property
    def positive_sentiment_words(self) -> set[str]:
        return {
            "നന്ദി", "നല്ലത്", "സന്തോഷം", "തൃപ്തി", "മികച്ചത്",
            "അത്ഭുതം", "നന്നായി",
        }

    @property
    def negative_sentiment_words(self) -> set[str]:
        return {
            "മോശം", "ദേഷ്യം", "നിരാശ", "ബുദ്ധിമുട്ട്", "അതൃപ്തി",
            "ഭയങ്കരം", "ഉപയോഗശൂന്യം",
        }

    @property
    def sample_texts(self) -> list[str]:
        return [
            "പേയ്മെന്റ് 3 തവണ പരാജയപ്പെട്ടു, ഉടൻ സഹായം വേണം",
            "എന്റെ ക്ലെയിം 2 ആഴ്ചയായി പെൻഡിംഗിലാണ്, ദയവായി പരിഹരിക്കുക",
            "സിസ്റ്റം നിലച്ചു, എന്റെ അക്കൗണ്ട് ആക്സസ് ചെയ്യാൻ കഴിയുന്നില്ല",
            "നന്ദി, എന്റെ പ്രശ്നം വേഗത്തിൽ പരിഹരിച്ചു",
            "എന്റെ വിലാസം അപ്ഡേറ്റ് ചെയ്യണം",
        ]

    def urgency_template(self, urgency: str, confidence: float) -> str:
        return f"അടിയന്തിരത: {urgency} (വിശ്വാസം: {confidence:.1%})"

    def action_label(self, action: str) -> str:
        labels = {
            "RESOLVE_TIER1": "ടിയർ 1 ൽ പരിഹരിക്കുക",
            "ESCALATE_TO_TIER2": "ടിയർ 2 ലേക്ക് അയയ്ക്കുക",
            "ESCALATE_TO_TIER3": "ടിയർ 3 ലേക്ക് അയയ്ക്കുക",
            "EMERGENCY": "അടിയന്തിര നടപടി",
        }
        return labels.get(action, action)

    def explanation_template(
        self, urgency: str, confidence: float, action: str, reasons: list[str],
    ) -> str:
        reason_text = "; ".join(reasons) if reasons else "സ്ഥിരമായ പ്രക്രിയ"
        return (
            f"തീരുമാനം: {urgency} അടിയന്തിരത ({confidence:.1%} വിശ്വാസം). "
            f"നടപടി: {self.action_label(action)}. "
            f"കാരണം: {reason_text}."
        )
