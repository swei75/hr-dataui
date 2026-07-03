"""Read .xlsx into dict[module_name, list[dict]]."""
from pathlib import Path
from typing import Any

import openpyxl


def read_workbook(path: Path | str) -> dict[str, list[dict[str, Any]]]:
    """读 .xlsx 全部 sheet（除 [配置] 外）→ dict[sheet_name, records]."""
    wb = openpyxl.load_workbook(path, data_only=True)
    result = {}
    for sheet_name in wb.sheetnames:
        if sheet_name == "配置":
            continue
        ws = wb[sheet_name]
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            result[sheet_name] = []
            continue
        headers = [
            str(h) if h is not None else f"col_{i}"
            for i, h in enumerate(rows[0])
        ]
        records = []
        for row in rows[1:]:
            if all(c is None or c == "" for c in row):
                continue
            record = {}
            for h, v in zip(headers, row):
                record[h] = v
            records.append(record)
        result[sheet_name] = records
    wb.close()
    return result


def read_config(path: Path | str) -> dict[str, Any]:
    """读 [配置] sheet → dict[key, value]."""
    wb = openpyxl.load_workbook(path, data_only=True)
    if "配置" not in wb.sheetnames:
        wb.close()
        return {}
    ws = wb["配置"]
    config = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None or row[0] == "":
            continue
        config[str(row[0])] = row[1] if len(row) > 1 else None
    wb.close()
    return config


def clean_value(v: Any, kind: str = "auto") -> Any:
    """清洗 Excel cell 值。
    - "pct": "25.86%" → 0.2586
    - "int": "5,901" → 5901
    - "float": "3.14" → 3.14
    - empty/None → None
    """
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return v
    s = str(v).strip()
    if not s:
        return None
    if kind == "pct":
        if s.endswith("%"):
            return float(s.rstrip("%")) / 100
        return float(s)
    if kind == "int":
        return int(s.replace(",", ""))
    if kind == "float":
        return float(s.replace(",", ""))
    return s
