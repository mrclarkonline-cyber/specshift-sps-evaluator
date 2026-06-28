#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# Remaining implemented external pipelines from latest landing:
# 01, 02, 06, 13, 17, 21, 22, 25, 29, 33, 34, 35, 39, 42, 43, 45, 47, 49, 50, 52, 53
#
# Use alternate or broader public endpoints where the first source-access check failed.
SOURCES = [
    (1, "WHO Disease Outbreak News", "https://www.who.int/emergencies/disease-outbreak-news", "web"),
    (2, "ReliefWeb / OCHA", "https://reliefweb.int/updates/rss.xml", "rss"),
    (6, "EU Open Data Portal", "https://data.europa.eu/api/hub/search/datasets?query=climate&limit=1", "api"),
    (13, "Copernicus EMS / Data Space", "https://emergency.copernicus.eu/mapping/list-of-components/EMSR", "web"),
    (17, "JAXA", "https://global.jaxa.jp/press/", "web"),
    (21, "FAO GIEWS", "https://www.fao.org/giews/countrybrief/index.jsp", "web"),
    (22, "IAEA IEC", "https://www.iaea.org/about/incident-and-emergency-centre", "web"),
    (25, "AHA Centre", "https://adinet.ahacentre.org/", "web"),
    (29, "ECLAC", "https://www.cepal.org/en/pressreleases", "web"),
    (33, "CDEMA", "https://www.cdema.org/", "web"),
    (34, "SICA", "https://www.sica.int/", "web"),
    (35, "Reuters verification", "https://www.reuters.com/world/", "web"),
    (39, "Kyodo", "https://english.kyodonews.net/", "web"),
    (42, "PIB India", "https://pib.gov.in/PressReleasePage.aspx", "web"),
    (43, "Xinhua", "https://english.news.cn/world/index.htm", "web"),
    (45, "OECD", "https://sdmx.oecd.org/public/rest/dataflow", "api"),
    (47, "IEA", "https://www.iea.org/news", "web"),
    (49, "IMO", "https://www.imo.org/en/MediaCentre/PressBriefings/Pages/Default.aspx", "web"),
    (50, "NSIDC", "https://nsidc.org/arcticseaicenews/", "web"),
    (52, "Arctic Council / AMAP", "https://www.amap.no/", "web"),
    (53, "National Gazettes", "https://www.gazette.gc.ca/accueil-home-eng.html", "web"),
]

OUT_DIR = Path("memory_layer/wiki/operator_memory/worldwide_validated")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "phase2_remaining_source_access_fast_checked_records.jsonl"

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
        "batch": "remaining_source_access_fast",
        "status": "source-access-checked",
        "phase_progress": 90.0,
        "source_type": source_type,
        "source_url": url,
        "checked_at_utc": now,
        "claim_boundary": "Source-access check only; no live ingestion, content interpretation, alerting, validation of source content, or production readiness claimed.",
    }

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
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
