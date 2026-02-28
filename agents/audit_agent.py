"""Agent 8: Audit & Compliance Agent.

Logs every decision to an SQLite database with full context,
generates unique audit IDs, and supports compliance queries.
"""

from __future__ import annotations

import os
import sqlite3
import json
from datetime import datetime, timezone

_DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
_DB_PATH = os.path.join(_DB_DIR, "decisions.db")


class AuditAgent:
    """SOC2 / HIPAA-ready audit logging agent."""

    name = "AUDIT_AGENT"

    def __init__(self):
        os.makedirs(_DB_DIR, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(_DB_PATH) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS decisions (
                    audit_id        TEXT PRIMARY KEY,
                    timestamp       TEXT NOT NULL,
                    input_text      TEXT NOT NULL,
                    language        TEXT NOT NULL,
                    urgency         TEXT NOT NULL,
                    action          TEXT NOT NULL,
                    confidence      REAL NOT NULL,
                    sla_hours       INTEGER,
                    sla_compliant   INTEGER,
                    processing_ms   REAL,
                    explanation     TEXT,
                    context_json    TEXT,
                    reasons_json    TEXT
                )
            """)
            conn.commit()

    def log(
        self,
        input_text: str,
        language: str,
        urgency: str,
        action: str,
        confidence: float,
        sla_hours: int,
        sla_compliant: bool,
        processing_ms: float,
        explanation: str,
        context: dict,
        reasons: list[str],
    ) -> str:
        """Log decision and return a unique audit ID."""
        now = datetime.now(timezone.utc)
        # Format: DEC-{YYYY}-{seq5}-{city}
        seq = self._next_seq(now.year)
        audit_id = f"DEC-{now.year}-{seq:05d}-HYD"

        with sqlite3.connect(_DB_PATH) as conn:
            conn.execute(
                """INSERT INTO decisions VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    audit_id,
                    now.isoformat(),
                    input_text,
                    language,
                    urgency,
                    action,
                    confidence,
                    sla_hours,
                    int(sla_compliant),
                    processing_ms,
                    explanation,
                    json.dumps(context, ensure_ascii=False),
                    json.dumps(reasons, ensure_ascii=False),
                ),
            )
            conn.commit()
        return audit_id

    def _next_seq(self, year: int) -> int:
        with sqlite3.connect(_DB_PATH) as conn:
            row = conn.execute(
                "SELECT COUNT(*) FROM decisions WHERE audit_id LIKE ?",
                (f"DEC-{year}-%",),
            ).fetchone()
            return (row[0] if row else 0) + 1

    def get_recent(self, limit: int = 20) -> list[dict]:
        """Return recent audit entries for the dashboard."""
        with sqlite3.connect(_DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM decisions ORDER BY timestamp DESC LIMIT ?",
                (limit,),
            ).fetchall()
            return [dict(r) for r in rows]

    def get_stats(self) -> dict:
        """Return aggregate stats for the dashboard."""
        with sqlite3.connect(_DB_PATH) as conn:
            total = conn.execute("SELECT COUNT(*) FROM decisions").fetchone()[0]
            by_lang = conn.execute(
                "SELECT language, COUNT(*) as cnt FROM decisions GROUP BY language"
            ).fetchall()
            by_urgency = conn.execute(
                "SELECT urgency, COUNT(*) as cnt FROM decisions GROUP BY urgency"
            ).fetchall()
            avg_conf = conn.execute(
                "SELECT AVG(confidence) FROM decisions"
            ).fetchone()[0]
            return {
                "total_decisions": total,
                "by_language": {r[0]: r[1] for r in by_lang},
                "by_urgency": {r[0]: r[1] for r in by_urgency},
                "avg_confidence": avg_conf or 0.0,
            }
