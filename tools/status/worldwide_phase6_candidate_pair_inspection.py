#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

INPUT = Path("memory_layer/wiki/operator_memory/worldwide_phase5/phase5_candidate_comparison_pairs.jsonl")

OUT_DIR = Path("memory_layer/wiki/operator_memory/worldwide_phase6")
OUT_DIR.mkdir(parents=True, exist_ok=True)

REPORT = OUT_DIR / "phase6_candidate_pair_inspection_report.json"
INSPECTED_OUT = OUT_DIR / "phase6_candidate_pair_inspection_records.jsonl"

now = datetime.now(timezone.utc).isoformat()

def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        raise SystemExit(f"Missing input artifact: {path}")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

pairs = load_jsonl(INPUT)
inspected = []

for pair in pairs:
    problems = []

    source_a = pair.get("source_a", {})
    source_b = pair.get("source_b", {})

    category = pair.get("category", "")
    if not category:
        problems.append("missing_category")

    for side_name, source in [("source_a", source_a), ("source_b", source_b)]:
        for field in ["pipeline_number", "name", "source_type", "source_url", "retrieved_at", "uncertainty_label", "claim_safety_label"]:
            if not source.get(field):
                problems.append(f"{side_name}_missing_{field}")

    if source_a.get("source_url") == source_b.get("source_url"):
        problems.append("same_source_url")

    source_type_diversity = "different_source_types" if source_a.get("source_type") != source_b.get("source_type") else "same_source_type"

    uncertainty_ok = (
        source_a.get("uncertainty_label") == "sample_only_not_content_validated"
        and source_b.get("uncertainty_label") == "sample_only_not_content_validated"
    )
    if not uncertainty_ok:
        problems.append("uncertainty_label_not_preserved")

    claim_safety_ok = (
        source_a.get("claim_safety_label") == "sample_only_not_content_validated"
        and source_b.get("claim_safety_label") == "sample_only_not_content_validated"
    )
    if not claim_safety_ok:
        problems.append("claim_safety_label_not_preserved")

    pair_ready = not problems

    inspected.append({
        "phase": "phase_6_worldwide_candidate_pair_inspection_scaffold",
        "status": "inspection-ready" if pair_ready else "inspection-held",
        "pair_inspected_at_utc": now,
        "category": category,
        "source_type_diversity": source_type_diversity,
        "source_a": source_a,
        "source_b": source_b,
        "inspection_problems": problems,
        "later_human_review_meaningful": pair_ready,
        "inspection_note": "Metadata-level pair inspection passed." if pair_ready else "Metadata-level pair inspection held; see inspection_problems.",
        "comparison_result": "not_evaluated",
        "claim_boundary": "Metadata inspection only. No contradiction detection, agreement detection, corroboration, content validation, alert readiness, autonomous action, production monitoring, or truth resolution claimed.",
    })

INSPECTED_OUT.write_text(
    "\n".join(json.dumps(rec, ensure_ascii=False, sort_keys=True) for rec in inspected) + "\n",
    encoding="utf-8",
)

pairs_checked = len(inspected)
ready_pairs = sum(1 for rec in inspected if rec["status"] == "inspection-ready")
held_pairs = pairs_checked - ready_pairs

by_category = Counter(rec["category"] for rec in inspected)
by_diversity = Counter(rec["source_type_diversity"] for rec in inspected)

report = {
    "phase": "phase_6_worldwide_candidate_pair_inspection_scaffold",
    "status": "complete" if pairs_checked and held_pairs == 0 else "partial" if ready_pairs else "held",
    "created_at_utc": now,
    "input_artifact": str(INPUT),
    "inspection_records_artifact": str(INSPECTED_OUT),
    "pairs_checked": pairs_checked,
    "inspection_ready_pairs": ready_pairs,
    "inspection_held_pairs": held_pairs,
    "by_category": dict(sorted(by_category.items())),
    "by_source_type_diversity": dict(sorted(by_diversity.items())),
    "claim_boundary": "Phase 6 inspects candidate-pair metadata only. It does not claim production monitoring, content validation, contradiction detection, agreement detection, corroboration, alert readiness, autonomous action, or truth resolution.",
}

REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

print(f"Wrote {REPORT}")
print(f"Wrote {INSPECTED_OUT}")
print(f"Pairs checked: {pairs_checked}")
print(f"Inspection-ready pairs: {ready_pairs}")
print(f"Held pairs: {held_pairs}")

if held_pairs:
    for rec in inspected:
        if rec["status"] != "inspection-ready":
            print(f"HOLD: {rec['category']} {rec['inspection_problems']}")
