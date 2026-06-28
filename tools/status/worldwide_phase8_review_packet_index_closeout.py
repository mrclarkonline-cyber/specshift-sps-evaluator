#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import defaultdict, Counter
from datetime import datetime, timezone
from pathlib import Path

INPUT = Path("memory_layer/wiki/operator_memory/worldwide_phase7/phase7_human_review_packets.jsonl")

OUT_DIR = Path("memory_layer/wiki/operator_memory/worldwide_phase8")
OUT_DIR.mkdir(parents=True, exist_ok=True)

INDEX_OUT = OUT_DIR / "phase8_review_packet_index.json"
REPORT = OUT_DIR / "phase8_review_packet_index_closeout_report.json"

now = datetime.now(timezone.utc).isoformat()

def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        raise SystemExit(f"Missing input artifact: {path}")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

packets = load_jsonl(INPUT)

index_by_category: dict[str, list[dict]] = defaultdict(list)
index_by_source_type_diversity: dict[str, list[dict]] = defaultdict(list)
held_packets = []

for packet in packets:
    packet_id = packet.get("packet_id", "")
    category = packet.get("category", "unknown")
    diversity = packet.get("source_type_diversity", "unknown")
    status = packet.get("status", "")

    source_a = packet.get("source_a", {})
    source_b = packet.get("source_b", {})

    problems = []

    if not packet_id:
        problems.append("missing_packet_id")
    if status != "review-packet-created":
        problems.append(f"unexpected_packet_status:{status}")
    if packet.get("comparison_result") != "not_evaluated":
        problems.append("comparison_result_not_preserved_as_not_evaluated")

    for side_name, source in [("source_a", source_a), ("source_b", source_b)]:
        for field in ["pipeline_number", "name", "source_type", "source_url", "retrieved_at", "uncertainty_label", "claim_safety_label"]:
            if not source.get(field):
                problems.append(f"{side_name}_missing_{field}")

    boundary = str(packet.get("claim_boundary", "")).lower()
    for term in [
        "no production monitoring",
        "content validation",
        "contradiction detection",
        "agreement detection",
        "corroboration",
        "alert readiness",
        "autonomous action",
        "truth resolution",
    ]:
        if term not in boundary:
            problems.append(f"missing_boundary_term:{term}")

    index_record = {
        "packet_id": packet_id,
        "status": status,
        "category": category,
        "source_type_diversity": diversity,
        "source_a_name": source_a.get("name", ""),
        "source_a_url": source_a.get("source_url", ""),
        "source_b_name": source_b.get("name", ""),
        "source_b_url": source_b.get("source_url", ""),
        "comparison_result": packet.get("comparison_result", ""),
        "human_review_tier": packet.get("human_review_tier", ""),
        "index_problems": problems,
        "claim_boundary": "Index reference only. No production monitoring, content validation, contradiction detection, agreement detection, corroboration, alert readiness, autonomous action, or truth resolution claimed.",
    }

    index_by_category[category].append(index_record)
    index_by_source_type_diversity[diversity].append(index_record)

    if problems:
        held_packets.append(index_record)

category_counts = Counter(packet.get("category", "unknown") for packet in packets)
diversity_counts = Counter(packet.get("source_type_diversity", "unknown") for packet in packets)
status_counts = Counter(packet.get("status", "unknown") for packet in packets)

index = {
    "phase": "phase_8_worldwide_review_packet_index_closeout",
    "created_at_utc": now,
    "input_artifact": str(INPUT),
    "packets_indexed": len(packets),
    "packets_held": len(held_packets),
    "index_by_category": dict(sorted(index_by_category.items())),
    "index_by_source_type_diversity": dict(sorted(index_by_source_type_diversity.items())),
    "claim_boundary": "Phase 8 index only. It does not claim production monitoring, content validation, contradiction detection, agreement detection, corroboration, alert readiness, autonomous action, or truth resolution.",
}

INDEX_OUT.write_text(json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

report = {
    "phase": "phase_8_worldwide_review_packet_index_closeout",
    "status": "complete" if packets and not held_packets else "partial" if packets else "held",
    "created_at_utc": now,
    "input_artifact": str(INPUT),
    "index_artifact": str(INDEX_OUT),
    "packets_indexed": len(packets),
    "packets_held": len(held_packets),
    "by_category": dict(sorted(category_counts.items())),
    "by_source_type_diversity": dict(sorted(diversity_counts.items())),
    "by_packet_status": dict(sorted(status_counts.items())),
    "closeout_summary": {
        "phase2": "registry/tracking closure completed",
        "phase3": "bounded live-sample records completed",
        "phase4": "claim-safety normalization completed",
        "phase5": "candidate comparison readiness completed",
        "phase6": "candidate-pair metadata inspection completed",
        "phase7": "human-review packet scaffolds completed",
        "phase8": "review-packet index and closeout completed" if packets and not held_packets else "review-packet index and closeout partial",
    },
    "held_packet_ids": [p.get("packet_id", "") for p in held_packets],
    "claim_boundary": "Phase 8 closeout summarizes packet indexing only. It does not claim production monitoring, content validation, contradiction detection, agreement detection, corroboration, alert readiness, autonomous action, or truth resolution.",
}

REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

print(f"Wrote {INDEX_OUT}")
print(f"Wrote {REPORT}")
print(f"Packets indexed: {len(packets)}")
print(f"Packets held: {len(held_packets)}")

if held_packets:
    for packet in held_packets:
        print(f"HOLD: {packet.get('packet_id')} {packet.get('index_problems')}")
