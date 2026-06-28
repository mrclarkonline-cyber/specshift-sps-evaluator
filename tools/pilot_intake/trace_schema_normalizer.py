#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

NORMALIZED_FIELDS = [
    "trace_id",
    "timestamp",
    "actor_system",
    "step_action",
    "input_context",
    "claimed_output",
    "final_state",
    "observable_evidence",
    "notes",
]

FIELD_ALIASES = {
    "trace_id": [
        "trace_id", "id", "record_id", "case_id", "workflow_id", "event_id", "ticket_id"
    ],
    "timestamp": [
        "timestamp", "time", "event_time", "created_at", "date", "datetime", "sequence_time"
    ],
    "actor_system": [
        "actor_system", "actor", "system", "user", "agent", "service", "component", "actor_id", "system_id"
    ],
    "step_action": [
        "step_action", "step", "action", "event", "event_type", "operation", "state_transition", "activity"
    ],
    "input_context": [
        "input_context", "input", "context", "trigger", "request", "prompt_summary", "visible_input"
    ],
    "claimed_output": [
        "claimed_output", "output", "response", "result", "visible_output", "claimed_result"
    ],
    "final_state": [
        "final_state", "claimed_final_state", "status", "completion_status", "ledger_state", "payment_status"
    ],
    "observable_evidence": [
        "observable_evidence", "evidence", "trace_reference", "log_reference", "source_row", "supporting_record"
    ],
    "notes": [
        "notes", "note", "comments", "comment", "limitation", "review_note"
    ],
}

BOUNDARY = (
    "Trace schema normalization only. This converts accepted observable trace artifacts into a standard review shape. "
    "It does not create legal advice, financial advice, binding terms, compliance certification, production validation, "
    "automated verdicts, free-pilot commitments, autonomous client action, truth validation, or hidden-mechanism claims."
)

def normalize_key(key: str) -> str:
    return key.strip().lower().replace(" ", "_").replace("-", "_")

def alias_map(input_keys: list[str]) -> dict[str, str]:
    normalized_input = {normalize_key(k): k for k in input_keys}
    mapping: dict[str, str] = {}

    for canonical, aliases in FIELD_ALIASES.items():
        for alias in aliases:
            alias_norm = normalize_key(alias)
            if alias_norm in normalized_input:
                mapping[canonical] = normalized_input[alias_norm]
                break

    return mapping

def normalize_row(row: dict[str, Any], mapping: dict[str, str], row_index: int) -> dict[str, str]:
    normalized: dict[str, str] = {}
    for field in NORMALIZED_FIELDS:
        source_key = mapping.get(field)
        value = row.get(source_key, "") if source_key else ""
        if value is None:
            value = ""
        normalized[field] = str(value)

    if not normalized["trace_id"]:
        normalized["trace_id"] = f"trace-row-{row_index:06d}"

    if not normalized["observable_evidence"]:
        normalized["observable_evidence"] = f"source_row:{row_index}"

    return normalized

def load_rows(input_path: Path) -> list[dict[str, Any]]:
    suffix = input_path.suffix.lower()

    if suffix == ".csv":
        with input_path.open("r", encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))

    if suffix == ".jsonl":
        rows = []
        for line in input_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                obj = json.loads(line)
                if not isinstance(obj, dict):
                    raise ValueError("JSONL rows must be objects")
                rows.append(obj)
        return rows

    if suffix == ".json":
        data = json.loads(input_path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and isinstance(data.get("rows"), list):
            return data["rows"]
        raise ValueError("JSON input must be a list of objects or {'rows': [...]}")

    raise ValueError(f"Unsupported input suffix: {suffix}")

def write_rows(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    suffix = output_path.suffix.lower()

    if suffix == ".csv":
        with output_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=NORMALIZED_FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        return

    if suffix == ".json" or suffix == ".jsonl":
        if suffix == ".jsonl":
            output_path.write_text(
                "\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in rows) + "\n",
                encoding="utf-8",
            )
        else:
            output_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return

    raise ValueError(f"Unsupported output suffix: {suffix}")

def normalize_file(input_path: Path, output_path: Path) -> dict[str, Any]:
    rows = load_rows(input_path)
    input_keys = list(rows[0].keys()) if rows else []
    mapping = alias_map(input_keys)
    normalized_rows = [normalize_row(row, mapping, i + 1) for i, row in enumerate(rows)]
    write_rows(normalized_rows, output_path)

    missing_canonical_fields = [field for field in NORMALIZED_FIELDS if field not in mapping and field not in {"trace_id", "observable_evidence"}]

    return {
        "engine": "trace_schema_normalizer_v1",
        "normalized_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_path": str(input_path),
        "output_path": str(output_path),
        "rows_in": len(rows),
        "rows_out": len(normalized_rows),
        "canonical_fields": NORMALIZED_FIELDS,
        "field_mapping": mapping,
        "missing_canonical_fields": missing_canonical_fields,
        "claim_boundary": BOUNDARY,
    }

def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize accepted observable trace artifacts into SpecShift review shape.")
    parser.add_argument("--input", required=True, help="Input CSV, JSON, or JSONL file")
    parser.add_argument("--output", required=True, help="Output CSV, JSON, or JSONL file")
    parser.add_argument("--report", default="", help="Optional JSON report path")
    args = parser.parse_args()

    report = normalize_file(Path(args.input), Path(args.output))

    print("Trace Schema Normalizer")
    print("=" * 72)
    print(f"input:    {report['input_path']}")
    print(f"output:   {report['output_path']}")
    print(f"rows in:  {report['rows_in']}")
    print(f"rows out: {report['rows_out']}")
    print()
    print("Field mapping:")
    for field in NORMALIZED_FIELDS:
        print(f"  - {field}: {report['field_mapping'].get(field, 'MISSING')}")

    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print()
        print(f"Report: {report_path}")

    print()
    print(f"Boundary: {BOUNDARY}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
