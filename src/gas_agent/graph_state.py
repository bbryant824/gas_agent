"""
LangGraph state schema for tiered domain search.
"""

from typing import TypedDict, Literal, Any

from gas_agent.schema import HMISGasRecord


TierName = Literal["suppliers", "standards", "regulatory", "open_web"]


class SearchState(TypedDict):
    """LangGraph state for multi-tier record filling."""
    # Records
    record: HMISGasRecord
    current_record: HMISGasRecord
    
    # Field tracking
    pending_fields: list[str]
    filled_fields: dict[str, dict]  # field -> {value, confidence, source_url, tier}
    
    # Current tier/phase
    tier: TierName
    tier_index: int
    general_search_count: int  # Max 3 general searches for remaining
    
    # Search results
    search_results: dict[str, dict]
    
    # Config
    config: dict
    
    # Tools (created once, reused)
    llm: Any
    search_tool: Any
    
    # Router control
    _next: str  # "search_tier", "search_general", "end"
