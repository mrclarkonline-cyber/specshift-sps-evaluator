#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SOURCES = [
    (12, "data.gov.au", "https://data.gov.au/data/api/3/action/package_search?rows=1", "api", "government_and_policy"),
    (14, "ECMWF", "https://www.ecmwf.int/en/forecasts/datasets/open-data", "web", "earth_and_environment"),
    (16, "JMA", "https://www.jma.go.jp/bosai/quake/data/list.json", "api", "earth_and_environment"),
    (18, "Geonet NZ", "https://api.geonet.org.nz/quake?MMI=3", "api", "earth_and_environment"),
    (19, "Geoscience Australia", "https://earthquakes.ga.gov.au/fdsnws/event/1/query?format=geojson&limit=1", "api", "earth_and_environment"),
    (20, "Smithsonian Global Volcanism Program", "https://volcano.si.edu/news/WeeklyVolcanoRSS.xml", "rss", "earth_and_environment"),
    (23, "Africa CDC", "https://africacdc.org/feed/", "rss", "health_and_biosecurity"),
    (24, "PAHO", "https://www.paho.org/en/epidemiological-alerts-and-updates", "web", "health_and_biosecurity"),
    (26, "BMKG Indonesia", "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json", "api", "earth_and_environment"),
    (27, "Singapore NEA", "https://api.data.gov.sg/v1/environment/air-temperature", "api", "earth_and_environment"),
    (28, "INEGI", "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001/es/0700/false/BISE/2.0/", "api", "infrastructure_and_economics"),
]

OUT_DIR = Path("memory_layer/wiki/operator_memory/worldwide_phase3/live_sample_batch2")
OUT_DIR.mkdir(parents=True, exist_ok=True)

RAW_OUT = OUT_DIR / "phase3_batch2_raw_sample_metadata.jsonl"
PARSED_OUT = OUT_DIR / "phase3_batch2_parsed_sample_records.jsonl"
SUMMARY_OUT = OUT_DIR / "phase3_batch2_summary.json"

now = datetime.now(timezone.utc).isoformat()

def fetch(num, name, url, source_type, category):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "SpecShift-Labs-phase3-bounded-live-sample/0.1 ben@specshiftlabs.com",
            "Accept": "application/json, application/xml, text/xml, text/html, */*",
        },
    )

    meta = {
        "pipeline_number": num,
        "name": name,
        "phase": "phase_3_worldwide_live_ingestion_runway",
        "batch": "phase3_live_sample_batch2",
        "source_url": url,
        "source_type": source_type,
        "category": category,
        "fetched_at_utc": now,
        "status": "live-sample-fetched",
        "claim_boundary": "Bounded live-sample fetch only; no production monitoring, content validation, alerting, autonomous action, or truth resolution claimed.",
    }

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read(12000)
            text = body.decode("utf-8", errors="replace")
            meta.update({
                "reachable": True,
                "http_status": resp.status,
                "content_type": resp.headers.get("Content-Type", ""),
                "sample_bytes": len(body),
                "sample_sha256": hashlib.sha256(body).hexdigest(),
            })
            return meta, text
    except Exception as exc:
        meta.update({
            "reachable": False,
            "http_status": None,
            "content_type": "",
            "sample_bytes": 0,
            "sample_sha256": "",
            "status": "live-sample-fetch-failed",
            "failure": f"{type(exc).__name__}: {exc}",
        })
        return meta, ""

def clean(text):
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:240]

def parse(num, name, url, source_type, category, meta, text):
    title = ""
    if text:
        if source_type == "rss":
            m = re.search(r"<title[^>]*>(.*?)</title>", text, flags=re.I | re.S)
            title = clean(m.group(1)) if m else ""
        elif source_type == "web":
            m = re.search(r"<title[^>]*>(.*?)</title>", text, flags=re.I | re.S)
            title = clean(m.group(1)) if m else clean(text[:300])
        else:
            title = clean(text[:300])

    return {
        "pipeline_number": num,
        "name": name,
        "phase": "phase_3_worldwide_live_ingestion_runway",
        "batch": "phase3_live_sample_batch2",
        "status": "live-sample-parsed" if meta.get("reachable") else "live-sample-parse-held",
        "phase_progress": 10.0 if meta.get("reachable") else 0.0,
        "source_url": url,
        "source_type": source_type,
        "category": category,
        "retrieved_at": now,
        "title_original_language": title,
        "title_translated": "",
        "summary_original_language": "",
        "summary_translated": "",
        "entities": [],
        "locations": [],
        "topic_tags": [category],
        "event_type": "bounded_live_sample",
        "confidence": 0.0,
        "uncertainty_label": "sample_only_not_content_validated",
        "bias_or_censorship_notes": "",
        "cross_source_matches": [],
        "cross_country_comparisons": [],
        "claim_safety_notes": [
            "Bounded sample only.",
            "No content validation performed.",
            "No alert or high-stakes conclusion allowed from this record."
        ],
        "raw_sample_sha256": meta.get("sample_sha256", ""),
        "claim_boundary": "Parsed metadata from bounded live sample only; no production monitoring, content validation, alerting, autonomous action, or truth resolution claimed.",
    }

raw_records = []
parsed_records = []

for source in SOURCES:
    meta, text = fetch(*source)
    raw_records.append(meta)
    parsed_records.append(parse(*source, meta, text))

RAW_OUT.write_text("\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in raw_records) + "\n", encoding="utf-8")
PARSED_OUT.write_text("\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in parsed_records) + "\n", encoding="utf-8")

fetched = sum(1 for r in raw_records if r.get("reachable"))
parsed = sum(1 for r in parsed_records if r.get("status") == "live-sample-parsed")

summary = {
    "phase": "phase_3_worldwide_live_ingestion_runway",
    "batch": "phase3_live_sample_batch2",
    "created_at_utc": now,
    "sources_attempted": len(SOURCES),
    "sources_fetched": fetched,
    "samples_parsed": parsed,
    "raw_artifact": str(RAW_OUT),
    "parsed_artifact": str(PARSED_OUT),
    "claim_boundary": "Phase 3 Batch 2 bounded live-sample ingestion only. This does not claim production monitoring, content validation, alert readiness, autonomous action, or truth resolution.",
}

SUMMARY_OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

print(f"Wrote {RAW_OUT}")
print(f"Wrote {PARSED_OUT}")
print(f"Wrote {SUMMARY_OUT}")
print(f"Fetched: {fetched}/{len(SOURCES)}")
print(f"Parsed: {parsed}/{len(SOURCES)}")

for rec in parsed_records:
    mark = "PASS" if rec["status"] == "live-sample-parsed" else "HOLD"
    print(f"{mark}: {rec['pipeline_number']:02d} {rec['name']} -> {rec['status']}")
