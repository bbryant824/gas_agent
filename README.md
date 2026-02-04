# Gas Agent — HMIS Chemical Gas Table Filler

Fill HMIS (Hazardous Materials Identification System) chemical gas table cells using **LangGraph**, **ChatOpenAI**, and **Tavily** web search. The pipeline reads an Excel sheet (rows = gases, columns = properties and industry standards), maps it to a structured schema, and uses a 3-phase search agent to fill ALL cells.

**NEW**: **3-Phase LangGraph Pipeline** with guaranteed complete data:
- ✅ **Zero blank fields** (tier → field → estimation fallback)
- ✅ **68% fewer API calls** (~29 vs 90 for full field coverage)
- ✅ **Transparent labeling** ("(estimated)" suffix for LLM guesses)
- ✅ **Cost controlled** (max 10 individual field searches)
- ✅ **Single unified workflow** for complete tracking

## Pipeline Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────────────────┐
│  HMIS TABLE     │     │  Structured      │     │  For each record:           │
│  (Excel)        │ ──► │  Schema           │ ──► │  LangGraph Multi-Tier       │
│  Rows = gases   │     │  (HMISGasRecord)  │     │  Search Agent (3-4 passes)  │
│  Cols = props   │     │  47 fields       │     │  → Fill all empty cells     │
└─────────────────┘     └──────────────────┘     └─────────────────────────────┘
```

1. **Load** — Read Excel (`docs/HMIS TABLE.xlsx`), first row = header, data rows → `HMISGasRecord` (Pydantic).
2. **Schema** — Each row is a `HMISGasRecord` with 47 optional string fields (chemical name, CAS number, flammability, GHS codes, etc.).
3. **Fill** — **3-Phase LangGraph Pipeline**:
   - **Phase 1**: Tier searches (suppliers → standards → regulatory → open web) → Batch extract all fields
   - **Phase 2**: Individual field searches (max 10) → Fill most common missing fields
   - **Phase 3**: LLM estimation → Fill ALL remaining with "(estimated)" label
   - **Total**: ~14-24 Tavily + ~15-19 LLM calls per record (vs. 90 in old version)
   - **Result**: 100% field coverage, zero blanks
4. **Export** — Write filled records back to Excel (same column order).

## Requirements

- **Python 3.11+**
- **OpenAI API key** — for ChatOpenAI (e.g. `gpt-4o-mini`).
- **Tavily API key** — for web search ([tavily.com](https://tavily.com)).

Set in environment or `.env`:

```bash
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
```

## Authoritative Reference Sources

The agent **prioritizes trusted sources** for accuracy:
- **Gas Suppliers**: Air Liquide, Merck, Matheson, Linde, PraxAir
- **Safety Standards**: OSHA, NIOSH, NFPA, GHS, CGA
- **Regulatory Bodies**: IBC/IFC, EPA, ECHA

See [REFERENCES_INTEGRATION.md](docs/REFERENCES_INTEGRATION.md) for details.

## Install

```bash
uv sync
# or: pip install -e .
```

## Usage

### CLI (Simple!)

```bash
# Default: Fill entire table (197 rows, ~4-5 hours)
# Input:  docs/HMIS TABLE.xlsx
# Output: docs/HMIS_filled.xlsx
uv run gas-agent

# Dry run: Test with first 5 rows (with LLM/search, ~3-5 minutes)
uv run gas-agent --dryrun
```

That's it! No complex arguments needed.

### Python API (Advanced Use)

```python
from gas_agent import run_pipeline

# Full run (all rows)
records = run_pipeline(
    "docs/HMIS TABLE.xlsx",
    output_path="docs/HMIS_filled.xlsx"
)

# Test run (first 5 rows with LLM)
records = run_pipeline(
    "docs/HMIS TABLE.xlsx",
    output_path="docs/HMIS_test.xlsx",
    max_rows=5
)

# Custom limits for testing
records = run_pipeline(
    "docs/HMIS TABLE.xlsx",
    output_path="docs/HMIS_test.xlsx",
    max_rows=10,
    max_fields_per_row=3,  # Fill only 3 fields per row
    use_trusted_domains=True  # Default
)
```

## Project Layout

| Path | Role |
|------|------|
| `src/gas_agent/schema.py` | Pydantic `HMISGasRecord`, column spec, helpers (`get_empty_field_names`) |
| `src/gas_agent/references.py` | Authoritative source domains (suppliers, standards, regulatory) |
| `src/gas_agent/loader.py` | `load_hmis_excel()` — Excel → list of `HMISGasRecord` |
| `src/gas_agent/agent.py` | `fill_one_field_with_search()`, `fill_record_with_agent()` — Tavily + ChatOpenAI |
| `src/gas_agent/export.py` | `export_records_to_excel()` — write records to Excel |
| `src/gas_agent/pipeline.py` | `run_pipeline()` — load → fill → export |
| `src/gas_agent/main.py` | CLI entrypoint (`gas-agent`) |

## Implementation Notes

- **Schema**: Column indices 0–46 map to `HMISGasRecord` fields (see `HMIS_COLUMN_SPEC` in `schema.py`). All fields are `Optional[str]` so empty Excel cells become `None`.
- **References**: Prioritizes searches from trusted domains organized in tiers: (1) Gas suppliers, (2) Safety standards, (3) Regulatory bodies, (4) Open web fallback.
- **Agent**: **NEW LangGraph multi-tier search** — 3-4 searches per record (not per field), structured extraction with confidence scoring. See `graph_agent.py`.
- **Performance**: For 197 rows, **~590-788 API calls total** (vs. ~8,668 in old version), **~33-50 minutes** (vs ~4.8 hours), **~$1.38** (vs ~$9.37).
- **Tavily**: Uses `langchain_tavily.TavilySearch` with `include_domains` for tier-specific filtering.
- **LLM**: `ChatOpenAI(model="gpt-4o-mini", temperature=0)` with structured JSON output for batch field extraction.

## Dependencies (pyproject.toml)

- `langchain`, `langchain-openai`, `langchain-tavily`, `langgraph`
- `openpyxl` — Excel read/write
- `python-dotenv` — env loading

## Documentation

- **README.md** — Quick start (this file)
- **docs/REFERENCES_INTEGRATION.md** — Authoritative source integration details
- **docs/ARCHITECTURE.md** — Deep dive: design, cost, optimizations
- **docs/FLOW_DIAGRAM.md** — Visual diagrams
- **docs/IMPLEMENTATION_GUIDE.md** — Step-by-step guide
- **docs/SUMMARY.md** — One-page reference
