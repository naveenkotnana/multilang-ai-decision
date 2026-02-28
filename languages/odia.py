"""Odia (ଓଡ଼ିଆ) language module."""

from .base import LanguageModule


class OdiaModule(LanguageModule):
    @property
    def iso_code(self) -> str:
        return "or"

    @property
    def native_name(self) -> str:
        return "ଓଡ଼ିଆ"

    @property
    def urgency_keywords(self) -> set[str]:
        return {
            "ଜରୁରୀ", "ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ", "ସମସ୍ୟା", "ବିଫଳ", "ତୁରନ୍ତ",
            "ସାହାଯ୍ୟ", "ଗମ୍ଭୀର", "ବନ୍ଦ", "କାମକରୁନାହିଁ",
            "ସମାଧାନ", "କଷ୍ଟ", "ଆବଶ୍ୟକ", "ଦୟାକରି",
        }

    @property
    def positive_sentiment_words(self) -> set[str]:
        return {
            "ଧନ୍ୟବାଦ", "ଭଲ", "ଖୁସି", "ସନ୍ତୁଷ୍ଟ", "ଅଦ୍ଭୁତ",
            "ଶ୍ରେଷ୍ଠ", "ଭଲରେ",
        }

    @property
    def negative_sentiment_words(self) -> set[str]:
        return {
            "ଖରାପ", "କ୍ରୋଧ", "ନିରାଶ", "ଅସୁବିଧା", "ଅସନ୍ତୁଷ୍ଟ",
            "ଭୟଙ୍କର", "ବେକାର",
        }

    @property
    def sample_texts(self) -> list[str]:
        return [
            "ପେମେଣ୍ଟ 3 ଥର ବିଫଳ ହୋଇଛି, ତୁରନ୍ତ ସାହାଯ୍ୟ ଦରକାର",
            "ମୋ ଦାବି 2 ସପ୍ତାହ ଧରି ବିଚାରାଧୀନ ଅଛି, ଦୟାକରି ସମାଧାନ କରନ୍ତୁ",
            "ସିଷ୍ଟମ ବନ୍ଦ ହୋଇଛି, ମୋ ଆକାଉଣ୍ଟ ଆକ୍ସେସ କରିପାରୁନାହିଁ",
            "ଧନ୍ୟବାଦ, ମୋ ସମସ୍ୟା ଶୀଘ୍ର ସମାଧାନ ହୋଇଗଲା",
            "ମୋ ଠିକଣା ଅପଡେଟ କରିବାକୁ ଦରକାର",
        ]

    def urgency_template(self, urgency: str, confidence: float) -> str:
        return f"ଜରୁରୀ ସ୍ଥିତି: {urgency} (ବିଶ୍ୱାସ: {confidence:.1%})"

    def action_label(self, action: str) -> str:
        labels = {
            "RESOLVE_TIER1": "ଟିଅର 1 ରେ ସମାଧାନ",
            "ESCALATE_TO_TIER2": "ଟିଅର 2 କୁ ପଠାନ୍ତୁ",
            "ESCALATE_TO_TIER3": "ଟିଅର 3 କୁ ପଠାନ୍ତୁ",
            "EMERGENCY": "ଜରୁରୀ କାର୍ଯ୍ୟ",
        }
        return labels.get(action, action)

    def explanation_template(
        self, urgency: str, confidence: float, action: str, reasons: list[str],
    ) -> str:
        reason_text = "; ".join(reasons) if reasons else "ମାନକ ପ୍ରକ୍ରିୟା"
        return (
            f"ନିର୍ଣ୍ଣୟ: {urgency} ଜରୁରୀ ସ୍ଥିତି ({confidence:.1%} ବିଶ୍ୱାସ). "
            f"କାର୍ଯ୍ୟ: {self.action_label(action)}. "
            f"କାରଣ: {reason_text}."
        )
