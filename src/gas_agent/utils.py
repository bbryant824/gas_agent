"""Utility functions for search agent."""

import json
import logging

logger = logging.getLogger(__name__)


def normalize_search_results(results) -> dict:
    """Normalize Tavily search results to dict format."""
    if isinstance(results, dict):
        return results
    elif isinstance(results, list):
        return {"results": results}
    else:
        return {"results": []}


def parse_json_response(text: str) -> dict:
    """Parse JSON from LLM response, handling markdown wrapping."""
    start = text.find("{")
    end = text.rfind("}") + 1
    
    if start < 0 or end <= start:
        return {}
    
    try:
        return json.loads(text[start:end])
    except json.JSONDecodeError as e:
        logger.warning(f"JSON parse error: {e}")
        return {}


def build_context_from_results(results: list, max_results: int, max_chars: int) -> str:
    """Build context string from search results."""
    context_parts = []
    for r in results[:max_results]:
        if isinstance(r, dict):
            content = r.get("content", "")
            url = r.get("url", "")
            snippet = content[:max_chars]
            context_parts.append(f"[{url}]\n{snippet}")
    
    return "\n\n---\n\n".join(context_parts)[:12000]


def should_update_field(field: str, new_confidence: float, filled_fields: dict, config: dict) -> bool:
    """Determine if a field should be updated based on confidence."""
    if field not in filled_fields:
        # Empty field - fill if confidence meets threshold
        return new_confidence >= config["confidence_threshold"]
    
    # Has value - only update if significantly better
    old_confidence = filled_fields[field].get("confidence", 0.0)
    return new_confidence >= old_confidence + config["overwrite_delta"]
