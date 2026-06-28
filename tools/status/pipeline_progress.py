#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

PIPELINES = [
    ("Workstation status command", "tools/status/specshift_status.sh"),
    ("Pipeline registry check", "tools/pipelines/pipeline_registry_check.py"),
    ("Source health monitor", "tools/pipelines/source_health_check.py"),
    ("CISA KEV defensive intake", "tools/pipelines/cisa_kev_fetch.py"),
    ("USGS Earthquake GeoJSON intake", "tools/pipelines/usgs_earthquake_fetch.py"),
    ("Federal Register policy intake", "tools/pipelines/federal_register_fetch.py"),
    ("arXiv research intake", "tools/pipelines/arxiv_fetch.py"),
    ("NOAA/NWS or SWPC alert intake", "tools/pipelines/noaa_alerts_fetch.py"),
    ("Hugging Face metadata intake", "tools/pipelines/huggingface_metadata_fetch.py"),
    ("SEC EDGAR basic filings intake", "tools/pipelines/sec_edgar_fetch.py"),
    ("World news RSS verification/intake", "tools/pipelines/world_news_rss_fetch.py"),
    ("Daily digest generator", "tools/pipelines/daily_digest.py"),
    ("Claim safety gate", "tools/pipelines/claim_safety_gate.py"),
    ("SpecShift buyer trigger watch", "tools/pipelines/specshift_buyer_trigger_watch.py"),
    ("Finance integrity watch", "tools/pipelines/finance_integrity_watch.py"),
    ("Multi-source contradiction detector", "tools/pipelines/contradiction_detector.py"),
    ("Claim-overstatement detector", "tools/pipelines/claim_overstatement_detector.py"),
    ("Low-frequency high-impact anomaly detector", "tools/pipelines/low_frequency_anomaly_detector.py"),
]

DOC_REQUIREMENTS = [
    ("Pipeline workplan", "workplans/workstation_pipeline_execution_workplan_2026-06-27.md"),
    ("Fast relevance pipeline registry", "docs/workstation/fast_relevance_pipelines.md"),
    ("Unified pipeline schema", "docs/workstation/unified_pipeline_data_schema.md"),
    ("Pipeline guardrails", "docs/workstation/pipeline_safety_and_provenance_guardrails.md"),
    ("MVP source registry", "docs/workstation/minimum_viable_source_registry.md"),
    ("AI recommendation synthesis", "docs/workstation/ai_pipeline_recommendation_synthesis.md"),
    ("7-day MVP build plan", "docs/workstation/fast_pipeline_mvp_7_day_build_plan.md"),
]

def exists(path: str) -> bool:
    return Path(path).exists() and Path(path).stat().st_size > 0

def main() -> int:
    done = 0
    total = len(PIPELINES)

    print("=======================================================================")
    print("Workstation Pipeline Progress")
    print("=======================================================================")
    print()

    for idx, (name, path) in enumerate(PIPELINES, start=1):
        if exists(path):
            mark = "DONE"
            done += 1
        else:
            mark = "TODO"
        print(f"{idx:02d}. [{mark}] {name}")
        print(f"    {path}")

    percent = round((done / total) * 100, 1) if total else 0.0

    print()
    print(f"Pipeline implementation progress: {done}/{total} = {percent}%")
    print()

    doc_done = 0
    doc_total = len(DOC_REQUIREMENTS)

    print("Required planning/control docs:")
    for name, path in DOC_REQUIREMENTS:
        if exists(path):
            mark = "DONE"
            doc_done += 1
        else:
            mark = "TODO"
        print(f"- [{mark}] {name}: {path}")

    doc_percent = round((doc_done / doc_total) * 100, 1) if doc_total else 0.0

    print()
    print(f"Planning/control doc progress: {doc_done}/{doc_total} = {doc_percent}%")
    print()

    if done < total:
        next_item = next((name, path) for name, path in PIPELINES if not exists(path))
        print(f"Next pipeline: {next_item[0]}")
        print(f"Next path: {next_item[1]}")
    else:
        print("Next pipeline: all listed pipelines implemented")

    print()
    print("=======================================================================")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
