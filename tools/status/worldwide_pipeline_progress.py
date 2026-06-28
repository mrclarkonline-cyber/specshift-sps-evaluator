#!/usr/bin/env python3
from pathlib import Path

PIPELINES = [
    ("01", "WHO Disease Outbreak News", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group1_dryrun_records.jsonl", "dry-run"),
    ("02", "ReliefWeb / OCHA", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group1_dryrun_records.jsonl", "dry-run"),
    ("03", "GDACS", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group1_dryrun_records.jsonl", "dry-run"),
    ("04", "World Bank Open Data", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group1_dryrun_records.jsonl", "dry-run"),
    ("05", "IMF Data", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group1_dryrun_records.jsonl", "dry-run"),
    ("06", "EU Open Data Portal", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group1_dryrun_records.jsonl", "dry-run"),
    ("07", "ECDC", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group1_dryrun_records.jsonl", "dry-run"),
    ("08", "BBC World Service RSS verification", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group2_dryrun_records.jsonl", "dry-run"),
    ("09", "Deutsche Welle RSS verification", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group2_dryrun_records.jsonl", "dry-run"),
    ("10", "Canada Open Government", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group2_dryrun_records.jsonl", "dry-run"),
    ("11", "data.gov.uk", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group2_dryrun_records.jsonl", "dry-run"),
    ("12", "data.gov.au", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group2_dryrun_records.jsonl", "dry-run"),
    ("13", "Copernicus EMS / Data Space", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group2_dryrun_records.jsonl", "dry-run"),
    ("14", "ECMWF", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group2_dryrun_records.jsonl", "dry-run"),
    ("15", "ESA / EUMETSAT", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group3_dryrun_records.jsonl", "dry-run"),
    ("16", "JMA", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group3_dryrun_records.jsonl", "dry-run"),
    ("17", "JAXA", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group3_dryrun_records.jsonl", "dry-run"),
    ("18", "Geonet NZ", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group3_dryrun_records.jsonl", "dry-run"),
    ("19", "Geoscience Australia", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group3_dryrun_records.jsonl", "dry-run"),
    ("20", "Smithsonian Global Volcanism Program", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group3_dryrun_records.jsonl", "dry-run"),
    ("21", "FAO GIEWS", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group3_dryrun_records.jsonl", "dry-run"),
    ("22", "IAEA IEC", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("23", "Africa CDC", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("24", "PAHO", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("25", "AHA Centre", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("26", "BMKG Indonesia", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("27", "Singapore NEA", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("28", "INEGI", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("29", "ECLAC", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("30", "SSN Mexico", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("31", "INPE Brazil", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("32", "SERNAGEOMIN Chile", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("33", "CDEMA", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("34", "SICA", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("35", "Reuters verification", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("36", "AFP verification", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("37", "Al Jazeera", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("38", "NHK World", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("39", "Kyodo", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("40", "Yonhap", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("41", "PTI", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("42", "PIB India", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("43", "Xinhua", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("44", "TASS", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("45", "OECD", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("46", "BIS", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("47", "IEA", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("48", "Global Fishing Watch", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("49", "IMO", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("50", "NSIDC", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("51", "SCAR / COMNAP", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("52", "Arctic Council / AMAP", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("53", "National Gazettes", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("54", "National Statistical Offices", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("55", "Multi-Country Contradiction Detector", "workplans/worldwide_pipeline_expansion_workplan_2026-06-28.md", "registered"),
    ("56", "Global anomaly flagger", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
]

STATUS_ORDER = {
    "missing": 0,
    "registered": 1,
    "configured": 1.625,
    "verify-first": 1,
    "bias-flag-required": 1,
    "official-claim-only": 1,
    "state-media-guarded": 1,
    "privacy-guard-required": 1,
    "per-country-only": 1,
    "build-last": 1,
    "dry-run": 2,
    "live-fetch": 3,
    "validated": 4,
    "done": 5,
}

def status_for(expected_path, declared_status):
    """Return the effective status for a pipeline row.

    Rule:
    - If the expected artifact exists, trust the declared row status.
    - If the artifact is missing, keep it at registered.
    - This allows dry-run JSONL artifacts to count as dry-run without falsely
      claiming live-fetch, validated, or done.
    """
    from pathlib import Path

    artifact = Path(expected_path)
    if artifact.exists():
        return declared_status
    return "registered"



def pct(status: str) -> float:
    return (STATUS_ORDER.get(status, 0) / 5.0) * 100.0

rows = []
for num, name, source_path, expected in PIPELINES:
    status = status_for(source_path, expected)
    rows.append((num, name, source_path, status, pct(status)))

total_pct = sum(row[4] for row in rows) / len(rows) if rows else 0.0
done_count = sum(1 for row in rows if row[3] == "done")
registered_or_better = sum(1 for row in rows if STATUS_ORDER.get(row[3], 0) >= 1)

print("=======================================================================")
print("Worldwide Pipeline Expansion Progress")
print("=======================================================================")
print()
for num, name, source_path, status, percent in rows:
    label = status.upper()
    print(f"{num}. [{label}] {name}")
    print(f"    {source_path}")
    print(f"    Phase progress: {percent:.1f}%")
print()
configured_count = sum(1 for row in rows if row[3] == "configured")
print(f"Worldwide expansion registration progress: {registered_or_better}/{len(rows)} = {(registered_or_better/len(rows))*100:.1f}%")
print(f"Worldwide expansion configuration progress: {configured_count}/{len(rows)} = {(configured_count/len(rows))*100:.1f}%")
print(f"Worldwide expansion implementation progress: {done_count}/{len(rows)} = {(done_count/len(rows))*100:.1f}%")
print(f"Overall Phase 2 progress score: {total_pct:.1f}%")
print()
print("Next worldwide build group:")
print("1. WHO Disease Outbreak News")
print("2. ReliefWeb / OCHA")
print("3. GDACS")
print("4. World Bank")
print("5. IMF")
print("6. EU Open Data Portal")
print("7. ECDC")
print()
print("=======================================================================")
