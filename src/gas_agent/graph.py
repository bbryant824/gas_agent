"""LangGraph workflow construction."""

from langgraph.graph import StateGraph, END

from gas_agent.graph_state import SearchState
from gas_agent.nodes import (
    search_tier_node,
    extract_fields_node,
    search_general_node,
    extract_general_node,
    router_node,
)


def build_search_graph() -> StateGraph:
    """Build 2-phase LangGraph: tier searches → general searches."""
    workflow = StateGraph(SearchState)
    
    # Add nodes
    workflow.add_node("search_tier", search_tier_node)
    workflow.add_node("extract_tier", extract_fields_node)
    workflow.add_node("search_general", search_general_node)
    workflow.add_node("extract_general", extract_general_node)
    workflow.add_node("router", router_node)
    
    # Set entry
    workflow.set_entry_point("search_tier")
    
    # Add edges
    workflow.add_edge("search_tier", "extract_tier")
    workflow.add_edge("extract_tier", "router")
    workflow.add_edge("search_general", "extract_general")
    workflow.add_edge("extract_general", "router")
    
    # Router conditional routing
    workflow.add_conditional_edges(
        "router",
        lambda state: state.get("_next", "end"),
        {
            "search_tier": "search_tier",
            "search_general": "search_general",
            "end": END
        }
    )
    
    return workflow.compile()
