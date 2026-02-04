"""Prompts for LLM extraction."""

from gas_agent.schema import FIELD_TO_DESCRIPTION

EXTRACTION_SYSTEM_PROMPT = """You are an expert in chemical safety and HMIS data extraction.

Extract field values from web search results. Output ONLY valid JSON.

Format:
{"updates": [{"field": "field_name", "value": "extracted value", "confidence": 0.0-1.0, "source_url": "url or null"}]}

Confidence scoring:
- 0.9-1.0: Multiple authoritative sources agree
- 0.7-0.9: One clear authoritative source
- 0.5-0.7: Source found but ambiguous
- 0.3-0.5: Reasonable estimate based on chemical properties
- 0.1-0.3: Best guess when no data available

Rules:
- Extract values found in search results with appropriate confidence
- Provide reasonable estimates when direct data unavailable
- Keep values concise (word/phrase/number+unit)
- ALWAYS provide a value, even if confidence is low"""


def build_extraction_prompt(chemical: str, fields: list[str], context: str, is_general: bool = False) -> str:
    """Build user prompt for LLM extraction."""
    field_descs = "\n".join([f"- {f}: {FIELD_TO_DESCRIPTION.get(f, f)}" for f in fields[:30]])
    
    if is_general:
        instruction = """IMPORTANT: These are remaining unfilled fields. You MUST provide a value for each field.
- If found in search results: extract with appropriate confidence
- If not found: provide your best estimate based on chemical properties/knowledge
- Mark uncertain estimates with lower confidence (0.1-0.4)
- NEVER leave a field without a value

Fields to fill:"""
    else:
        instruction = "Fields to extract:"
    
    return f"""Chemical: {chemical}

{instruction}
{field_descs}

Search results:
{context}

Extract or estimate ALL field values. Output JSON only."""
