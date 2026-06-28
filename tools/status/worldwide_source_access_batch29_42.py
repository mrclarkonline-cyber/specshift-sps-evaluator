#!/usr/bin/env python3
from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SOURCES = [
    (29, "ECLAC", "https://www.cepal.org/en/rss.xml", "rss"),
    (30, "SSN Mexico", "http://www.ssn.unam.mx/rss/ultimos-sismos.xml", "rss"),
    (31, "INPE Brazil", "https://terrabrasilis.dpi.inpe.br/queimadas/portal/", "web"),
    (32, "SERNAGEOMIN Chile", "https://www.sernageomin.cl/feed/", "rss"),
    (33, "CDEMA", "https://www.cdema.org/feed/", "rss"),
    (34, "SICA", "https://www.sica.int/consulta/rss.aspx", "rss"),
    (35, "Reuters verification", "https://www.reuters.com/world/rss", "rss"),
    (36, "AFP verification", "https://www.afp.com/en/news-hub", "web"),
    (37, "Al Jazeera", "https://www.aljazeera.com/xml/rss/all.xml", "rss"),
    (38, "NHK World", "https://www3.nhk.or.jp/rss/news/cat0.xml", "rss"),
    (39, "Kyodo", "https://english.kyodonews.net/rss/news.xml", "rss"),
    (40, "Yonhap", "https://en.yna.co.kr/RSS/news.xml", "rss"),
    (41, "PTI", "https://www.ptinews.com/rss", "rss"),
    (42, "PIB India", "https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3", "rss"),
]

OUT_DIR = Path("memory_layer/wiki/operator_memory/worldwide_validated")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "phase2_batch29_42_source_access_checked_records.jsonl"

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
        "batch": "source_access_batch_29_42",
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
