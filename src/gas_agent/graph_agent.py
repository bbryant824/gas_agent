"""Main entry point for LangGraph search agent."""

import logging

from gas_agent.schema import HMISGasRecord, get_empty_field_names
from gas_agent.graph_state import SearchState
from gas_agent.config import TIERS
from gas_agent.graph import build_search_graph

logger = logging.getLogger(__name__)


def fill_record_with_graph(
    record: HMISGasRecord,
    *,
    llm=None,
    search_tool=None,
    confidence_threshold: float = 0.6,
    overwrite_delta: float = 0.2,
    max_snippet_chars: int = 1500,
    max_results_per_search: int = 5,
    enable_open_web_fallback: bool = True,
) -> HMISGasRecord:
    """Fill empty fields using 2-phase LangGraph pipeline."""
    from langchain_openai import ChatOpenAI
    from langchain_tavily import TavilySearch
    
    empty_fields = get_empty_field_names(record)
    if not empty_fields:
        logger.info("No empty fields")
        return record
    
    logger.info(f"Starting pipeline: {len(empty_fields)} empty fields")
    
    # Create tools once (reused across all nodes)
    llm = llm or ChatOpenAI(model="gpt-4o-mini", temperature=0)
    search_tool = search_tool or TavilySearch(max_results=max_results_per_search)
    
    initial_state: SearchState = {
        "record": record,
        "current_record": HMISGasRecord(**record.model_dump()),
        "pending_fields": empty_fields.copy(),
        "filled_fields": {},
        "tier": "suppliers",
        "tier_index": 0,
        "general_search_count": 0,
        "search_results": {},
        "config": {
            "confidence_threshold": confidence_threshold,
            "overwrite_delta": overwrite_delta,
            "max_snippet_chars": max_snippet_chars,
            "max_results_per_search": max_results_per_search,
            "enable_open_web_fallback": enable_open_web_fallback,
        },
        "llm": llm,
        "search_tool": search_tool,
        "_next": "search_tier",
    }
    
    graph = build_search_graph()
    final_state = graph.invoke(initial_state)
    
    # Summary
    filled = len(final_state["filled_fields"])
    pending = len(final_state["pending_fields"])
    tier_filled = sum(1 for f in final_state["filled_fields"].values() if f.get("tier") in TIERS)
    general_filled = sum(1 for f in final_state["filled_fields"].values() if f.get("tier") == "general")
    
    logger.info(f"✓ Pipeline complete: {filled} filled ({tier_filled} tier, {general_filled} general), {pending} unfilled")
    
    return final_state["current_record"]
