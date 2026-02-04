"""Gas agent: HMIS chemical gas table enrichment via LLM + web search."""

from gas_agent.schema import HMISGasRecord
from gas_agent.loader import load_hmis_excel
from gas_agent.graph_agent import fill_record_with_graph
from gas_agent.graph import build_search_graph
from gas_agent.pipeline import run_pipeline

__all__ = [
    "HMISGasRecord",
    "load_hmis_excel",
    "fill_record_with_graph",
    "build_search_graph",
    "run_pipeline",
]
