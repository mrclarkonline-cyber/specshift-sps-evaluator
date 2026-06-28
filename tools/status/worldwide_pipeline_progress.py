#!/usr/bin/env python3
from pathlib import Path

PIPELINES = [
    ("01", "WHO Disease Outbreak News", "memory_layer/wiki/operator_memory/worldwide_configured/phase2_group1_configured_records.jsonl", "configured"),
    ("02", "ReliefWeb / OCHA", "memory_layer/wiki/operator_memory/worldwide_configured/phase2_group1_configured_records.jsonl", "configured"),
    ("03", "GDACS", "memory_layer/wiki/operator_memory/worldwide_configured/phase2_group1_configured_records.jsonl", "configured"),
    ("04", "World Bank Open Data", "memory_layer/wiki/operator_memory/worldwide_configured/phase2_group1_configured_records.jsonl", "configured"),
    ("05", "IMF Data", "memory_layer/wiki/operator_memory/worldwide_configured/phase2_group1_configured_records.jsonl", "configured"),
    ("06", "EU Open Data Portal", "memory_layer/wiki/operator_memory/worldwide_configured/phase2_group1_configured_records.jsonl", "configured"),
    ("07", "ECDC", "memory_layer/wiki/operator_memory/worldwide_configured/phase2_group1_configured_records.jsonl", "configured"),
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
    ("22", "IAEA IEC", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group4_dryrun_records.jsonl", "dry-run"),
    ("23", "Africa CDC", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group4_dryrun_records.jsonl", "dry-run"),
    ("24", "PAHO", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group4_dryrun_records.jsonl", "dry-run"),
    ("25", "AHA Centre", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group4_dryrun_records.jsonl", "dry-run"),
    ("26", "BMKG Indonesia", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group4_dryrun_records.jsonl", "dry-run"),
    ("27", "Singapore NEA", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group4_dryrun_records.jsonl", "dry-run"),
    ("28", "INEGI", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group4_dryrun_records.jsonl", "dry-run"),
    ("29", "ECLAC", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group5_dryrun_records.jsonl", "dry-run"),
    ("30", "SSN Mexico", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group5_dryrun_records.jsonl", "dry-run"),
    ("31", "INPE Brazil", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group5_dryrun_records.jsonl", "dry-run"),
    ("32", "SERNAGEOMIN Chile", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group5_dryrun_records.jsonl", "dry-run"),
    ("33", "CDEMA", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group5_dryrun_records.jsonl", "dry-run"),
    ("34", "SICA", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group5_dryrun_records.jsonl", "dry-run"),
    ("35", "Reuters verification", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group5_dryrun_records.jsonl", "dry-run"),
    ("36", "AFP verification", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group6_to_8_dryrun_records.jsonl", "dry-run"),
    ("37", "Al Jazeera", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group6_to_8_dryrun_records.jsonl", "dry-run"),
    ("38", "NHK World", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group6_to_8_dryrun_records.jsonl", "dry-run"),
    ("39", "Kyodo", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group6_to_8_dryrun_records.jsonl", "dry-run"),
    ("40", "Yonhap", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group6_to_8_dryrun_records.jsonl", "dry-run"),
    ("41", "PTI", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group6_to_8_dryrun_records.jsonl", "dry-run"),
    ("42", "PIB India", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group6_to_8_dryrun_records.jsonl", "dry-run"),
    ("43", "Xinhua", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group6_to_8_dryrun_records.jsonl", "dry-run"),
    ("44", "TASS", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group6_to_8_dryrun_records.jsonl", "dry-run"),
    ("45", "OECD", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group6_to_8_dryrun_records.jsonl", "dry-run"),
    ("46", "BIS", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group6_to_8_dryrun_records.jsonl", "dry-run"),
    ("47", "IEA", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group6_to_8_dryrun_records.jsonl", "dry-run"),
    ("48", "Global Fishing Watch", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group6_to_8_dryrun_records.jsonl", "dry-run"),
    ("49", "IMO", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group6_to_8_dryrun_records.jsonl", "dry-run"),
    ("50", "NSIDC", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group6_to_8_dryrun_records.jsonl", "dry-run"),
    ("51", "SCAR / COMNAP", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group6_to_8_dryrun_records.jsonl", "dry-run"),
    ("52", "Arctic Council / AMAP", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group6_to_8_dryrun_records.jsonl", "dry-run"),
    ("53", "National Gazettes", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group6_to_8_dryrun_records.jsonl", "dry-run"),
    ("54", "National Statistical Offices", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group6_to_8_dryrun_records.jsonl", "dry-run"),
    ("55", "Multi-Country Contradiction Detector", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group6_to_8_dryrun_records.jsonl", "dry-run"),
    ("56", "Global anomaly flagger", "memory_layer/wiki/operator_memory/worldwide_dryrun/phase2_group6_to_8_dryrun_records.jsonl", "dry-run"),
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
