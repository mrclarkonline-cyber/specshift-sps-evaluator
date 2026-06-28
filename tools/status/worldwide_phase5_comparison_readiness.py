#!/usr/bin/env python3
from __future__ import annotations

import itertools
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

INPUT = Path("memory_layer/wiki/operator_memory/worldwide_phase4/phase4_claim_safety_normalized_records.jsonl")

OUT_DIR = Path("memory_layer/wiki/operator_memory/worldwide_phase5")
OUT_DIR.mkdir(parents=True, exist_ok=True)

REPORT = OUT_DIR / "phase5_cross_source_comparison_readiness_report.json"
PAIRS_OUT = OUT_DIR / "phase5_candidate_comparison_pairs.jsonl"

now = datetime.now(timezone.utc).isoformat()

def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        raise SystemExit(f"Missing input artifact: {path}")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

records = load_jsonl(INPUT)

groups: dict[str, list[dict]] = defaultdict(list)
for rec in records:
    category = str(rec.get("category", "unknown"))
    groups[category].append(rec)

candidate_pairs = []
category_reports = []

for category, items in sorted(groups.items()):
    source_types = sorted({str(item.get("source_type", "unknown")) for item in items})
    names = sorted({str(item.get("name", "unknown")) for item in items})

    possible_pairs = list(itertools.combinations(items, 2))
    same_category_pair_count = len(possible_pairs)

    ready = same_category_pair_count > 0

    category_reports.append({
        "category": category,
        "record_count": len(items),
        "source_type_count": len(source_types),
        "source_types": source_types,
        "source_names": names,
        "candidate_pair_count": same_category_pair_count,
        "comparison_readiness": "comparison-ready" if ready else "comparison-held-insufficient-pairs",
        "claim_boundary": "Readiness only. This does not claim agreement, contradiction, content validation, alert readiness, or truth resolution.",
    })

    for a, b in possible_pairs:
        candidate_pairs.append({
            "phase": "phase_5_worldwide_cross_source_comparison_runway",
            "status": "candidate-comparison-pair",
            "category": category,
            "pair_created_at_utc": now,
            "source_a": {
                "pipeline_number": a.get("pipeline_number"),
                "name": a.get("name"),
                "source_type": a.get("source_type"),
                "source_url": a.get("source_url"),
                "retrieved_at": a.get("retrieved_at"),
                "uncertainty_label": a.get("uncertainty_label"),
                "claim_safety_label": a.get("claim_safety_label"),
            },
            "source_b": {
                "pipeline_number": b.get("pipeline_number"),
                "name": b.get("name"),
                "source_type": b.get("source_type"),
                "source_url": b.get("source_url"),
                "retrieved_at": b.get("retrieved_at"),
                "uncertainty_label": b.get("uncertainty_label"),
                "claim_safety_label": b.get("claim_safety_label"),
            },
            "comparison_label": "candidate_pair_only",
            "comparison_result": "not_evaluated",
            "claim_boundary": "Candidate pair only. No contradiction detection, agreement claim, content validation, alert readiness, autonomous action, or truth resolution claimed.",
        })

PAIRS_OUT.write_text(
    "\n".join(json.dumps(pair, ensure_ascii=False, sort_keys=True) for pair in candidate_pairs) + "\n",
    encoding="utf-8",
)

categories_checked = len(category_reports)
ready_categories = sum(1 for item in category_reports if item["comparison_readiness"] == "comparison-ready")
held_categories = categories_checked - ready_categories

report = {
    "phase": "phase_5_worldwide_cross_source_comparison_runway",
    "status": "complete" if categories_checked and held_categories == 0 else "partial" if ready_categories else "held",
    "created_at_utc": now,
    "input_artifact": str(INPUT),
    "candidate_pairs_artifact": str(PAIRS_OUT),
    "records_checked": len(records),
    "categories_checked": categories_checked,
    "comparison_ready_categories": ready_categories,
    "comparison_held_categories": held_categories,
    "candidate_pair_count": len(candidate_pairs),
    "category_reports": category_reports,
    "claim_boundary": "Phase 5 identifies comparison readiness and candidate pairs only. It does not claim production monitoring, content validation, contradiction detection, alert readiness, autonomous action, or truth resolution.",
}

REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

print(f"Wrote {REPORT}")
print(f"Wrote {PAIRS_OUT}")
print(f"Records checked: {len(records)}")
print(f"Categories checked: {categories_checked}")
print(f"Comparison-ready categories: {ready_categories}")
print(f"Held categories: {held_categories}")
print(f"Candidate pairs: {len(candidate_pairs)}")

for item in category_reports:
    print(f"{item['comparison_readiness']}: {item['category']} records={item['record_count']} pairs={item['candidate_pair_count']}")
