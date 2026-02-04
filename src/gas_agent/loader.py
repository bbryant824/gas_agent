"""
Load HMIS chemical gas table from Excel and convert rows to HMISGasRecord.
"""

from pathlib import Path

import openpyxl

from gas_agent.schema import HMISGasRecord, COLUMN_INDEX_TO_FIELD


def _cell_to_str(cell: object) -> str | None:
    """Convert Excel cell value to string; None/blank -> None."""
    if cell is None:
        return None
    if isinstance(cell, str):
        s = cell.strip()
        return s if s else None
    if isinstance(cell, (int, float)):
        return str(cell).strip() or None
    return str(cell).strip() or None

def load_hmis_excel(
    path: str | Path,
    sheet_name: str | None = None,
    skip_header: bool = True,
) -> list[HMISGasRecord]:
    """
    Load HMIS table from Excel. First row is header; data rows become HMISGasRecord.
    """
    path = Path(path)
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet_name] if sheet_name else wb.active
    rows = list(ws.iter_rows(values_only=True))
    wb.close()

    if not rows:
        return []

    if skip_header:
        rows = rows[1:]

    records: list[HMISGasRecord] = []
    max_col = max(COLUMN_INDEX_TO_FIELD.keys(), default=0)

    for row in rows:
        values: dict[str, str | None] = {}
        for idx in range(max_col + 1):
            field = COLUMN_INDEX_TO_FIELD.get(idx)
            if not field:
                continue
            raw = row[idx] if idx < len(row) else None
            values[field] = _cell_to_str(raw)
        records.append(HMISGasRecord(**values))
    return records
