#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SOURCES = [
    {
        "pipeline_number": 3,
        "name": "GDACS",
        "url": "https://www.gdacs.org/xml/rss.xml",
        "source_type": "rss",
        "category": "earth_and_environment",
    },
    {
        "pipeline_number": 4,
        "name": "World Bank Open Data",
        "url": "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?format=json&per_page=1",
        "source_type": "api",
        "category": "infrastructure_and_economics",
    },
    {
        "pipeline_number": 5,
        "name": "IMF Data",
        "url": "https://www.imf.org/external/datamapper/api/v1/NGDP_RPCH",
        "source_type": "api",
        "category": "infrastructure_and_economics",
    },
    {
        "pipeline_number": 8,
        "name": "BBC World Service RSS verification",
        "url": "https://feeds.bbci.co.uk/news/world/rss.xml",
        "source_type": "rss",
        "category": "global_news",
    },
    {
        "pipeline_number": 9,
        "name": "Deutsche Welle RSS verification",
        "url": "https://rss.dw.com/rdf/rss-en-all",
        "source_type": "rss",
        "category": "global_news",
    },
    {
        "pipeline_number": 10,
        "name": "Canada Open Government",
        "url": "https://open.canada.ca/data/api/3/action/package_search?rows=1",
        "source_type": "api",
        "category": "government_and_policy",
    },
    {
        "pipeline_number": 11,
        "name": "data.gov.uk",
        "url": "https://data.gov.uk/api/3/action/package_search?rows=1",
        "source_type": "api",
        "category": "government_and_policy",
    },
]

OUT_DIR = Path("memory_layer/wiki/operator_memory/worldwide_phase3/live_sample_batch1")
OUT_DIR.mkdir(parents=True, exist_ok=True)

RAW_OUT = OUT_DIR / "phase3_batch1_raw_sample_metadata.jsonl"
PARSED_OUT = OUT_DIR / "phase3_batch1_parsed_sample_records.jsonl"
SUMMARY_OUT = OUT_DIR / "phase3_batch1_summary.json"

now = datetime.now(timezone.utc).isoformat()

def fetch(source: dict) -> tuple[dict, str]:
    req = urllib.request.Request(
        source["url"],
        headers={
            "User-Agent": "SpecShift-Labs-phase3-bounded-live-sample/0.1 ben@specshiftlabs.com",
            "Accept": "application/json, application/xml, text/xml, text/html, */*",
        },
    )

    meta = {
        "pipeline_number": source["pipeline_number"],
        "name": source["name"],
        "phase": "phase_3_worldwide_live_ingestion_runway",
        "batch": "phase3_live_sample_batch1",
        "source_url": source["url"],
        "source_type": source["source_type"],
        "category": source["category"],
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

def clean_title(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:240]

def parse_sample(source: dict, meta: dict, text: str) -> dict:
    title = ""
    if text:
        if source["source_type"] == "rss":
            m = re.search(r"<title[^>]*>(.*?)</title>", text, flags=re.I | re.S)
            title = clean_title(m.group(1)) if m else ""
        elif source["source_type"] == "api":
            title = clean_title(text[:300])
        else:
            m = re.search(r"<title[^>]*>(.*?)</title>", text, flags=re.I | re.S)
            title = clean_title(m.group(1)) if m else clean_title(text[:300])

    return {
        "pipeline_number": source["pipeline_number"],
        "name": source["name"],
        "phase": "phase_3_worldwide_live_ingestion_runway",
        "batch": "phase3_live_sample_batch1",
        "status": "live-sample-parsed" if meta.get("reachable") else "live-sample-parse-held",
        "phase_progress": 10.0 if meta.get("reachable") else 0.0,
        "source_url": source["url"],
        "source_type": source["source_type"],
        "category": source["category"],
        "retrieved_at": now,
        "title_original_language": title,
        "title_translated": "",
        "summary_original_language": "",
        "summary_translated": "",
        "entities": [],
        "locations": [],
        "topic_tags": [source["category"]],
        "event_type": "bounded_live_sample",
        "confidence": 0.0,
        "uncertainty_label": "sample_only_not_content_validated",
        "bias_or_censorship_notes": "",
        "cross_source_matches": [],
        "cross_country_comparisons": [],
        "claim_safety_notes": [
            "Bounded sample only.",
            "No content validation performed.",
            "No alert or high-stakes conclusion allowed from this record.",
        ],
        "raw_sample_sha256": meta.get("sample_sha256", ""),
        "claim_boundary": "Parsed metadata from bounded live sample only; no production monitoring, content validation, alerting, autonomous action, or truth resolution claimed.",
    }

raw_records = []
parsed_records = []

for source in SOURCES:
    meta, text = fetch(source)
    raw_records.append(meta)
    parsed_records.append(parse_sample(source, meta, text))

with RAW_OUT.open("w", encoding="utf-8") as f:
    for rec in raw_records:
        f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")

with PARSED_OUT.open("w", encoding="utf-8") as f:
    for rec in parsed_records:
        f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")

fetched = sum(1 for r in raw_records if r.get("reachable"))
parsed = sum(1 for r in parsed_records if r.get("status") == "live-sample-parsed")

summary = {
    "phase": "phase_3_worldwide_live_ingestion_runway",
    "batch": "phase3_live_sample_batch1",
    "created_at_utc": now,
    "sources_attempted": len(SOURCES),
    "sources_fetched": fetched,
    "samples_parsed": parsed,
    "raw_artifact": str(RAW_OUT),
    "parsed_artifact": str(PARSED_OUT),
    "claim_boundary": "Phase 3 Batch 1 bounded live-sample ingestion only. This does not claim production monitoring, content validation, alert readiness, autonomous action, or truth resolution.",
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
