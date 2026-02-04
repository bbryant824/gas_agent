"""LangGraph nodes for search and extraction."""

import logging

from langchain_core.messages import SystemMessage, HumanMessage

from gas_agent.schema import HMISGasRecord, FIELD_TO_DESCRIPTION
from gas_agent.graph_state import SearchState
from gas_agent.config import TIERS, TIER_ORDER
from gas_agent.prompts import EXTRACTION_SYSTEM_PROMPT, build_extraction_prompt
from gas_agent.utils import (
    normalize_search_results,
    parse_json_response,
    build_context_from_results,
    should_update_field,
)

logger = logging.getLogger(__name__)


def search_tier_node(state: SearchState) -> dict:
    """Perform Tavily search for current tier."""
    tier = state["tier"]
    record = state["record"]
    search_tool = state["search_tool"]
    
    chemical = record.chemical_name or record.sub_system_filter_formula or "chemical"
    domains = TIERS[tier]
    
    query = f"{chemical} safety data sheet properties hazards" if domains else f"{chemical} SDS MSDS"
    logger.info(f"🔍 {tier}: {chemical}")
    
    search_params = {"query": query}
    if domains:
        search_params["include_domains"] = domains[:10]
    
    try:
        results = search_tool.invoke(search_params)
        search_results = state["search_results"].copy()
        search_results[tier] = normalize_search_results(results)
        
        num = len(search_results[tier].get('results', []))
        logger.info(f"✓ {num} results")
        return {"search_results": search_results}
    except Exception as e:
        logger.warning(f"✗ Search failed: {e}")
        search_results = state["search_results"].copy()
        search_results[tier] = {"results": []}
        return {"search_results": search_results}


def extract_fields_node(state: SearchState) -> dict:
    """Extract field values from tier search results."""
    tier = state["tier"]
    record = state["record"]
    current_record = state["current_record"]
    config = state["config"]
    llm = state["llm"]
    
    target_fields = state["pending_fields"]
    if not target_fields:
        return {}
    
    search_data = state["search_results"].get(tier, {})
    results = search_data.get("results", [])
    
    if not results:
        logger.info(f"ℹ️  No results")
        return {}
    
    # Build context and prompt
    context = build_context_from_results(
        results,
        config["max_results_per_search"],
        config["max_snippet_chars"]
    )
    
    chemical = record.chemical_name or record.sub_system_filter_formula or "chemical"
    prompt = build_extraction_prompt(chemical, target_fields, context)
    
    try:
        response = llm.invoke([
            SystemMessage(content=EXTRACTION_SYSTEM_PROMPT),
            HumanMessage(content=prompt)
        ])
        
        data = parse_json_response((response.content or "").strip())
        if not data:
            return {}
        
        updates = data.get("updates", [])
        
        # Apply updates
        new_record_data = current_record.model_dump()
        filled = state["filled_fields"].copy()
        pending = state["pending_fields"].copy()
        
        filled_count = 0
        for upd in updates:
            field = upd.get("field")
            value = upd.get("value", "").strip()
            confidence = upd.get("confidence", 0.5)
            source_url = upd.get("source_url")
            
            if not field or not value or "UNKNOWN" in value.upper() or field not in target_fields:
                continue
            
            if should_update_field(field, confidence, filled, config):
                new_record_data[field] = value
                filled[field] = {
                    "value": value,
                    "confidence": confidence,
                    "source_url": source_url,
                    "tier": tier
                }
                if field in pending:
                    pending.remove(field)
                filled_count += 1
        
        logger.info(f"✓ {filled_count} filled, {len(pending)} pending")
        
        return {
            "current_record": HMISGasRecord(**new_record_data),
            "filled_fields": filled,
            "pending_fields": pending,
        }
    
    except Exception as e:
        logger.warning(f"✗ Extraction failed: {e}")
        return {}


