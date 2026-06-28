#!/usr/bin/env python3
from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SOURCES = [
    {
        "pipeline_number": 1,
        "name": "WHO Disease Outbreak News",
        "url": "https://www.who.int/feeds/entity/don/en/rss.xml",
        "type": "rss",
        "expected": "reachable",
    },
    {
        "pipeline_number": 2,
        "name": "ReliefWeb / OCHA",
        "url": "https://api.reliefweb.int/v1/reports?appname=specshift-source-access-check&limit=1",
        "type": "api",
        "expected": "reachable",
    },
    {
        "pipeline_number": 3,
        "name": "GDACS",
        "url": "https://www.gdacs.org/xml/rss.xml",
        "type": "rss",
        "expected": "reachable",
    },
    {
        "pipeline_number": 4,
        "name": "World Bank Open Data",
        "url": "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?format=json&per_page=1",
        "type": "api",
        "expected": "reachable",
    },
    {
        "pipeline_number": 5,
        "name": "IMF Data",
        "url": "https://www.imf.org/external/datamapper/api/v1/NGDP_RPCH",
        "type": "api",
        "expected": "reachable",
    },
    {
        "pipeline_number": 6,
        "name": "EU Open Data Portal",
        "url": "https://data.europa.eu/api/hub/search/datasets?limit=1",
        "type": "api",
        "expected": "reachable",
    },
    {
        "pipeline_number": 7,
        "name": "ECDC",
        "url": "https://www.ecdc.europa.eu/en/rss-feeds",
        "type": "web",
        "expected": "reachable",
    },
]

OUT_DIR = Path("memory_layer/wiki/operator_memory/worldwide_validated")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "phase2_group1_source_access_validation.jsonl"

now = datetime.now(timezone.utc).isoformat()

def check_source(source: dict) -> dict:
    req = urllib.request.Request(
        source["url"],
        headers={
            "User-Agent": "SpecShift-Labs-source-access-validation/0.1 ben@specshiftlabs.com",
            "Accept": "application/json, application/xml, text/xml, text/html, */*",
        },
    )

    result = {
        "pipeline_number": source["pipeline_number"],
        "name": source["name"],
        "phase": "phase_2_worldwide_expansion",
        "batch": "source_access_batch_1",
        "status": "source-access-checked",
        "phase_progress": 90.0,
        "source_type": source["type"],
        "source_url": source["url"],
        "checked_at_utc": now,
        "claim_boundary": "Source access validation only; no live ingestion, content interpretation, alerting, or production readiness claimed.",
    }

    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            body = resp.read(4096)
            result.update({
                "reachable": True,
                "http_status": resp.status,
                "content_type": resp.headers.get("Content-Type", ""),
                "sample_bytes": len(body),
                "validation_note": "Endpoint responded to bounded access check.",
            })
    except Exception as exc:
        result.update({
            "reachable": False,
            "http_status": None,
            "content_type": "",
            "sample_bytes": 0,
            "validation_note": f"Endpoint did not complete bounded access check: {type(exc).__name__}: {exc}",
        })

    return result

records = [check_source(source) for source in SOURCES]

with OUT_PATH.open("w", encoding="utf-8") as f:
    for rec in records:
        f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")

reachable = sum(1 for r in records if r["reachable"])
print(f"Wrote {OUT_PATH}")
print(f"Reachable: {reachable}/{len(records)}")
for r in records:
    mark = "PASS" if r["reachable"] else "CHECK"
    print(f"{mark}: {r['pipeline_number']:02d} {r['name']} status={r['http_status']} bytes={r['sample_bytes']}")
