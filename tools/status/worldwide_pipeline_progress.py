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
    ("08", "BBC World Service RSS verification", "docs/workstation/worldwide_source_expansion_backlog.md", "registered"),
    ("09", "Deutsche Welle RSS verification", "docs/workstation/worldwide_source_expansion_backlog.md", "registered"),
    ("10", "Canada Open Government", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("11", "data.gov.uk", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("12", "data.gov.au", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("13", "Copernicus EMS / Data Space", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("14", "ECMWF", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("15", "ESA / EUMETSAT", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("16", "JMA", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("17", "JAXA", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("18", "Geonet NZ", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("19", "Geoscience Australia", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("20", "Smithsonian Global Volcanism Program", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
    ("21", "FAO GIEWS", "docs/workstation/worldwide_pipeline_expansion_registry.md", "registered"),
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

def status_for(source_path: str, expected: str) -> str:
    p = Path(source_path)
    if not p.exists():
        return "missing"
    text = p.read_text(encoding="utf-8", errors="replace").lower()
    return expected if expected.lower() in text else "registered"

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