def search_general_node(state: SearchState) -> dict:
    """Perform general web search for remaining fields."""
    pending = state["pending_fields"]
    search_count = state["general_search_count"]
    search_tool = state["search_tool"]
    record = state["record"]
    
    if not pending or search_count >= 3:
        return {}
    
    chemical = record.chemical_name or record.sub_system_filter_formula or "chemical"
    
    # Build query from top pending fields
    field_terms = " ".join([FIELD_TO_DESCRIPTION.get(f, f).split()[0] for f in pending[:5]])
    query = f"{chemical} chemical properties {field_terms} SDS"
    
    logger.info(f"🔍 General {search_count + 1}/3")
    
    try:
        results = search_tool.invoke({"query": query})
        search_results = state["search_results"].copy()
        search_results[f"general_{search_count}"] = normalize_search_results(results)
        
        return {
            "search_results": search_results,
            "general_search_count": search_count + 1,
        }
    except Exception as e:
        logger.warning(f"✗ Search failed: {e}")
        return {"general_search_count": search_count + 1}


def extract_general_node(state: SearchState) -> dict:
    """Extract remaining fields from general search (mark as review required)."""
    pending = state["pending_fields"]
    search_count = state["general_search_count"]
    llm = state["llm"]
    record = state["record"]
    current_record = state["current_record"]
    
    if not pending or search_count == 0:
        return {}
    
    tier_key = f"general_{search_count - 1}"
    search_data = state["search_results"].get(tier_key, {})
    results = search_data.get("results", [])
    
    # Build context (use what's available, even if empty)
    context_parts = []
    if results:
        for r in results[:5]:
            if isinstance(r, dict):
                content = r.get("content", "")[:800]
                if content:
                    context_parts.append(content)
    
    context = "\n\n".join(context_parts)[:3000] if context_parts else "No search results available. Provide estimates based on chemical knowledge."
    
    chemical = record.chemical_name or record.sub_system_filter_formula or "chemical"
    prompt = build_extraction_prompt(chemical, pending[:20], context, is_general=True)
    
    try:
        response = llm.invoke([
            SystemMessage(content=EXTRACTION_SYSTEM_PROMPT),
            HumanMessage(content=prompt)
        ])
        
        data = parse_json_response((response.content or "").strip())
        if not data:
            return {}
        
        updates = data.get("updates", [])
        
        new_record_data = current_record.model_dump()
        filled = state["filled_fields"].copy()
        new_pending = state["pending_fields"].copy()
        
        for upd in updates:
            field = upd.get("field")
            value = upd.get("value", "").strip()
            confidence = upd.get("confidence", 0.2)
            
            # Accept ANY value for general search (final pass)
            if field in pending and value and value.upper() not in ["NULL", "NONE", ""]:
                # Mark with (review required) for low confidence or no search results
                if confidence < 0.4 or not results:
                    labeled_value = f"{value} (review required)"
                else:
                    labeled_value = value
                    
                new_record_data[field] = labeled_value
                filled[field] = {
                    "value": labeled_value,
                    "confidence": confidence,
                    "source_url": None,
                    "tier": "general"
                }
                if field in new_pending:
                    new_pending.remove(field)
        
        return {
            "current_record": HMISGasRecord(**new_record_data),
            "filled_fields": filled,
            "pending_fields": new_pending,
        }
    except Exception as e:
        logger.warning(f"✗ Extraction failed: {e}")
    
    return {}


def router_node(state: SearchState) -> dict:
    """Route between tier searches, general searches, and end."""
    tier_index = state["tier_index"]
    pending = state["pending_fields"]
    search_count = state["general_search_count"]
    config = state["config"]
    
    max_tier = 3 if config["enable_open_web_fallback"] else 2
    
    # Phase 1: Tier searches
    if tier_index < max_tier:
        new_tier_index = tier_index + 1
        new_tier = TIER_ORDER[new_tier_index]
        return {"tier_index": new_tier_index, "tier": new_tier, "_next": "search_tier"}
    
    # Phase 2: General searches (max 3)
    if pending and search_count < 3:
        return {"_next": "search_general"}
    
    # Done
    logger.info(f"✓ Complete")
    return {"_next": "end"}
