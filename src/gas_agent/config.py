"""Configuration for LangGraph search agent."""

from gas_agent.references import GAS_SUPPLIERS, SAFETY_STANDARDS, REGULATORY_BODIES
from gas_agent.graph_state import TierName

TIERS = {
    "suppliers": GAS_SUPPLIERS,
    "standards": SAFETY_STANDARDS,
    "regulatory": REGULATORY_BODIES,
    "open_web": None,
}

TIER_ORDER: list[TierName] = ["suppliers", "standards", "regulatory", "open_web"]

DEFAULT_CONFIG = {
    "confidence_threshold": 0.3,  # Accept lower confidence answers
    "overwrite_delta": 0.2,
    "max_snippet_chars": 1500,
    "max_results_per_search": 5,
    "enable_open_web_fallback": True,
}
