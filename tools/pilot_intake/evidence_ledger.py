#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

BOUNDARY = "Evidence ledger only. No legal advice, financial advice, binding terms, compliance certification, production validation, automated verdict, free pilot commitment, autonomous client action, truth validation, or hidden-mechanism claim."

VALID_EVENTS = {
    "artifact_received",
    "classification",
    "risk_decision",
    "route",
    "reviewer_output",
    "delivery_file",
    "buyer_label_reveal_status",
    "validation_result",
    "closeout_recommendation",
}

def file_hash(path: str) -> str:
    if not path:
        return ""
    p = Path(path)
    if not p.exists() or not p.is_file():
        return ""
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSONL at line {line_number}: {exc}")
    return rows

def append_record(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

def make_record(args) -> dict:
    if args.event_type not in VALID_EVENTS:
        raise SystemExit(f"Invalid event_type: {args.event_type}")

    event_time = datetime.now(timezone.utc).isoformat()
    seed = f"{args.project_id}|{args.event_type}|{args.artifact_id}|{event_time}"
    ledger_id = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]

    return {
        "ledger_id": ledger_id,
        "event_time_utc": event_time,
        "project_id": args.project_id,
        "event_type": args.event_type,
        "artifact_id": args.artifact_id,
        "artifact_path": args.artifact_path,
        "artifact_hash": file_hash(args.artifact_path),
        "classification": args.classification,
        "risk_decision": args.risk_decision,
        "route": args.route,
        "reviewer_output": args.reviewer_output,
        "delivery_file": args.delivery_file,
        "buyer_label_reveal_status": args.buyer_label_reveal_status,
        "validation_result": args.validation_result,
        "closeout_recommendation": args.closeout_recommendation,
        "notes": args.notes,
        "claim_boundary": BOUNDARY,
    }

def summarize(path: Path) -> dict:
    rows = read_rows(path)
    counts = {}
    for row in rows:
        event = row.get("event_type", "")
        counts[event] = counts.get(event, 0) + 1
    return {
        "ledger": str(path),
        "record_count": len(rows),
        "event_counts": counts,
        "claim_boundary": BOUNDARY,
    }

def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add")
    add.add_argument("--ledger", required=True)
    add.add_argument("--project-id", required=True)
    add.add_argument("--event-type", required=True)
    add.add_argument("--artifact-id", default="")
    add.add_argument("--artifact-path", default="")
    add.add_argument("--classification", default="")
    add.add_argument("--risk-decision", default="")
    add.add_argument("--route", default="")
    add.add_argument("--reviewer-output", default="")
    add.add_argument("--delivery-file", default="")
    add.add_argument("--buyer-label-reveal-status", default="")
    add.add_argument("--validation-result", default="")
    add.add_argument("--closeout-recommendation", default="")
    add.add_argument("--notes", default="")

    summary = sub.add_parser("summary")
    summary.add_argument("--ledger", required=True)
    summary.add_argument("--output", default="")

    args = parser.parse_args()

    if args.cmd == "add":
        record = make_record(args)
        append_record(Path(args.ledger), record)
        print(json.dumps(record, indent=2, sort_keys=True))
        return 0

    if args.cmd == "summary":
        result = summarize(Path(args.ledger))
        if args.output:
            out = Path(args.output)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0

    return 1

if __name__ == "__main__":
    raise SystemExit(main())
