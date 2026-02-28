"""
🌐 Multi-Language AI Decision Automation Dashboard
8 Indian Languages × 8 Specialized Agents × MCP Pipeline

Run: streamlit run app.py --server.port 8501
"""

from __future__ import annotations

import sys
import os
import time
import json

sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st

from orchestrator.mcp_pipeline import MCPOrchestrator
from languages import LANGUAGE_REGISTRY, LANGUAGE_NAMES
from agents.audit_agent import AuditAgent

# ──────────────────── Page Config ────────────────────
st.set_page_config(
    page_title="Multi-Language AI Decision System",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────── Custom CSS ─────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    .stApp {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }

    .main-header h1 {
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .main-header p {
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }

    .result-card {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        border-radius: 16px;
        padding: 1.5rem;
        color: white;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        margin-bottom: 1rem;
    }

    .metric-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 0.75rem 1.25rem;
        margin: 0.25rem;
        border: 1px solid rgba(255,255,255,0.1);
        font-size: 0.95rem;
    }

    .urgency-high {
        border-left: 4px solid #ff4757;
        background: linear-gradient(145deg, #2d1b2e, #1a1a2e);
    }

    .urgency-medium {
        border-left: 4px solid #ffa502;
        background: linear-gradient(145deg, #2d2a1b, #1a1a2e);
    }

    .urgency-low {
        border-left: 4px solid #2ed573;
        background: linear-gradient(145deg, #1b2d1e, #1a1a2e);
    }

    .agent-trace {
        background: rgba(255,255,255,0.03);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        border-left: 3px solid #667eea;
        font-family: 'Inter', monospace;
        font-size: 0.85rem;
    }

    .lang-chip {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.15rem;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
    }

    .sidebar-info {
        background: rgba(102, 126, 234, 0.08);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(102, 126, 234, 0.2);
        margin-bottom: 1rem;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.75rem;
    }

    .stat-item {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        color: white;
        border: 1px solid rgba(255,255,255,0.1);
    }

    .stat-item .value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
    }

    .stat-item .label {
        font-size: 0.75rem;
        opacity: 0.7;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────── Header ─────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🌐 Multi-Language AI Decision Automation</h1>
    <p>8 Indian Languages • 8 AI Agents • MCP Pipeline • Enterprise Ready</p>
</div>
""", unsafe_allow_html=True)

# ──────────────────── Sidebar ────────────────────────
with st.sidebar:
    st.markdown("### 🎛️ Configuration")

    st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
    st.markdown("**Supported Languages:**")
    for code, name in LANGUAGE_NAMES.items():
        st.markdown(f'<span class="lang-chip">{name}</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 👤 Customer Context")

    customer_type = st.selectbox(
        "Customer Type",
        ["regular", "premium"],
        help="Premium customers get auto-escalation",
    )

    interaction_count = st.slider(
        "Prior Interactions",
        min_value=0,
        max_value=10,
        value=2,
        help="Number of previous interactions",
    )

    severity_score = st.slider(
        "Severity Score",
        min_value=1,
        max_value=10,
        value=7,
        help="1 = Minor, 10 = Critical",
    )

    st.markdown("---")
    st.markdown("### 🏗️ Agent Pipeline")
    st.markdown("""
    ```
    1. 🔍 LANG_DETECTOR
    2. 📝 NLP_AGENT
    3. ⚙️ FEATURE_AGENT
    4. 🤖 ML_PREDICTOR
    5. 📋 RULE_AGENT
    6. 💡 EXPLAIN_AGENT
    7. 🎯 ACTION_AGENT
    8. 📊 AUDIT_AGENT
    ```
    """)

# ──────────────────── Sample Texts ───────────────────
SAMPLE_TEXTS = {}
for code, lang_module in LANGUAGE_REGISTRY.items():
    name = LANGUAGE_NAMES[code]
    SAMPLE_TEXTS[name] = lang_module.sample_texts[0] if lang_module.sample_texts else ""

# ──────────────────── Main Content ───────────────────
col_input, col_output = st.columns([1, 1], gap="large")

with col_input:
    st.markdown("### 📥 Input")

    selected_lang_name = st.selectbox(
        "Select Language",
        list(LANGUAGE_NAMES.values()),
        index=0,
        help="Choose a language or auto-detect from text",
    )

    # Show all sample texts for the selected language
    selected_code = [c for c, n in LANGUAGE_NAMES.items() if n == selected_lang_name][0]
    selected_module = LANGUAGE_REGISTRY[selected_code]

    sample_selector = st.selectbox(
        "Sample Text",
        ["Custom input"] + selected_module.sample_texts,
        index=1,
    )

    default_text = "" if sample_selector == "Custom input" else sample_selector
    input_text = st.text_area(
        "Enter your request",
        value=default_text,
        height=120,
        placeholder="Type or select a sample text...",
    )

    analyze_btn = st.button(
        "🚀 ANALYZE (8-Agent MCP Pipeline)",
        type="primary",
        use_container_width=True,
    )

with col_output:
    st.markdown("### 📤 Decision Output")

    if analyze_btn and input_text.strip():
        context = {
            "customer_type": customer_type,
            "interaction_count": interaction_count,
            "severity_score": severity_score,
        }

        with st.spinner("Running 8-agent MCP pipeline..."):
            try:
                mcp = MCPOrchestrator()
                result = mcp.process(input_text, context)

                # Urgency-based styling
                urgency_class = f"urgency-{result.urgency.lower()}"
                urgency_emoji = {"HIGH": "🔥", "MEDIUM": "⚠️", "LOW": "✅"}.get(result.urgency, "ℹ️")
                action_emoji = {
                    "RESOLVE_TIER1": "✅",
                    "ESCALATE_TO_TIER2": "⬆️",
                    "ESCALATE_TO_TIER3": "🚨",
                    "EMERGENCY": "🆘",
                }.get(result.action, "📌")

                # Main result card
                st.markdown(f"""
                <div class="result-card {urgency_class}">
                    <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                        <div class="metric-badge">
                            {urgency_emoji} <strong>URGENCY:</strong> {result.urgency} ({result.confidence:.0%})
                        </div>
                        <div class="metric-badge">
                            {action_emoji} <strong>ACTION:</strong> {result.action}
                        </div>
                        <div class="metric-badge">
                            ⏱️ <strong>TIME:</strong> {result.processing_time_ms:.0f}ms
                        </div>
                        <div class="metric-badge">
                            🌐 <strong>LANG:</strong> {LANGUAGE_NAMES.get(result.language, result.language)}
                        </div>
                        <div class="metric-badge">
                            🔗 <strong>ID:</strong> {result.audit_id}
                        </div>
                    </div>
                    <div style="margin-top: 1rem; padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 8px;">
                        📝 {result.explanation}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # SLA status
                sla_color = "🟢" if result.sla_compliant else "🔴"
                st.markdown(f"{sla_color} **SLA:** {'Compliant' if result.sla_compliant else 'Violation'} (<2s target) | Response SLA: {result.sla_hours}h")

                # Reasons
                if result.reasons:
                    st.markdown("**📋 Business Rules Applied:**")
                    for reason in result.reasons:
                        st.markdown(f"  - {reason}")

                # Agent trace (collapsible)
                with st.expander("🔬 Agent Pipeline Trace (8 agents)", expanded=False):
                    for step in result.agent_trace:
                        agent = step["agent"]
                        t = step["time_ms"]
                        emoji_map = {
                            "LANG_DETECTOR": "🔍",
                            "NLP_AGENT": "📝",
                            "FEATURE_AGENT": "⚙️",
                            "ML_PREDICTOR": "🤖",
                            "RULE_AGENT": "📋",
                            "EXPLAIN_AGENT": "💡",
                            "ACTION_AGENT": "🎯",
                            "AUDIT_AGENT": "📊",
                        }
                        emoji = emoji_map.get(agent, "▶️")
                        st.markdown(f"""
                        <div class="agent-trace">
                            {emoji} <strong>{agent}</strong>
                            <span style="float:right; color: #667eea;">{t:.1f}ms</span>
                            <br><small style="opacity:0.7;">{json.dumps(step['output'], ensure_ascii=False, indent=None)}</small>
                        </div>
                        """, unsafe_allow_html=True)

            except FileNotFoundError as e:
                st.error(f"⚠️ {e}\n\nRun `python train_model.py` first to train the model.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    elif analyze_btn:
        st.warning("Please enter some text to analyze.")
    else:
        st.info("👈 Configure context in the sidebar, enter text, and click **ANALYZE**.")

# ──────────────────── Audit Log Section ──────────────
st.markdown("---")
st.markdown("### 📊 Audit Log & Analytics")

tab_recent, tab_stats = st.tabs(["📋 Recent Decisions", "📈 Statistics"])

with tab_recent:
    try:
        audit = AuditAgent()
        recent = audit.get_recent(limit=15)
        if recent:
            import pandas as pd
            df = pd.DataFrame(recent)
            display_cols = [
                "audit_id", "timestamp", "language", "urgency",
                "action", "confidence", "processing_ms",
            ]
            available = [c for c in display_cols if c in df.columns]
            st.dataframe(
                df[available],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No decisions logged yet. Analyze some text to populate the audit log.")
    except Exception as e:
        st.info("Audit log will appear here after your first analysis.")

with tab_stats:
    try:
        audit = AuditAgent()
        stats = audit.get_stats()
        if stats["total_decisions"] > 0:
            scol1, scol2, scol3 = st.columns(3)
            with scol1:
                st.metric("Total Decisions", stats["total_decisions"])
            with scol2:
                st.metric("Avg Confidence", f"{stats['avg_confidence']:.1%}")
            with scol3:
                st.metric("Languages Used", len(stats["by_language"]))

            lcol1, lcol2 = st.columns(2)
            with lcol1:
                st.markdown("**By Language:**")
                for lang, count in stats["by_language"].items():
                    name = LANGUAGE_NAMES.get(lang, lang)
                    st.markdown(f"- {name}: **{count}**")
            with lcol2:
                st.markdown("**By Urgency:**")
                for urg, count in stats["by_urgency"].items():
                    emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(urg, "⚪")
                    st.markdown(f"- {emoji} {urg}: **{count}**")
        else:
            st.info("Statistics will appear after your first analysis.")
    except Exception:
        st.info("Statistics will appear after your first analysis.")

# ──────────────────── Footer ─────────────────────────
st.markdown("---")
st.markdown(
    '<div style="text-align:center; opacity:0.5; font-size:0.8rem;">'
    '🌐 Multi-Language AI Decision System • 8 Languages • 8 Agents • MCP Pipeline<br>'
    'Enterprise-Grade Decision Automation for Indian Languages'
    '</div>',
    unsafe_allow_html=True,
)
