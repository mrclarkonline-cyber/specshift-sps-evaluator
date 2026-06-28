#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

BOUNDARY = (
    "Label reconciliation only. It compares candidate-discrepancy memo categories against buyer-retained labels "
    "after buyer-controlled label reveal. It does not claim production validation, compliance certification, "
    "truth validation, automated verdicts, legal advice, financial advice, binding terms, or autonomous client action."
)

VALID_CATEGORIES = {
    "true_positive",
    "false_positive",
    "true_negative",
    "false_negative",
    "ambiguous",
    "out_of_scope",
    "label_unavailable",
}

def classify(candidate_flag: str, buyer_label: str) -> str:
    c = candidate_flag.strip().lower()
    b = buyer_label.strip().lower()

    if not b or b in {"unknown", "unavailable", "na", "n/a"}:
        return "label_unavailable"
    if b in {"ambiguous", "unclear", "mixed"}:
        return "ambiguous"
    if b in {"out_of_scope", "out of scope"}:
        return "out_of_scope"

    candidate_yes = c in {"1", "true", "yes", "flagged", "candidate", "positive"}
    label_yes = b in {"1", "true", "yes", "issue", "positive", "discrepancy"}

    if candidate_yes and label_yes:
        return "true_positive"
    if candidate_yes and not label_yes:
        return "false_positive"
    if not candidate_yes and not label_yes:
        return "true_negative"
    if not candidate_yes and label_yes:
        return "false_negative"
    return "ambiguous"

def read_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def reconcile(input_path: Path, output_path: Path) -> dict:
    rows = read_rows(input_path)
    out_rows = []
    counts = {k: 0 for k in sorted(VALID_CATEGORIES)}

    for i, row in enumerate(rows, start=1):
        category = classify(row.get("candidate_flag", ""), row.get("buyer_label", ""))
        counts[category] += 1
        out = dict(row)
        out["reconciliation_category"] = category
        out["reconciliation_note"] = "buyer-label comparison after buyer-controlled reveal"
        out_rows.append(out)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted(set().union(*(r.keys() for r in out_rows))) if out_rows else [
        "trace_id", "candidate_flag", "buyer_label", "reconciliation_category", "reconciliation_note"
    ]
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)

    report = {
        "engine": "label_reconciliation_v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_path": str(input_path),
        "output_path": str(output_path),
        "rows": len(rows),
        "category_counts": counts,
        "claim_boundary": BOUNDARY,
    }
    return report

def main() -> int:
    parser = argparse.ArgumentParser(description="Reconcile SpecShift candidate prompts against buyer-retained labels after reveal.")
    parser.add_argument("--input", required=True, help="CSV with trace_id,candidate_flag,buyer_label")
    parser.add_argument("--output", required=True, help="Output reconciliation CSV")
    parser.add_argument("--report", default="", help="Optional JSON report path")
    args = parser.parse_args()

    report = reconcile(Path(args.input), Path(args.output))

    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("Buyer Label Reconciliation")
    print("=" * 72)
    print(f"rows: {report['rows']}")
    for key, value in report["category_counts"].items():
        print(f"  - {key}: {value}")
    print()
    print(f"Boundary: {BOUNDARY}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
