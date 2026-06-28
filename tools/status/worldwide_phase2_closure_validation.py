#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

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

ADAPTER_SMOKE = Path("memory_layer/wiki/operator_memory/worldwide_adapter_smoke/phase2_all_adapter_smoke_records.jsonl")
OUT_DIR = Path("memory_layer/wiki/operator_memory/worldwide_validated")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "phase2_all_registry_closure_validated_records.jsonl"

now = datetime.now(timezone.utc).isoformat()

if not ADAPTER_SMOKE.exists():
    raise SystemExit(f"Missing adapter smoke artifact: {ADAPTER_SMOKE}")

adapter_records = {}
for line in ADAPTER_SMOKE.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    rec = json.loads(line)
    adapter_records[int(rec["pipeline_number"])] = rec

missing = sorted(set(EXPECTED) - set(adapter_records))
extra = sorted(set(adapter_records) - set(EXPECTED))

if missing:
    raise SystemExit(f"Missing expected adapter smoke records: {missing}")

if extra:
    raise SystemExit(f"Unexpected adapter smoke records: {extra}")

validated = []

for number, name in EXPECTED.items():
    source = adapter_records[number]
    problems = []

    if source.get("name") != name:
        problems.append("name_mismatch")

    if source.get("status") != "adapter-smoke-checked":
        problems.append("adapter_status_not_checked")

    if source.get("adapter_ready") is not True:
        problems.append("adapter_not_ready")

    boundary = str(source.get("claim_boundary", ""))
    required_boundary_terms = [
        "not live ingestion",
        "content validation",
        "alert readiness",
        "production monitoring",
        "truth resolution",
    ]

    lower_boundary = boundary.lower()
    for term in required_boundary_terms:
        if term not in lower_boundary:
            problems.append(f"missing_boundary_term:{term}")

    status = "validated" if not problems else "validation-held"
    phase_progress = 100.0 if not problems else 95.0

    validated.append({
        "pipeline_number": number,
        "name": name,
        "phase": "phase_2_worldwide_expansion",
        "batch": "phase2_registry_closure_validation",
        "status": status,
        "phase_progress": phase_progress,
        "validated_at_utc": now,
        "source_status": source.get("source_status", ""),
        "source_url": source.get("source_url", ""),
        "adapter_ready": source.get("adapter_ready", False),
        "validation_problems": problems,
        "validation_note": "Repo-side registry/tracking closure validation passed." if not problems else "Repo-side closure validation held; see validation_problems.",
        "claim_boundary": "Validated means Phase 2 registry/tracking artifacts are complete, parseable, routeable, and claim-bounded. It does not claim live ingestion, production monitoring, content validation, alert readiness, autonomous action, or truth resolution.",
    })

with OUT_PATH.open("w", encoding="utf-8") as f:
    for rec in validated:
        f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")

passed = sum(1 for rec in validated if rec["status"] == "validated")
held = sum(1 for rec in validated if rec["status"] != "validated")

print(f"Wrote {OUT_PATH}")
print(f"Repo-side closure validated: {passed}/{len(validated)}")
print(f"Held: {held}/{len(validated)}")

if held:
    for rec in validated:
        if rec["status"] != "validated":
            print(f"HOLD: {rec['pipeline_number']:02d} {rec['name']} {rec['validation_problems']}")
else:
    print("All worldwide Phase 2 registry/tracking records passed closure validation.")
