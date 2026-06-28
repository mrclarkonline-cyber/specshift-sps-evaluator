#!/usr/bin/env python3
"""
Phase 2 worldwide group 1 source health check.

This is a connectivity/configuration scaffold only.
It does not claim ingestion, parsing, validation, or operational alerting.
"""

from __future__ import annotations

import json
import socket
import ssl
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "configs" / "worldwide_sources" / "phase2_group1_sources.json"
OUTDIR = ROOT / "memory_layer" / "wiki" / "operator_memory"
OUT = OUTDIR / "phase2_group1_healthcheck_latest.json"


def check_url(url: str, timeout: int = 10) -> dict:
    parsed = urllib.parse.urlparse(url)
    result = {
        "url": url,
        "scheme": parsed.scheme,
        "host": parsed.netloc,
        "ok": False,
        "status": None,
        "error": None,
    }

    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        result["error"] = "unsupported_or_invalid_url"
        return result

    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "SpecShiftLabs-Phase2Healthcheck/0.1 (ben@specshiftlabs.com)",
                "Accept": "application/json, application/xml, text/xml, text/html;q=0.8,*/*;q=0.5",
            },
            method="GET",
        )
        context = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=timeout, context=context) as resp:
            result["status"] = getattr(resp, "status", None)
            result["content_type"] = resp.headers.get("content-type")
            result["ok"] = result["status"] is not None and 200 <= result["status"] < 400
            # Read only a tiny prefix to avoid bulk collection.
            prefix = resp.read(512)
            result["sample_bytes"] = len(prefix)
    except urllib.error.HTTPError as exc:
        result["status"] = exc.code
        result["error"] = f"http_error:{exc.code}"
    except urllib.error.URLError as exc:
        result["error"] = f"url_error:{exc.reason}"
    except socket.timeout:
        result["error"] = "timeout"
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}:{exc}"

    return result


def main() -> int:
    if not CONFIG.exists():
        print(f"Missing config: {CONFIG}", file=sys.stderr)
        return 1

    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    checked_at = datetime.now(timezone.utc).isoformat()

    report = {
        "checked_at_utc": checked_at,
        "status": "healthcheck_only_not_live_ingestion",
        "config": str(CONFIG.relative_to(ROOT)),
        "sources_total": len(data.get("sources", [])),
        "sources": [],
    }

    for source in data.get("sources", []):
        source_report = {
            "id": source["id"],
            "name": source["name"],
            "status": source.get("status"),
            "checks": [],
        }
        for url in source.get("candidate_urls", []):
            source_report["checks"].append(check_url(url))
        source_report["any_ok"] = any(c.get("ok") for c in source_report["checks"])
        report["sources"].append(source_report)

    OUTDIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")

    ok_count = sum(1 for s in report["sources"] if s["any_ok"])
    print("Phase 2 Group 1 Health Check")
    print(f"Checked at UTC: {checked_at}")
    print(f"Sources reachable: {ok_count}/{report['sources_total']}")
    print(f"Report: {OUT.relative_to(ROOT)}")
    print()
    for i, s in enumerate(report["sources"], 1):
        status = "OK" if s["any_ok"] else "CHECK"
        print(f"{i:02d}. [{status}] {s['name']}")
        for c in s["checks"]:
            detail = c.get("status") if c.get("status") is not None else c.get("error")
            print(f"    - {c['url']} -> {detail}")

    return 0 if ok_count > 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
