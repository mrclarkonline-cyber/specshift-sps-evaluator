#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

INPUT = Path("memory_layer/wiki/operator_memory/worldwide_phase6/phase6_candidate_pair_inspection_records.jsonl")

OUT_DIR = Path("memory_layer/wiki/operator_memory/worldwide_phase7")
OUT_DIR.mkdir(parents=True, exist_ok=True)

PACKETS_OUT = OUT_DIR / "phase7_human_review_packets.jsonl"
REPORT = OUT_DIR / "phase7_human_review_packet_report.json"

now = datetime.now(timezone.utc).isoformat()

def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        raise SystemExit(f"Missing input artifact: {path}")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

records = load_jsonl(INPUT)
ready_records = [r for r in records if r.get("status") == "inspection-ready"]

packets = []
held = []

for idx, rec in enumerate(ready_records, start=1):
    source_a = rec.get("source_a", {})
    source_b = rec.get("source_b", {})
    category = rec.get("category", "")

    problems = []
    for side_name, source in [("source_a", source_a), ("source_b", source_b)]:
        for field in ["pipeline_number", "name", "source_type", "source_url", "retrieved_at", "uncertainty_label", "claim_safety_label"]:
            if not source.get(field):
                problems.append(f"{side_name}_missing_{field}")

    if not category:
        problems.append("missing_category")

    packet_status = "review-packet-created" if not problems else "review-packet-held"

    packet = {
        "phase": "phase_7_worldwide_human_review_packet_scaffold",
        "packet_id": f"phase7-review-packet-{idx:03d}",
        "status": packet_status,
        "created_at_utc": now,
        "category": category,
        "source_type_diversity": rec.get("source_type_diversity", ""),
        "source_a": source_a,
        "source_b": source_b,
        "comparison_result": "not_evaluated",
        "review_questions": [
            "Do these two records describe comparable event classes, datasets, or public-source observations?",
            "Are the source types sufficiently different to make later comparison meaningful?",
            "Are retrieval timestamps and source URLs adequate for reviewer follow-up?",
            "Are any apparent similarities or differences only metadata-level and not content-level?",
            "Should this pair be promoted to later human review, held for more source context, or discarded?"
        ],
        "reviewer_cautions": [
            "Do not infer agreement from shared category.",
            "Do not infer contradiction from different source framing.",
            "Do not treat machine-readable access as content validation.",
            "Do not create alerts or high-stakes conclusions from this packet.",
            "Keep all judgments at human-review-candidate tier unless separately validated."
        ],
        "packet_problems": problems,
        "human_review_tier": "candidate_only",
        "claim_boundary": "Human-review packet scaffold only. No production monitoring, content validation, contradiction detection, agreement detection, corroboration, alert readiness, autonomous action, or truth resolution claimed."
    }

    if packet_status == "review-packet-held":
        held.append(packet)
    packets.append(packet)

PACKETS_OUT.write_text(
    "\n".join(json.dumps(packet, ensure_ascii=False, sort_keys=True) for packet in packets) + "\n",
    encoding="utf-8",
)

by_category = Counter(packet["category"] for packet in packets)
by_diversity = Counter(packet["source_type_diversity"] for packet in packets)

created = sum(1 for packet in packets if packet["status"] == "review-packet-created")
held_count = sum(1 for packet in packets if packet["status"] == "review-packet-held")

report = {
    "phase": "phase_7_worldwide_human_review_packet_scaffold",
    "status": "complete" if packets and held_count == 0 else "partial" if created else "held",
    "created_at_utc": now,
    "input_artifact": str(INPUT),
    "review_packets_artifact": str(PACKETS_OUT),
    "inspection_ready_pairs_loaded": len(ready_records),
    "review_packets_created": created,
    "review_packets_held": held_count,
    "by_category": dict(sorted(by_category.items())),
    "by_source_type_diversity": dict(sorted(by_diversity.items())),
    "comparison_result_default": "not_evaluated",
    "claim_boundary": "Phase 7 creates human-review packet scaffolds only. It does not claim production monitoring, content validation, contradiction detection, agreement detection, corroboration, alert readiness, autonomous action, or truth resolution."
}

REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

print(f"Wrote {PACKETS_OUT}")
print(f"Wrote {REPORT}")
print(f"Inspection-ready pairs loaded: {len(ready_records)}")
print(f"Review packets created: {created}")
print(f"Review packets held: {held_count}")

if held:
    for packet in held:
        print(f"HOLD: {packet['packet_id']} {packet['packet_problems']}")
