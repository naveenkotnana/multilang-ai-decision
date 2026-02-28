"""Agent 7: Action Decision Agent.

Finalises the action, performs SLA compliance checks, and
produces the structured decision output.
"""

from __future__ import annotations

from dataclasses import dataclass
from .rule_agent import RuleResult


@dataclass
class ActionDecision:
    """Final decision output before audit."""
    action: str
    urgency: str
    confidence: float
    sla_hours: int
    sla_compliant: bool
    explanation: str
    language: str


class ActionAgent:
    """Final decision assembly + SLA compliance."""

    name = "ACTION_AGENT"

    def decide(
        self,
        urgency: str,
        confidence: float,
        rule_result: RuleResult,
        explanation: str,
        lang_code: str,
        processing_time_ms: float,
    ) -> ActionDecision:
        # SLA check: processing time must be under 2000ms
        sla_compliant = processing_time_ms < 2000.0

        return ActionDecision(
            action=rule_result.action,
            urgency=urgency,
            confidence=confidence,
            sla_hours=rule_result.sla_hours,
            sla_compliant=sla_compliant,
            explanation=explanation,
            language=lang_code,
        )
