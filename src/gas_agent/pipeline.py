"""
Pipeline: load HMIS Excel → fill empty cells via LangGraph → export.
"""

from pathlib import Path

from gas_agent.loader import load_hmis_excel
from gas_agent.graph_agent import fill_record_with_graph
from gas_agent.schema import HMISGasRecord
from gas_agent.export import export_records_to_excel


def run_pipeline(
    input_path: str | Path,
    output_path: str | Path | None = None,
    *,
    sheet_name: str | None = None,
    max_rows: int | None = None,
    dry_run: bool = False,
) -> list[HMISGasRecord]:
    """
    Load HMIS Excel, fill empty cells using LangGraph pipeline, optionally export.

    Args:
        input_path: Path to HMIS TABLE.xlsx
        output_path: If set, write filled records to this Excel file
        sheet_name: Sheet to read (default: first sheet)
        max_rows: Process only this many rows (default: all)
        dry_run: If True, load and return records without calling LLM/search

    Returns:
        List of (possibly filled) HMISGasRecord
    """
    path = Path(input_path)
    records = load_hmis_excel(path, sheet_name=sheet_name)

    if max_rows is not None:
        records = records[:max_rows]

    if dry_run:
        if output_path:
            export_records_to_excel(records, output_path, original_path=path)
        return records

    filled: list[HMISGasRecord] = []
    for idx, record in enumerate(records, 1):
        print(f"Processing row {idx}/{len(records)}: {record.chemical_name or record.sub_system_filter_formula}")
        updated = fill_record_with_graph(record)
        filled.append(updated)

    if output_path:
        export_records_to_excel(filled, output_path, original_path=path)
    return filled
