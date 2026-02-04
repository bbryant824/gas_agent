# Quick Start — HMIS Gas Agent

## ⚡ Super Simple Usage

### 1. Set API Keys
```bash
export OPENAI_API_KEY=sk-...
export TAVILY_API_KEY=tvly-...
```

### 2. Run!

**Test Mode** (First 5 rows with LLM/search):
```bash
uv run gas-agent --dryrun
```

**Full Run** (All 197 rows):
```bash
uv run gas-agent
```

That's it! 🎉

---

## What Happens

### Dry Run (`--dryrun`)
- ✅ Reads `docs/HMIS TABLE.xlsx`
- ✅ Processes **first 5 rows only**
- ✅ **Uses LLM + web search** to fill empty cells (real test!)
- ✅ Prioritizes **authoritative sources** (suppliers, standards)
- ✅ Outputs `docs/HMIS_filled.xlsx`
- ⏱️ Takes ~3-5 minutes (5 rows × ~44 fields × 2 sec)
- 💰 Costs ~$0.25

### Full Run (default)
- ✅ Reads `docs/HMIS TABLE.xlsx`
- ✅ Processes **all 197 rows**
- ✅ Uses **LLM + web search** to fill empty cells
- ✅ Prioritizes **authoritative sources** (suppliers, standards)
- ✅ Outputs `docs/HMIS_filled.xlsx`
- ⏱️ Takes ~4-5 hours
- 💰 Costs ~$9.37

---

## Files

**Input**: `docs/HMIS TABLE.xlsx` (must exist)  
**Output**: `docs/HMIS_filled.xlsx` (auto-created)

---

## No Complex Options!

The CLI is intentionally simple. If you need advanced options (custom paths, field limits, etc.), use the Python API:

```python
from gas_agent import run_pipeline

records = run_pipeline(
    "path/to/input.xlsx",
    output_path="path/to/output.xlsx",
    max_rows=10,  # Limit for testing
    max_fields_per_row=5,  # Limit fields per row
)
```

See [README.md](README.md) for full Python API documentation.
