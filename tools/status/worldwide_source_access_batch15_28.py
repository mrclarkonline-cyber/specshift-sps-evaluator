#!/usr/bin/env python3
from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SOURCES = [
    (15, "ESA / EUMETSAT", "https://www.esa.int/rssfeed/TopNews", "rss"),
    (16, "JMA", "https://www.jma.go.jp/bosai/quake/data/list.json", "api"),
    (17, "JAXA", "https://global.jaxa.jp/press/index.rdf", "rss"),
    (18, "Geonet NZ", "https://api.geonet.org.nz/quake?MMI=3", "api"),
    (19, "Geoscience Australia", "https://earthquakes.ga.gov.au/fdsnws/event/1/query?format=geojson&limit=1", "api"),
    (20, "Smithsonian Global Volcanism Program", "https://volcano.si.edu/news/WeeklyVolcanoRSS.xml", "rss"),
    (21, "FAO GIEWS", "https://www.fao.org/giews/rss/en/", "rss"),
    (22, "IAEA IEC", "https://www.iaea.org/newscenter/rss/news", "rss"),
    (23, "Africa CDC", "https://africacdc.org/feed/", "rss"),
    (24, "PAHO", "https://www.paho.org/en/epidemiological-alerts-and-updates", "web"),
    (25, "AHA Centre", "https://api.reliefweb.int/v1/reports?appname=specshift-source-access-check&query[value]=AHA%20Centre&limit=1", "api"),
    (26, "BMKG Indonesia", "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json", "api"),
    (27, "Singapore NEA", "https://api.data.gov.sg/v1/environment/air-temperature", "api"),
    (28, "INEGI", "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001/es/0700/false/BISE/2.0/", "api"),
]

OUT_DIR = Path("memory_layer/wiki/operator_memory/worldwide_validated")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "phase2_batch15_28_source_access_checked_records.jsonl"

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
        "batch": "source_access_batch_15_28",
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
