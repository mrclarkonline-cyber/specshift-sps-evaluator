#!/usr/bin/env python3
"""
Phase 2 worldwide group 1 dry-run writer.

Boundary:
- This creates normalized dry-run records from the source registry.
- It does not fetch live source content.
- It does not claim ingestion, validation, contradiction detection, or alerting.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid5, NAMESPACE_URL


ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "configs" / "worldwide_sources" / "phase2_group1_sources.json"
OUTDIR = ROOT / "memory_layer" / "wiki" / "operator_memory" / "worldwide_dryrun"
OUTFILE = OUTDIR / "phase2_group1_dryrun_records.jsonl"
SUMMARY = OUTDIR / "phase2_group1_dryrun_summary.json"


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def make_record(source: dict, checked_at: str) -> dict:
    canonical_url = source.get("candidate_urls", [""])[0]
    seed = f"{source['id']}|{canonical_url}|phase2_group1_dryrun"

    return {
        "record_id": str(uuid5(NAMESPACE_URL, seed)),
        "pipeline_id": source["id"],
        "pipeline_name": source["name"],
        "phase": "phase2_worldwide",
        "status": "dry_run",
        "source_name": source["name"],
        "source_country_or_region": source.get("region_or_country"),
        "source_language": "unknown_or_source_defined",
        "source_url": canonical_url,
        "candidate_urls": source.get("candidate_urls", []),
        "retrieved_at": checked_at,
        "published_at": None,
        "title_original_language": f"DRY RUN CONFIG RECORD: {source['name']}",
        "title_translated": f"DRY RUN CONFIG RECORD: {source['name']}",
        "summary_original_language": source.get("purpose"),
        "summary_translated": source.get("purpose"),
        "entities": [],
        "locations": [],
        "topic_tags": [source.get("category"), source.get("priority")],
        "event_type": "source_configuration_dry_run",
        "confidence": None,
        "uncertainty_label": "configuration_dry_run_not_live_ingestion",
        "bias_or_censorship_notes": source.get("uncertainty_policy"),
        "cross_source_matches": [],
        "cross_country_comparisons": [],
        "claim_safety_notes": source.get("guardrails", []),
        "raw_payload_sha256": sha256_text(json.dumps(source, sort_keys=True)),
        "guardrail_boundary": [
            "not_live_ingestion",
            "not_validated_parsing",
            "not_alerting",
            "not_medical_legal_financial_or_emergency_advice"
        ],
    }


def main() -> int:
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    checked_at = datetime.now(timezone.utc).isoformat()

    records = [make_record(source, checked_at) for source in data.get("sources", [])]

    OUTDIR.mkdir(parents=True, exist_ok=True)
    OUTFILE.write_text(
        "\n".join(json.dumps(record, sort_keys=True) for record in records) + "\n",
        encoding="utf-8",
    )

    summary = {
        "generated_at_utc": checked_at,
        "status": "dry_run_records_written_not_live_ingestion",
        "records_written": len(records),
        "output_file": str(OUTFILE.relative_to(ROOT)),
        "sources": [record["pipeline_name"] for record in records],
        "boundary": "Dry-run records are normalized config artifacts only. They do not represent fetched or validated live source content.",
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")

    print("Phase 2 Group 1 dry-run writer")
    print(f"Records written: {len(records)}")
    print(f"JSONL: {OUTFILE.relative_to(ROOT)}")
    print(f"Summary: {SUMMARY.relative_to(ROOT)}")
    print()
    for i, record in enumerate(records, 1):
        print(f"{i}. [DRY-RUN] {record['pipeline_name']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
