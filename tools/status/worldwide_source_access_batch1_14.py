#!/usr/bin/env python3
from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SOURCES = [
    (1, "WHO Disease Outbreak News", "https://www.who.int/feeds/entity/don/en/rss.xml", "rss"),
    (2, "ReliefWeb / OCHA", "https://api.reliefweb.int/v1/reports?appname=specshift-source-access-check&limit=1", "api"),
    (3, "GDACS", "https://www.gdacs.org/xml/rss.xml", "rss"),
    (4, "World Bank Open Data", "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?format=json&per_page=1", "api"),
    (5, "IMF Data", "https://www.imf.org/external/datamapper/api/v1/NGDP_RPCH", "api"),
    (6, "EU Open Data Portal", "https://data.europa.eu/api/hub/search/datasets?limit=1", "api"),
    (7, "ECDC", "https://www.ecdc.europa.eu/en/rss-feeds", "web"),
    (8, "BBC World Service RSS verification", "https://feeds.bbci.co.uk/news/world/rss.xml", "rss"),
    (9, "Deutsche Welle RSS verification", "https://rss.dw.com/rdf/rss-en-all", "rss"),
    (10, "Canada Open Government", "https://open.canada.ca/data/api/3/action/package_search?rows=1", "api"),
    (11, "data.gov.uk", "https://data.gov.uk/api/3/action/package_search?rows=1", "api"),
    (12, "data.gov.au", "https://data.gov.au/data/api/3/action/package_search?rows=1", "api"),
    (13, "Copernicus EMS / Data Space", "https://catalogue.dataspace.copernicus.eu/resto/api/collections/search.json?maxRecords=1", "api"),
    (14, "ECMWF", "https://www.ecmwf.int/en/forecasts/datasets/open-data", "web"),
]

OUT_DIR = Path("memory_layer/wiki/operator_memory/worldwide_validated")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "phase2_batch1_14_source_access_checked_records.jsonl"

now = datetime.now(timezone.utc).isoformat()

def check(num: int, name: str, url: str, source_type: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "SpecShift-Labs-source-access-validation/0.1 ben@specshiftlabs.com",
            "Accept": "application/json, application/xml, text/xml, text/html, */*",
        },
    )

    rec = {
        "pipeline_number": num,
        "name": name,
        "phase": "phase_2_worldwide_expansion",
        "batch": "source_access_batch_1_14",
        "status": "source-access-checked",
        "phase_progress": 90.0,
        "source_type": source_type,
        "source_url": url,
        "checked_at_utc": now,
        "claim_boundary": "Source-access check only; no live ingestion, content interpretation, alerting, validation of source content, or production readiness claimed.",
    }

    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            sample = resp.read(4096)
            rec.update({
                "reachable": True,
                "http_status": resp.status,
                "content_type": resp.headers.get("Content-Type", ""),
                "sample_bytes": len(sample),
                "validation_note": "Endpoint responded to bounded source-access check.",
            })
    except Exception as exc:
        rec.update({
            "reachable": False,
            "http_status": None,
            "content_type": "",
            "sample_bytes": 0,
            "validation_note": f"Endpoint did not complete bounded source-access check: {type(exc).__name__}: {exc}",
        })

    return rec

records = [check(*src) for src in SOURCES]

with OUT_PATH.open("w", encoding="utf-8") as f:
    for rec in records:
        f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")

reachable = sum(1 for rec in records if rec["reachable"])
print(f"Wrote {OUT_PATH}")
print(f"Reachable: {reachable}/{len(records)}")
for rec in records:
    mark = "PASS" if rec["reachable"] else "CHECK"
    print(f"{mark}: {rec['pipeline_number']:02d} {rec['name']} status={rec['http_status']} bytes={rec['sample_bytes']}")
