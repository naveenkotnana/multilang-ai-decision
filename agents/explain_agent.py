"""Agent 6: Explainability Agent.

Generates human-readable explanations in the detected native
language, using the language module templates.
"""

from __future__ import annotations

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from languages import LANGUAGE_REGISTRY


class ExplainAgent:
    """Produces native-language explanations of the decision."""

    name = "EXPLAIN_AGENT"

    def explain(
        self,
        lang_code: str,
        urgency: str,
        confidence: float,
        action: str,
        reasons: list[str],
    ) -> str:
        lang = LANGUAGE_REGISTRY.get(lang_code, LANGUAGE_REGISTRY["en"])
        return lang.explanation_template(urgency, confidence, action, reasons)
