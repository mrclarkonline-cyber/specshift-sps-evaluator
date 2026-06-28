#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

TARGETS = [
    {
        "pipeline_number": 22,
        "name": "IAEA IEC",
        "source_type": "web/rss",
        "urls": [
            "https://www.iaea.org/",
            "https://www.iaea.org/about/incident-and-emergency-centre",
            "https://www.iaea.org/newscenter",
            "https://www.iaea.org/newscenter/pressreleases",
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
            "http://www.sica.int/",
        ],
    },
    {
        "pipeline_number": 35,
        "name": "Reuters verification",
        "source_type": "web/rss",
        "urls": [
            "https://www.reuters.com/",
            "https://www.reuters.com/world/",
            "https://www.reutersagency.com/",
            "https://www.reutersagency.com/en/news-feed-solutions/",
        ],
    },
    {
        "pipeline_number": 42,
        "name": "PIB India",
        "source_type": "web/rss",
        "urls": [
            "https://pib.gov.in/",
            "https://pib.gov.in/Allrel.aspx",
            "https://pib.gov.in/PressReleasePage.aspx",
            "https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3",
            "http://pib.gov.in/",
        ],
    },
    {
        "pipeline_number": 47,
        "name": "IEA",
        "source_type": "web/rss",
        "urls": [
            "https://www.iea.org/",
            "https://www.iea.org/news",
            "https://www.iea.org/reports",
            "https://www.iea.org/rss/news.xml",
        ],
    },
]

OUT_DIR = Path("memory_layer/wiki/operator_memory/worldwide_validated")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "phase2_last5_source_access_repair_records.jsonl"

now = datetime.now(timezone.utc).isoformat()

HEADERS = {
    "User-Agent": "Mozilla/5.0 SpecShift-Labs-source-access-validation/0.1 ben@specshiftlabs.com",
    "Accept": "application/json, application/xml, text/xml, text/csv, text/html, */*",
}

def urllib_check(url: str) -> dict:
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            sample = resp.read(4096)
            return {
                "method": "urllib",
                "reachable": 200 <= int(resp.status) < 400,
                "http_status": int(resp.status),
                "content_type": resp.headers.get("Content-Type", ""),
                "sample_bytes": len(sample),
                "note": "urllib bounded check completed.",
            }
    except Exception as exc:
        return {
            "method": "urllib",
            "reachable": False,
            "http_status": None,
            "content_type": "",
            "sample_bytes": 0,
            "note": f"urllib failed: {type(exc).__name__}: {exc}",
        }

def curl_check(url: str) -> dict:
    cmd = [
        "curl",
        "-L",
        "--http1.1",
        "--compressed",
        "--connect-timeout", "12",
        "--max-time", "25",
        "-A", "Mozilla/5.0 SpecShift-Labs-source-access-validation/0.1 ben@specshiftlabs.com",
        "-H", "Accept: text/html,application/xhtml+xml,application/xml,application/json,*/*",
        "-sS",
        "-o", "/tmp/specshift_source_access_sample.tmp",
        "-w", "%{http_code} %{content_type} %{size_download}",
        url,
    ]

    try:
        proc = subprocess.run(cmd, text=True, capture_output=True, check=False)
        parts = proc.stdout.strip().split(maxsplit=2)
        status = int(parts[0]) if parts and parts[0].isdigit() else None
        content_type = parts[1] if len(parts) > 1 else ""
        size = int(float(parts[2])) if len(parts) > 2 and parts[2].replace(".", "", 1).isdigit() else 0

        return {
            "method": "curl",
            "reachable": status is not None and 200 <= status < 400 and size > 0,
            "http_status": status,
            "content_type": content_type,
            "sample_bytes": min(size, 4096),
            "note": "curl bounded check completed." if status else f"curl failed: {proc.stderr.strip()}",
        }
    except Exception as exc:
        return {
            "method": "curl",
            "reachable": False,
            "http_status": None,
            "content_type": "",
            "sample_bytes": 0,
            "note": f"curl exception: {type(exc).__name__}: {exc}",
        }

def check_target(target: dict) -> dict:
    attempts = []
    chosen = None

    for url in target["urls"]:
        for checker in (urllib_check, curl_check):
            result = checker(url)
            result["url"] = url
            attempts.append(result)
            if result["reachable"]:
                chosen = result
                break
        if chosen:
            break

    if chosen is None:
        chosen = attempts[-1]

    return {
        "pipeline_number": target["pipeline_number"],
        "name": target["name"],
        "phase": "phase_2_worldwide_expansion",
        "batch": "last5_source_access_repair",
        "status": "source-access-checked" if chosen["reachable"] else "implemented",
        "phase_progress": 90.0 if chosen["reachable"] else 80.0,
        "source_type": target["source_type"],
        "source_url": chosen["url"],
        "checked_at_utc": now,
        "reachable": chosen["reachable"],
        "http_status": chosen["http_status"],
        "content_type": chosen["content_type"],
        "sample_bytes": chosen["sample_bytes"],
        "access_method": chosen["method"],
        "attempt_count": len(attempts),
        "attempted_urls": [a["url"] for a in attempts],
        "validation_note": chosen["note"],
        "claim_boundary": "Final fallback source-access check only; no live ingestion, content interpretation, alerting, source-content validation, or production readiness claimed.",
    }

records = [check_target(target) for target in TARGETS]

with OUT_PATH.open("w", encoding="utf-8") as f:
    for rec in records:
        f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")

passed = sum(1 for rec in records if rec["reachable"])
print(f"Wrote {OUT_PATH}")
print(f"Last-5 source-access passed: {passed}/{len(records)}")
for rec in records:
    mark = "PASS" if rec["reachable"] else "CHECK"
    print(f"{mark}: {rec['pipeline_number']:02d} {rec['name']} status={rec['http_status']} method={rec['access_method']} url={rec['source_url']}")
