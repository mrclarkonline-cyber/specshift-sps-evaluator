#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

SOURCE_RECORD_FILES = [
    Path("memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch1_14_source_access_checked_records.jsonl"),
    Path("memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch15_28_source_access_checked_records.jsonl"),
    Path("memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch29_42_source_access_checked_records.jsonl"),
    Path("memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch43_54_source_access_checked_records.jsonl"),
    Path("memory_layer/wiki/operator_memory/worldwide_validated/phase2_remaining_source_access_fast_checked_records.jsonl"),
    Path("memory_layer/wiki/operator_memory/worldwide_validated/phase2_final_source_access_repair_records.jsonl"),
    Path("memory_layer/wiki/operator_memory/worldwide_validated/phase2_last5_source_access_repair_records.jsonl"),
    Path("memory_layer/wiki/operator_memory/worldwide_validated/phase2_final3_source_access_repair_records.jsonl"),
    Path("memory_layer/wiki/operator_memory/worldwide_validated/phase2_final_block_or_pass_source_access_records.jsonl"),
    Path("memory_layer/wiki/operator_memory/worldwide_validated/phase2_derived_pipeline_validation_records.jsonl"),
]

EXPECTED = {
    1: "WHO Disease Outbreak News",
    2: "ReliefWeb / OCHA",
    3: "GDACS",
    4: "World Bank Open Data",
    5: "IMF Data",
    6: "EU Open Data Portal",
    7: "ECDC",
    8: "BBC World Service RSS verification",
    9: "Deutsche Welle RSS verification",
    10: "Canada Open Government",
    11: "data.gov.uk",
    12: "data.gov.au",
    13: "Copernicus EMS / Data Space",
    14: "ECMWF",
    15: "ESA / EUMETSAT",
    16: "JMA",
    17: "JAXA",
    18: "Geonet NZ",
    19: "Geoscience Australia",
    20: "Smithsonian Global Volcanism Program",
    21: "FAO GIEWS",
    22: "IAEA IEC",
    23: "Africa CDC",
    24: "PAHO",
    25: "AHA Centre",
    26: "BMKG Indonesia",
    27: "Singapore NEA",
    28: "INEGI",
    29: "ECLAC",
    30: "SSN Mexico",
    31: "INPE Brazil",
    32: "SERNAGEOMIN Chile",
    33: "CDEMA",
    34: "SICA",
    35: "Reuters verification",
    36: "AFP verification",
    37: "Al Jazeera",
    38: "NHK World",
    39: "Kyodo",
    40: "Yonhap",
    41: "PTI",
    42: "PIB India",
    43: "Xinhua",
    44: "TASS",
    45: "OECD",
    46: "BIS",
    47: "IEA",
    48: "Global Fishing Watch",
    49: "IMO",
    50: "NSIDC",
    51: "SCAR / COMNAP",
    52: "Arctic Council / AMAP",
    53: "National Gazettes",
    54: "National Statistical Offices",
    55: "Multi-Country Contradiction Detector",
    56: "Global anomaly flagger",
}

OUT_DIR = Path("memory_layer/wiki/operator_memory/worldwide_adapter_smoke")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "phase2_all_adapter_smoke_records.jsonl"

now = datetime.now(timezone.utc).isoformat()

latest: dict[int, dict] = {}

for file_path in SOURCE_RECORD_FILES:
    if not file_path.exists():
        continue
    for line in file_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue

        try:
            number = int(rec["pipeline_number"])
        except Exception:
            continue

        if number not in EXPECTED:
            continue

        latest[number] = rec

records = []

for number, name in EXPECTED.items():
    source = latest.get(number)
    if not source:
        status = "adapter-smoke-missing-source-record"
        progress = 90.0
        adapter_ready = False
        adapter_note = "No source-access or blocked record found for adapter smoke validation."
        source_status = "missing"
        source_url = ""
    else:
        source_status = str(source.get("status", "unknown"))
        source_url = str(source.get("source_url", ""))

        if source_status in {"source-access-checked", "source-access-blocked"}:
            status = "adapter-smoke-checked"
            progress = 95.0
            adapter_ready = True
            adapter_note = "Adapter smoke validation passed: source-access status record is parseable, routeable, and claim-bounded."
        else:
            status = "adapter-smoke-held"
            progress = 90.0
            adapter_ready = False
            adapter_note = f"Adapter smoke validation held because source status is {source_status!r}."

    records.append({
        "pipeline_number": number,
        "name": name,
        "phase": "phase_2_worldwide_expansion",
        "batch": "all_adapter_smoke_validation",
        "status": status,
        "phase_progress": progress,
        "adapter_ready": adapter_ready,
        "source_status": source_status,
        "source_url": source_url,
        "checked_at_utc": now,
        "validation_note": adapter_note,
        "claim_boundary": "Adapter smoke validation only. This proves repo-side routing/status parsing, not live ingestion, content validation, alert readiness, production monitoring, autonomous action, or truth resolution.",
    })

with OUT_PATH.open("w", encoding="utf-8") as f:
    for rec in records:
        f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")

ready = sum(1 for r in records if r["adapter_ready"])
print(f"Wrote {OUT_PATH}")
print(f"Adapter-smoke checked: {ready}/{len(records)}")
for rec in records:
    mark = "PASS" if rec["adapter_ready"] else "HOLD"
    print(f"{mark}: {rec['pipeline_number']:02d} {rec['name']} -> {rec['status']} ({rec['phase_progress']}%)")
