#!/usr/bin/env python3
from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SOURCES = [
    (43, "Xinhua", "https://english.news.cn/rss/world.xml", "rss"),
    (44, "TASS", "https://tass.com/rss/v2.xml", "rss"),
    (45, "OECD", "https://sdmx.oecd.org/public/rest/dataflow/OECD.SDD.TPS/all/all?dimension_at_observation=AllDimensions", "api"),
    (46, "BIS", "https://stats.bis.org/api/v1/dataflow", "api"),
    (47, "IEA", "https://www.iea.org/rss/news.xml", "rss"),
    (48, "Global Fishing Watch", "https://globalfishingwatch.org/data-download/datasets/public-fishing-effort/", "web"),
    (49, "IMO", "https://www.imo.org/en/MediaCentre/PressBriefings/Pages/RSS.aspx", "rss"),
    (50, "NSIDC", "https://noaadata.apps.nsidc.org/NOAA/G02135/north/daily/data/NH_seaice_extent_latest.csv", "csv"),
    (51, "SCAR / COMNAP", "https://www.scar.org/feed/", "rss"),
    (52, "Arctic Council / AMAP", "https://www.amap.no/rss", "rss"),
    (53, "National Gazettes", "https://www.gazette.gc.ca/rss/rss-eng.html", "rss"),
    (54, "National Statistical Offices", "https://api.worldbank.org/v2/sources?format=json", "api"),
]

OUT_DIR = Path("memory_layer/wiki/operator_memory/worldwide_validated")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "phase2_batch43_54_source_access_checked_records.jsonl"

now = datetime.now(timezone.utc).isoformat()

def check(num: int, name: str, url: str, source_type: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "SpecShift-Labs-source-access-validation/0.1 ben@specshiftlabs.com",
            "Accept": "application/json, application/xml, text/xml, text/csv, text/html, */*",
        },
    )

    rec = {
        "pipeline_number": num,
        "name": name,
        "phase": "phase_2_worldwide_expansion",
        "batch": "source_access_batch_43_54",
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
