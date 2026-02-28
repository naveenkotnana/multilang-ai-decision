"""MCP (Multi-Context Protocol) Orchestrator Pipeline.

Wires all 8 agents in sequence:
INPUT → LangDetector → NLPAgent → FeatureAgent → MLPredictor →
RuleAgent → ExplainAgent → ActionAgent → AuditAgent → OUTPUT
"""

from __future__ import annotations

import time
from dataclasses import dataclass, asdict
from typing import Any

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agents.lang_detector import LangDetectorAgent
from agents.nlp_agent import NLPAgent
from agents.feature_agent import FeatureAgent
from agents.ml_predictor import MLPredictorAgent
from agents.rule_agent import RuleAgent
from agents.explain_agent import ExplainAgent
from agents.action_agent import ActionAgent
from agents.audit_agent import AuditAgent


@dataclass
class DecisionOutput:
    """Complete decision output from the MCP pipeline."""
    audit_id: str
    urgency: str
    action: str
    confidence: float
    language: str
    explanation: str
    sla_hours: int
    sla_compliant: bool
    processing_time_ms: float
    reasons: list[str]
    agent_trace: list[dict[str, Any]]

    def to_dict(self) -> dict:
        return asdict(self)


class MCPOrchestrator:
    """Orchestrates the 8-agent MCP pipeline for multilingual decision making."""

    def __init__(self):
        self.lang_detector = LangDetectorAgent()
        self.nlp_agent = NLPAgent()
        self.feature_agent = FeatureAgent()
        self.ml_predictor = MLPredictorAgent()
        self.rule_agent = RuleAgent()
        self.explain_agent = ExplainAgent()
        self.action_agent = ActionAgent()
        self.audit_agent = AuditAgent()

    def process(self, text: str, context: dict) -> DecisionOutput:
        """Run the full MCP pipeline and return a DecisionOutput."""
        trace: list[dict[str, Any]] = []
        start = time.perf_counter()

        # ── Agent 1: Language Detection ──────────────────────
        t0 = time.perf_counter()
        lang_code = self.lang_detector.detect(text)
        trace.append({
            "agent": self.lang_detector.name,
            "output": {"language": lang_code},
            "time_ms": round((time.perf_counter() - t0) * 1000, 2),
        })

        # ── Agent 2: NLP Preprocessing ──────────────────────
        t0 = time.perf_counter()
        nlp_result = self.nlp_agent.process(text, lang_code)
        trace.append({
            "agent": self.nlp_agent.name,
            "output": {
                "urgency_signal": nlp_result.urgency_signal,
                "sentiment_score": nlp_result.sentiment_score,
                "urgency_keywords": nlp_result.urgency_keyword_count,
                "token_count": nlp_result.token_count,
            },
            "time_ms": round((time.perf_counter() - t0) * 1000, 2),
        })

        # ── Agent 3: Feature Engineering ────────────────────
        t0 = time.perf_counter()
        features = self.feature_agent.build(nlp_result, lang_code, context)
        trace.append({
            "agent": self.feature_agent.name,
            "output": features.to_dict(),
            "time_ms": round((time.perf_counter() - t0) * 1000, 2),
        })

        # ── Agent 4: ML Prediction ─────────────────────────
        t0 = time.perf_counter()
        urgency, confidence = self.ml_predictor.predict(features)
        trace.append({
            "agent": self.ml_predictor.name,
            "output": {"urgency": urgency, "confidence": confidence},
            "time_ms": round((time.perf_counter() - t0) * 1000, 2),
        })

        # ── Agent 5: Business Rules ────────────────────────
        t0 = time.perf_counter()
        rule_result = self.rule_agent.evaluate(urgency, confidence, context, lang_code)
        trace.append({
            "agent": self.rule_agent.name,
            "output": {
                "action": rule_result.action,
                "reasons": rule_result.reasons,
                "sla_hours": rule_result.sla_hours,
                "overridden": rule_result.rule_overridden,
            },
            "time_ms": round((time.perf_counter() - t0) * 1000, 2),
        })

        # ── Agent 6: Explainability ────────────────────────
        t0 = time.perf_counter()
        explanation = self.explain_agent.explain(
            lang_code, urgency, confidence, rule_result.action, rule_result.reasons,
        )
        trace.append({
            "agent": self.explain_agent.name,
            "output": {"explanation": explanation},
            "time_ms": round((time.perf_counter() - t0) * 1000, 2),
        })

        # ── Agent 7: Action Decision ──────────────────────
        elapsed_ms = (time.perf_counter() - start) * 1000
        t0 = time.perf_counter()
        action_decision = self.action_agent.decide(
            urgency, confidence, rule_result, explanation, lang_code, elapsed_ms,
        )
        trace.append({
            "agent": self.action_agent.name,
            "output": {
                "action": action_decision.action,
                "sla_compliant": action_decision.sla_compliant,
            },
            "time_ms": round((time.perf_counter() - t0) * 1000, 2),
        })

        # ── Agent 8: Audit Logging ─────────────────────────
        total_ms = (time.perf_counter() - start) * 1000
        t0 = time.perf_counter()
        audit_id = self.audit_agent.log(
            input_text=text,
            language=lang_code,
            urgency=urgency,
            action=rule_result.action,
            confidence=confidence,
            sla_hours=rule_result.sla_hours,
            sla_compliant=action_decision.sla_compliant,
            processing_ms=total_ms,
            explanation=explanation,
            context=context,
            reasons=rule_result.reasons,
        )
        trace.append({
            "agent": self.audit_agent.name,
            "output": {"audit_id": audit_id},
            "time_ms": round((time.perf_counter() - t0) * 1000, 2),
        })

        total_ms = (time.perf_counter() - start) * 1000

        return DecisionOutput(
            audit_id=audit_id,
            urgency=urgency,
            action=rule_result.action,
            confidence=confidence,
            language=lang_code,
            explanation=explanation,
            sla_hours=rule_result.sla_hours,
            sla_compliant=action_decision.sla_compliant,
            processing_time_ms=round(total_ms, 2),
            reasons=rule_result.reasons,
            agent_trace=trace,
        )
