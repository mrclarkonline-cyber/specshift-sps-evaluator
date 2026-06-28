#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

INPUTS = {
    "phase4_normalized_records": Path("memory_layer/wiki/operator_memory/worldwide_phase4/phase4_claim_safety_normalized_records.jsonl"),
    "phase5_candidate_pairs": Path("memory_layer/wiki/operator_memory/worldwide_phase5/phase5_candidate_comparison_pairs.jsonl"),
    "phase6_inspection_records": Path("memory_layer/wiki/operator_memory/worldwide_phase6/phase6_candidate_pair_inspection_records.jsonl"),
    "phase7_review_packets": Path("memory_layer/wiki/operator_memory/worldwide_phase7/phase7_human_review_packets.jsonl"),
    "phase8_packet_index": Path("memory_layer/wiki/operator_memory/worldwide_phase8/phase8_review_packet_index.json"),
}

OUT_DIR = Path("memory_layer/wiki/operator_memory/worldwide_phase10")
OUT_DIR.mkdir(parents=True, exist_ok=True)

REPORT = OUT_DIR / "phase10_pattern_detection_report.json"
PATTERNS_OUT = OUT_DIR / "phase10_candidate_pattern_records.jsonl"

now = datetime.now(timezone.utc).isoformat()

def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

phase4 = load_jsonl(INPUTS["phase4_normalized_records"])
phase5 = load_jsonl(INPUTS["phase5_candidate_pairs"])
phase6 = load_jsonl(INPUTS["phase6_inspection_records"])
phase7 = load_jsonl(INPUTS["phase7_review_packets"])
phase8 = load_json(INPUTS["phase8_packet_index"])

artifacts_checked = sum(1 for p in INPUTS.values() if p.exists())

patterns = []

def add_pattern(pattern_type: str, observed_value: str, count: int, support: list[str], interpretation: str) -> None:
    patterns.append({
        "phase": "phase_10_worldwide_pattern_detection_layer",
        "status": "candidate-pattern-detected",
        "detected_at_utc": now,
        "pattern_type": pattern_type,
        "observed_value": observed_value,
        "count": count,
        "supporting_artifacts": support,
        "observed_metadata": True,
        "candidate_interpretation": interpretation,
        "suggested_human_check": "Review whether this metadata-level concentration is meaningful, a sampling artifact, or simply expected from the bounded source list.",
        "claim_boundary": "Candidate metadata pattern only. No production monitoring, content validation, contradiction detection, causal inference, prediction, alert readiness, autonomous action, or truth resolution claimed."
    })

category_counts = Counter(str(r.get("category", "unknown")) for r in phase4)
for category, count in sorted(category_counts.items()):
    if count >= 2:
        add_pattern(
            "category_recurrence",
            category,
            count,
            [str(INPUTS["phase4_normalized_records"])],
            "Multiple normalized records share this category; this may support later category-level review."
        )

source_type_counts = Counter(str(r.get("source_type", "unknown")) for r in phase4)
for source_type, count in sorted(source_type_counts.items()):
    if count >= 2:
        add_pattern(
            "source_type_recurrence",
            source_type,
            count,
            [str(INPUTS["phase4_normalized_records"])],
            "Multiple normalized records share this source type; this may reveal intake-shape concentration."
        )

uncertainty_counts = Counter(str(r.get("uncertainty_label", "unknown")) for r in phase4)
for label, count in sorted(uncertainty_counts.items()):
    if count >= 2:
        add_pattern(
            "uncertainty_label_recurrence",
            label,
            count,
            [str(INPUTS["phase4_normalized_records"])],
            "The same uncertainty label recurs across bounded samples; this is expected if the runway is correctly preserving sample-only status."
        )

claim_safety_counts = Counter(str(r.get("claim_safety_label", "unknown")) for r in phase4)
for label, count in sorted(claim_safety_counts.items()):
    if count >= 2:
        add_pattern(
            "claim_safety_label_recurrence",
            label,
            count,
            [str(INPUTS["phase4_normalized_records"])],
            "The same claim-safety label recurs; this may indicate boundary consistency across the intake runway."
        )

pair_category_counts = Counter(str(r.get("category", "unknown")) for r in phase5)
for category, count in sorted(pair_category_counts.items()):
    if count >= 2:
        add_pattern(
            "candidate_pair_density_by_category",
            category,
            count,
            [str(INPUTS["phase5_candidate_pairs"])],
            "This category has multiple candidate comparison pairs; later review may prioritize or sample from it."
        )

inspection_diversity_counts = Counter(str(r.get("source_type_diversity", "unknown")) for r in phase6)
for diversity, count in sorted(inspection_diversity_counts.items()):
    if count >= 2:
        add_pattern(
            "source_type_diversity_cluster",
            diversity,
            count,
            [str(INPUTS["phase6_inspection_records"])],
            "Multiple inspected pairs share this source-type diversity label; this may affect later review design."
        )

packet_category_counts = Counter(str(r.get("category", "unknown")) for r in phase7)
for category, count in sorted(packet_category_counts.items()):
    if count >= 2:
        add_pattern(
            "review_packet_category_cluster",
            category,
            count,
            [str(INPUTS["phase7_review_packets"])],
            "Multiple human-review packets exist in this category; this may support category-level reviewer batching."
        )

if phase8:
    by_category = phase8.get("index_by_category", {})
    if isinstance(by_category, dict):
        for category, items in sorted(by_category.items()):
            if isinstance(items, list) and len(items) >= 2:
                add_pattern(
                    "indexed_packet_category_cluster",
                    category,
                    len(items),
                    [str(INPUTS["phase8_packet_index"])],
                    "The packet index shows multiple indexed packets in this category; this supports findability, not validation."
                )

PATTERNS_OUT.write_text(
    "\n".join(json.dumps(p, ensure_ascii=False, sort_keys=True) for p in patterns) + "\n",
    encoding="utf-8"
)

pattern_type_counts = Counter(p["pattern_type"] for p in patterns)

report = {
    "phase": "phase_10_worldwide_pattern_detection_layer",
    "status": "complete" if artifacts_checked and patterns else "held",
    "created_at_utc": now,
    "input_artifacts": {k: str(v) for k, v in INPUTS.items()},
    "artifacts_checked": artifacts_checked,
    "candidate_patterns_detected": len(patterns),
    "patterns_held": 0,
    "pattern_type_counts": dict(sorted(pattern_type_counts.items())),
    "candidate_patterns_artifact": str(PATTERNS_OUT),
    "claim_boundary": "Phase 10 detects metadata-level candidate patterns only. It does not claim production monitoring, content validation, contradiction detection, agreement detection, causal inference, prediction, alert readiness, autonomous action, or truth resolution."
}

REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

print(f"Wrote {PATTERNS_OUT}")
print(f"Wrote {REPORT}")
print(f"Artifacts checked: {artifacts_checked}")
print(f"Candidate patterns detected: {len(patterns)}")
for pattern_type, count in sorted(pattern_type_counts.items()):
    print(f"{pattern_type}: {count}")
