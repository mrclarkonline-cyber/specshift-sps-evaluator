#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

INPUTS = [
    Path("memory_layer/wiki/operator_memory/worldwide_phase3/live_sample_batch1/phase3_batch1_parsed_sample_records.jsonl"),
    Path("memory_layer/wiki/operator_memory/worldwide_phase3/live_sample_batch2/phase3_batch2_parsed_sample_records.jsonl"),
]

OUT_DIR = Path("memory_layer/wiki/operator_memory/worldwide_phase4")
OUT_DIR.mkdir(parents=True, exist_ok=True)

REPORT = OUT_DIR / "phase4_claim_safety_normalization_report.json"
RECORDS_OUT = OUT_DIR / "phase4_claim_safety_normalized_records.jsonl"

now = datetime.now(timezone.utc).isoformat()

REQUIRED_FIELDS = [
    "pipeline_number",
    "name",
    "phase",
    "batch",
    "status",
    "source_url",
    "source_type",
    "category",
    "retrieved_at",
    "title_original_language",
    "title_translated",
    "summary_original_language",
    "summary_translated",
    "topic_tags",
    "event_type",
    "confidence",
    "uncertainty_label",
    "claim_safety_notes",
    "claim_boundary",
]

FORBIDDEN_CLAIMS = [
    "production monitoring validated",
    "content truth validated",
    "alert ready",
    "autonomous action ready",
    "truth resolution validated",
]

HIGH_RISK_HINTS = {
    "global_news",
    "government_and_policy",
    "health_and_biosecurity",
}

def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        records.append(json.loads(line))
    return records

records = []
for path in INPUTS:
    records.extend(load_jsonl(path))

normalized = []

for rec in records:
    problems = []

    for field in REQUIRED_FIELDS:
        if field not in rec:
            problems.append(f"missing_field:{field}")

    boundary = str(rec.get("claim_boundary", "")).lower()
    boundary_terms = [
        "no production monitoring",
        "content validation",
        "alerting",
        "autonomous action",
        "truth resolution",
    ]

    for term in boundary_terms:
        if term not in boundary:
            problems.append(f"missing_boundary_term:{term}")

    uncertainty = str(rec.get("uncertainty_label", ""))
    if uncertainty != "sample_only_not_content_validated":
        problems.append("uncertainty_label_not_sample_only")

    if not isinstance(rec.get("claim_safety_notes", []), list) or not rec.get("claim_safety_notes"):
        problems.append("claim_safety_notes_missing_or_empty")

    lower_blob = json.dumps(rec, ensure_ascii=False).lower()
    for phrase in FORBIDDEN_CLAIMS:
        if phrase in lower_blob:
            problems.append(f"forbidden_claim:{phrase}")

    category = str(rec.get("category", ""))
    risk_label = "standard_sample_only"
    if category in HIGH_RISK_HINTS:
        risk_label = "heightened_review_sample_only"

    normalized_record = {
        "pipeline_number": rec.get("pipeline_number"),
        "name": rec.get("name"),
        "phase": "phase_4_worldwide_claim_safety_normalization",
        "source_phase": rec.get("phase"),
        "source_batch": rec.get("batch"),
        "status": "claim-safety-normalized" if not problems else "claim-safety-held",
        "phase_progress": 100.0 if not problems else 50.0,
        "source_url": rec.get("source_url", ""),
        "source_type": rec.get("source_type", ""),
        "category": category,
        "retrieved_at": rec.get("retrieved_at", ""),
        "checked_at_utc": now,
        "title_original_language": rec.get("title_original_language", ""),
        "title_translated": rec.get("title_translated", ""),
        "summary_original_language": rec.get("summary_original_language", ""),
        "summary_translated": rec.get("summary_translated", ""),
        "uncertainty_label": uncertainty,
        "claim_safety_label": "sample_only_not_content_validated",
        "review_risk_label": risk_label,
        "normalization_problems": problems,
        "validation_note": "Schema, provenance, language separation, uncertainty label, and claim boundary checks passed." if not problems else "Held for normalization problems.",
        "claim_boundary": "Phase 4 normalization only. This does not claim production monitoring, content validation, alert readiness, autonomous action, or truth resolution.",
    }

    normalized.append(normalized_record)

RECORDS_OUT.write_text(
    "\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in normalized) + "\n",
    encoding="utf-8",
)

checked = len(normalized)
passed = sum(1 for r in normalized if r["status"] == "claim-safety-normalized")
held = checked - passed

by_category = {}
for rec in normalized:
    category = rec.get("category", "unknown")
    by_category[category] = by_category.get(category, 0) + 1

report = {
    "phase": "phase_4_worldwide_claim_safety_normalization",
    "status": "complete" if checked and held == 0 else "partial" if passed else "held",
    "created_at_utc": now,
    "records_checked": checked,
    "records_passed": passed,
    "records_held": held,
    "input_artifacts": [str(p) for p in INPUTS],
    "normalized_records_artifact": str(RECORDS_OUT),
    "by_category": by_category,
    "claim_boundary": "Phase 4 checks schema, provenance, language separation, uncertainty, category routing, and claim-safety labels only. It does not claim production monitoring, content validation, alert readiness, autonomous action, or truth resolution.",
}

REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

print(f"Wrote {RECORDS_OUT}")
print(f"Wrote {REPORT}")
print(f"Records checked: {checked}")
print(f"Records passed:  {passed}")
print(f"Records held:    {held}")

if held:
    for rec in normalized:
        if rec["status"] != "claim-safety-normalized":
            print(f"HOLD: {rec['pipeline_number']} {rec['name']} {rec['normalization_problems']}")
