#!/usr/bin/env python3
from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

TARGETS = [
    {
        "pipeline_number": 6,
        "name": "EU Open Data Portal",
        "source_type": "api/web",
        "urls": [
            "https://data.europa.eu/api/hub/search/datasets?query=climate&limit=1",
            "https://data.europa.eu/api/hub/search/datasets?limit=1",
            "https://data.europa.eu/en",
        ],
    },
    {
        "pipeline_number": 13,
        "name": "Copernicus EMS / Data Space",
        "source_type": "api/web",
        "urls": [
            "https://emergency.copernicus.eu/mapping/list-of-components/EMSR",
            "https://dataspace.copernicus.eu/",
            "https://browser.dataspace.copernicus.eu/",
        ],
    },
    {
        "pipeline_number": 22,
        "name": "IAEA IEC",
        "source_type": "web/rss",
        "urls": [
            "https://www.iaea.org/about/incident-and-emergency-centre",
            "https://www.iaea.org/newscenter",
            "https://www.iaea.org/newscenter/rss/news",
        ],
    },
    {
        "pipeline_number": 34,
        "name": "SICA",
        "source_type": "web",
        "urls": [
            "https://www.sica.int/",
            "https://www.sica.int/noticias",
            "https://www.sica.int/consulta/rss.aspx",
        ],
    },
    {
        "pipeline_number": 35,
        "name": "Reuters verification",
        "source_type": "web/rss",
        "urls": [
            "https://www.reuters.com/world/",
            "https://www.reuters.com/",
            "https://www.reutersagency.com/en/news-feed-solutions/",
        ],
    },
    {
        "pipeline_number": 42,
        "name": "PIB India",
        "source_type": "web/rss",
        "urls": [
            "https://pib.gov.in/",
            "https://pib.gov.in/PressReleasePage.aspx",
            "https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3",
        ],
    },
    {
        "pipeline_number": 47,
        "name": "IEA",
        "source_type": "web/rss",
        "urls": [
            "https://www.iea.org/news",
            "https://www.iea.org/",
            "https://www.iea.org/rss/news.xml",
        ],
    },
]

OUT_DIR = Path("memory_layer/wiki/operator_memory/worldwide_validated")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "phase2_final_source_access_repair_records.jsonl"

now = datetime.now(timezone.utc).isoformat()

def try_url(url: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "SpecShift-Labs-source-access-validation/0.1 ben@specshiftlabs.com",
            "Accept": "application/json, application/xml, text/xml, text/csv, text/html, */*",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            sample = resp.read(4096)
            return {
                "reachable": True,
                "http_status": resp.status,
                "content_type": resp.headers.get("Content-Type", ""),
                "sample_bytes": len(sample),
                "validation_note": "Endpoint responded to bounded fallback source-access check.",
            }
    except Exception as exc:
        return {
            "reachable": False,
            "http_status": None,
            "content_type": "",
            "sample_bytes": 0,
            "validation_note": f"Endpoint failed bounded fallback check: {type(exc).__name__}: {exc}",
        }

def check_target(target: dict) -> dict:
    attempts = []
    chosen = None

    for url in target["urls"]:
        result = try_url(url)
        result["url"] = url
        attempts.append(result)
        if result["reachable"]:
            chosen = result
            break

    if chosen is None:
        chosen = attempts[-1]

    return {
        "pipeline_number": target["pipeline_number"],
        "name": target["name"],
        "phase": "phase_2_worldwide_expansion",
        "batch": "final_source_access_repair",
        "status": "source-access-checked" if chosen["reachable"] else "implemented",
        "phase_progress": 90.0 if chosen["reachable"] else 80.0,
        "source_type": target["source_type"],
        "source_url": chosen["url"],
        "checked_at_utc": now,
        "reachable": chosen["reachable"],
        "http_status": chosen["http_status"],
        "content_type": chosen["content_type"],
        "sample_bytes": chosen["sample_bytes"],
        "attempt_count": len(attempts),
        "attempted_urls": [a["url"] for a in attempts],
        "validation_note": chosen["validation_note"],
        "claim_boundary": "Fallback source-access check only; no live ingestion, content interpretation, alerting, content validation, or production readiness claimed.",
    }

records = [check_target(target) for target in TARGETS]

with OUT_PATH.open("w", encoding="utf-8") as f:
    for rec in records:
        f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")

passed = sum(1 for rec in records if rec["reachable"])
print(f"Wrote {OUT_PATH}")
print(f"Fallback source-access passed: {passed}/{len(records)}")
for rec in records:
    mark = "PASS" if rec["reachable"] else "CHECK"
    print(f"{mark}: {rec['pipeline_number']:02d} {rec['name']} status={rec['http_status']} url={rec['source_url']}")
