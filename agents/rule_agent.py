"""Agent 5: Business Rules Engine.

Applies deterministic business rules on top of ML predictions,
handling premium customer escalation, severity overrides, and
SLA compliance.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass
class RuleResult:
    """Output of the rules engine."""
    action: str
    reasons: list[str]
    sla_hours: int
    rule_overridden: bool


class RuleAgent:
    """Applies business rules to adjust predictions."""

    name = "RULE_AGENT"

    # SLA targets per urgency level (hours)
    _SLA = {"LOW": 48, "MEDIUM": 24, "HIGH": 4, "EMERGENCY": 1}

    def evaluate(
        self,
        urgency: str,
        confidence: float,
        context: dict,
        lang_code: str,
    ) -> RuleResult:
        reasons: list[str] = []
        override = False
        action = self._base_action(urgency)

        # -------- Rule 1: Premium customer escalation --------
        if context.get("customer_type") == "premium":
            if urgency in ("MEDIUM", "HIGH"):
                action = "ESCALATE_TO_TIER2"
                reasons.append("Premium customer → auto-escalate")
                override = urgency == "MEDIUM"

        # -------- Rule 2: High severity override --------
        severity = context.get("severity_score", 5)
        if severity >= 9:
            action = "ESCALATE_TO_TIER3"
            reasons.append(f"Severity {severity}/10 → Tier 3")
            override = True
        elif severity >= 7 and urgency != "LOW":
            if action == "RESOLVE_TIER1":
                action = "ESCALATE_TO_TIER2"
                reasons.append(f"Severity {severity}/10 → upgrade to Tier 2")

        # -------- Rule 3: Repeated interactions --------
        interactions = context.get("interaction_count", 0)
        if interactions >= 5:
            if action in ("RESOLVE_TIER1", "ESCALATE_TO_TIER2"):
                action = "ESCALATE_TO_TIER2"
                reasons.append(f"{interactions} prior interactions → escalate")

        # -------- Rule 4: Emergency override --------
        if severity >= 10 and context.get("customer_type") == "premium":
            action = "EMERGENCY"
            reasons.append("Critical premium case → EMERGENCY")
            override = True

        # -------- Rule 5: Low-confidence safety net --------
        if confidence < 0.5:
            reasons.append(f"Low confidence {confidence:.0%} → human review")
            if action == "RESOLVE_TIER1":
                action = "ESCALATE_TO_TIER2"

        if not reasons:
            reasons.append("Standard processing rules applied")

        sla_hours = self._SLA.get(urgency, 24)

        return RuleResult(
            action=action,
            reasons=reasons,
            sla_hours=sla_hours,
            rule_overridden=override,
        )

    @staticmethod
    def _base_action(urgency: str) -> str:
        return {
            "LOW": "RESOLVE_TIER1",
            "MEDIUM": "ESCALATE_TO_TIER2",
            "HIGH": "ESCALATE_TO_TIER3",
        }.get(urgency, "ESCALATE_TO_TIER2")
