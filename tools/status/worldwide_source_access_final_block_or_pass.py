#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

TARGETS = [
    {
        "pipeline_number": 34,
        "name": "SICA",
        "source_type": "web",
        "urls": [
            "https://www.sica.int/",
            "http://www.sica.int/",
            "https://www.sica.int/noticias",
            "https://www.sica.int/consulta/Noticias.aspx",
            "https://www.sica.int/busqueda/busqueda.aspx",
            "https://www.sica.int/consulta/entidad.aspx",
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
            "https://www.iea.org/data-and-statistics",
            "https://www.iea.org/analysis",
            "https://www.iea.org/topics",
            "https://www.iea.org/rss/news.xml",
        ],
    },
]

OUT_DIR = Path("memory_layer/wiki/operator_memory/worldwide_validated")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "phase2_final_block_or_pass_source_access_records.jsonl"

now = datetime.now(timezone.utc).isoformat()

def curl_check(url: str) -> dict:
    cmd = [
        "curl",
        "-L",
        "--http1.1",
        "--compressed",
        "--retry", "2",
        "--connect-timeout", "15",
        "--max-time", "35",
        "-A", "Mozilla/5.0 AppleWebKit/605.1.15 SpecShift-Labs-source-access-validation/0.1",
        "-H", "Accept: text/html,application/xhtml+xml,application/xml,application/json,*/*",
        "-sS",
        "-o", "/tmp/specshift_final_block_or_pass.tmp",
        "-w", "%{http_code} %{size_download}",
        url,
    ]

    proc = subprocess.run(cmd, text=True, capture_output=True, check=False)
    parts = proc.stdout.strip().split()
    status = int(parts[0]) if parts and parts[0].isdigit() else None
    size = int(float(parts[1])) if len(parts) > 1 and parts[1].replace(".", "", 1).isdigit() else 0

    return {
        "url": url,
        "reachable": status is not None and 200 <= status < 400 and size > 0,
        "http_status": status,
        "sample_bytes": min(size, 4096),
        "validation_note": "curl bounded source-access check completed." if status else f"curl failed: {proc.stderr.strip()}",
    }

def check_target(target: dict) -> dict:
    attempts = []
    chosen = None

    for url in target["urls"]:
        result = curl_check(url)
        attempts.append(result)
        if result["reachable"]:
            chosen = result
            break

    if chosen is None:
        chosen = attempts[-1]

    reachable = bool(chosen["reachable"])

    return {
        "pipeline_number": target["pipeline_number"],
        "name": target["name"],
        "phase": "phase_2_worldwide_expansion",
        "batch": "final_block_or_pass_source_access",
        "status": "source-access-checked" if reachable else "source-access-blocked",
        "phase_progress": 90.0 if reachable else 90.0,
        "source_type": target["source_type"],
        "source_url": chosen["url"],
        "checked_at_utc": now,
        "reachable": reachable,
        "http_status": chosen["http_status"],
        "sample_bytes": chosen["sample_bytes"],
        "attempt_count": len(attempts),
        "attempted_urls": [a["url"] for a in attempts],
        "validation_note": chosen["validation_note"] if reachable else "Official source access could not be completed from this workstation after multiple bounded attempts; registered as source-access-blocked so the workplan can proceed without falsely claiming endpoint reachability.",
        "claim_boundary": "Source-access status only. Blocked does not mean the source is invalid; it means this workstation did not complete bounded access. No live ingestion, content validation, alerting, or production readiness claimed.",
    }

records = [check_target(target) for target in TARGETS]

with OUT_PATH.open("w", encoding="utf-8") as f:
    for rec in records:
        f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")

passed = sum(1 for rec in records if rec["reachable"])
blocked = sum(1 for rec in records if rec["status"] == "source-access-blocked")
print(f"Wrote {OUT_PATH}")
print(f"Passed: {passed}/{len(records)}")
print(f"Blocked: {blocked}/{len(records)}")
for rec in records:
    mark = "PASS" if rec["reachable"] else "BLOCKED"
    print(f"{mark}: {rec['pipeline_number']:02d} {rec['name']} status={rec['http_status']} url={rec['source_url']}")
