#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAW = Path("memory_layer/wiki/operator_memory/worldwide_phase3/live_sample_batch2/phase3_batch2_raw_sample_metadata.jsonl")
PARSED = Path("memory_layer/wiki/operator_memory/worldwide_phase3/live_sample_batch2/phase3_batch2_parsed_sample_records.jsonl")
SUMMARY = Path("memory_layer/wiki/operator_memory/worldwide_phase3/live_sample_batch2/phase3_batch2_summary.json")

now = datetime.now(timezone.utc).isoformat()

fallbacks = {
    12: [
        "https://data.gov.au/data/api/3/action/package_search?rows=1",
        "https://data.gov.au/data/api/3/action/package_search?q=climate&rows=1",
        "https://data.gov.au/data/dataset",
    ],
    14: [
        "https://www.ecmwf.int/en/forecasts/datasets/open-data",
        "https://www.ecmwf.int/",
    ],
    16: [
        "https://www.jma.go.jp/bosai/quake/data/list.json",
        "https://www.jma.go.jp/jma/indexe.html",
    ],
    18: [
        "https://api.geonet.org.nz/quake?MMI=3",
        "https://api.geonet.org.nz/quake?MMI=4",
    ],
    19: [
        "https://earthquakes.ga.gov.au/fdsnws/event/1/query?format=geojson&limit=1",
        "https://earthquakes.ga.gov.au/",
    ],
    20: [
        "https://volcano.si.edu/news/WeeklyVolcanoRSS.xml",
        "https://volcano.si.edu/reports_weekly.cfm",
    ],
    23: [
        "https://africacdc.org/feed/",
        "https://africacdc.org/disease-outbreak-watch/",
        "https://africacdc.org/",
    ],
    24: [
        "https://www.paho.org/en/epidemiological-alerts-and-updates",
        "https://www.paho.org/en",
    ],
    26: [
        "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json",
        "https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json",
    ],
    27: [
        "https://api.data.gov.sg/v1/environment/air-temperature",
        "https://api.data.gov.sg/v1/environment/psi",
    ],
    28: [
        "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001/es/0700/false/BISE/2.0/",
        "https://www.inegi.org.mx/",
    ],
}

def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

def write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in records) + "\n", encoding="utf-8")

def clean(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:240]

def fetch(url: str) -> tuple[bool, dict, str]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "SpecShift-Labs-phase3-bounded-live-sample-repair/0.1 ben@specshiftlabs.com",
            "Accept": "application/json, application/xml, text/xml, text/html, */*",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=18) as resp:
            body = resp.read(12000)
            return True, {
                "http_status": resp.status,
                "content_type": resp.headers.get("Content-Type", ""),
                "sample_bytes": len(body),
                "sample_sha256": hashlib.sha256(body).hexdigest(),
            }, body.decode("utf-8", errors="replace")
    except Exception as exc:
        return False, {"failure": f"{type(exc).__name__}: {exc}"}, ""

raw_records = load_jsonl(RAW)
parsed_records = load_jsonl(PARSED)

held = [r for r in raw_records if r.get("reachable") is not True]

if not held:
    print("No held Batch 2 raw records to repair.")
else:
    for held_rec in held:
        number = int(held_rec["pipeline_number"])
        urls = fallbacks.get(number, [held_rec["source_url"]])

        repaired = None
        repaired_text = ""

        for url in urls:
            ok, meta, text = fetch(url)
            if ok:
                repaired = (url, meta)
                repaired_text = text
                break

        if repaired is None:
            print(f"HOLD: {number:02d} {held_rec['name']} still failed.")
            continue

        url, meta = repaired
        print(f"PASS: {number:02d} {held_rec['name']} repaired with {url}")

        for rec in raw_records:
            if int(rec["pipeline_number"]) == number:
                rec.update({
                    "source_url": url,
                    "reachable": True,
                    "http_status": meta["http_status"],
                    "content_type": meta["content_type"],
                    "sample_bytes": meta["sample_bytes"],
                    "sample_sha256": meta["sample_sha256"],
                    "status": "live-sample-fetched",
                    "repaired_at_utc": now,
                    "claim_boundary": "Bounded live-sample repair fetch only; no production monitoring, content validation, alerting, autonomous action, or truth resolution claimed.",
                })
                rec.pop("failure", None)

        title = clean(repaired_text[:300])
        m = re.search(r"<title[^>]*>(.*?)</title>", repaired_text, flags=re.I | re.S)
        if m:
            title = clean(m.group(1))

        for rec in parsed_records:
            if int(rec["pipeline_number"]) == number:
                rec.update({
                    "source_url": url,
                    "status": "live-sample-parsed",
                    "phase_progress": 10.0,
                    "retrieved_at": now,
                    "title_original_language": title,
                    "raw_sample_sha256": meta["sample_sha256"],
                    "claim_safety_notes": [
                        "Bounded repaired sample only.",
                        "No content validation performed.",
                        "No alert or high-stakes conclusion allowed from this record."
                    ],
                    "claim_boundary": "Parsed metadata from bounded repaired live sample only; no production monitoring, content validation, alerting, autonomous action, or truth resolution claimed.",
                })

write_jsonl(RAW, raw_records)
write_jsonl(PARSED, parsed_records)

fetched = sum(1 for r in raw_records if r.get("reachable") is True)
parsed = sum(1 for r in parsed_records if r.get("status") == "live-sample-parsed")
attempted = len(raw_records)

summary = json.loads(SUMMARY.read_text(encoding="utf-8")) if SUMMARY.exists() else {}
summary.update({
    "sources_attempted": attempted,
    "sources_fetched": fetched,
    "samples_parsed": parsed,
    "repaired_at_utc": now,
    "claim_boundary": "Phase 3 Batch 2 bounded live-sample ingestion only. This does not claim production monitoring, content validation, alert readiness, autonomous action, or truth resolution.",
})
SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

print(f"Batch 2 fetched: {fetched}/{attempted}")
print(f"Batch 2 parsed: {parsed}/{attempted}")
