#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CISA_KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
REPORT_ROOT = Path("reports/fast_relevance")


@dataclass
class FetchResult:
    retrieved_at_utc: str
    source_url: str
    raw_sha256: str
    raw_path: Path
    summary_path: Path
    record_count: int


def utc_now_slug() -> tuple[str, str]:
    now = datetime.now(timezone.utc)
    iso = now.isoformat().replace("+00:00", "Z")
    slug = now.strftime("%Y%m%dT%H%M%SZ")
    return iso, slug


def fetch_bytes(url: str, timeout: int = 30) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "SpecShiftLabsResearchWorkstation/0.1 ben@specshiftlabs.com",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_get(record: dict[str, Any], key: str, default: str = "") -> str:
    value = record.get(key, default)
    if value is None:
        return default
    return str(value).strip()


def sorted_vulnerabilities(payload: dict[str, Any]) -> list[dict[str, Any]]:
    vulns = payload.get("vulnerabilities", [])
    if not isinstance(vulns, list):
        raise ValueError("CISA payload field 'vulnerabilities' is not a list")

    def sort_key(item: dict[str, Any]) -> str:
        return safe_get(item, "dateAdded", "")

    return sorted(
        [v for v in vulns if isinstance(v, dict)],
        key=sort_key,
        reverse=True,
    )


def build_summary(
    payload: dict[str, Any],
    raw_sha256: str,
    source_url: str,
    retrieved_at_utc: str,
    raw_path: Path,
    limit: int,
) -> str:
    vulns = sorted_vulnerabilities(payload)
    catalog_version = payload.get("catalogVersion", "unknown")
    catalog_date_released = payload.get("dateReleased", "unknown")
    count = len(vulns)

    lines: list[str] = []
    lines.append("# CISA KEV Defensive Advisory Digest")
    lines.append("")
    lines.append(f"Retrieved at UTC: {retrieved_at_utc}")
    lines.append(f"Source: {source_url}")
    lines.append(f"Catalog version: {catalog_version}")
    lines.append(f"Catalog date released: {catalog_date_released}")
    lines.append(f"Raw payload SHA256: {raw_sha256}")
    lines.append(f"Raw payload path: {raw_path}")
    lines.append(f"Record count: {count}")
    lines.append("")
    lines.append("## Safety Boundary")
    lines.append("")
    lines.append("This digest is defensive awareness only.")
    lines.append("")
    lines.append("Do not use this output for exploit generation, attack chains, target-specific reconnaissance, active probing, evasion guidance, or weaponization.")
    lines.append("")
    lines.append("## Latest KEV Records")
    lines.append("")

    for idx, vuln in enumerate(vulns[:limit], start=1):
        cve_id = safe_get(vuln, "cveID", "unknown")
        vendor = safe_get(vuln, "vendorProject", "unknown")
        product = safe_get(vuln, "product", "unknown")
        vuln_name = safe_get(vuln, "vulnerabilityName", "unknown")
        date_added = safe_get(vuln, "dateAdded", "unknown")
        due_date = safe_get(vuln, "dueDate", "unknown")
        ransomware = safe_get(vuln, "knownRansomwareCampaignUse", "unknown")
        required_action = safe_get(vuln, "requiredAction", "See CISA source")

        lines.append(f"### {idx}. {cve_id}")
        lines.append("")
        lines.append(f"- Vendor/project: {vendor}")
        lines.append(f"- Product: {product}")
        lines.append(f"- Vulnerability name: {vuln_name}")
        lines.append(f"- Date added: {date_added}")
        lines.append(f"- Due date: {due_date}")
        lines.append(f"- Known ransomware campaign use: {ransomware}")
        lines.append(f"- Required action: {required_action}")
        lines.append("- Uncertainty label: institutional_directive")
        lines.append("- Source tier: tier_1_authoritative")
        lines.append("")

    lines.append("## Claim Safety Note")
    lines.append("")
    lines.append("CISA KEV confirms that a vulnerability is in the Known Exploited Vulnerabilities catalog. It does not by itself determine local exposure, compromise, or required local action without human review of local systems.")
    lines.append("")

    return "\n".join(lines)


def write_outputs(raw_data: bytes, limit: int) -> FetchResult:
    retrieved_at_utc, slug = utc_now_slug()
    day = slug[:8]
    day_dir = REPORT_ROOT / f"{day[:4]}-{day[4:6]}-{day[6:8]}"
    raw_dir = day_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    raw_sha256 = sha256_bytes(raw_data)
    raw_path = raw_dir / f"cisa_kev_{slug}.json"
    summary_path = day_dir / "cybersecurity_cisa_kev.md"

    payload = json.loads(raw_data.decode("utf-8"))
    vulns = sorted_vulnerabilities(payload)

    raw_path.write_bytes(raw_data)
    summary = build_summary(
        payload=payload,
        raw_sha256=raw_sha256,
        source_url=CISA_KEV_URL,
        retrieved_at_utc=retrieved_at_utc,
        raw_path=raw_path,
        limit=limit,
    )
    summary_path.write_text(summary, encoding="utf-8")

    return FetchResult(
        retrieved_at_utc=retrieved_at_utc,
        source_url=CISA_KEV_URL,
        raw_sha256=raw_sha256,
        raw_path=raw_path,
        summary_path=summary_path,
        record_count=len(vulns),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch CISA KEV catalog for defensive awareness.")
    parser.add_argument("--dry-run", action="store_true", help="Validate configuration without network fetch.")
    parser.add_argument("--limit", type=int, default=10, help="Number of latest KEV records to summarize.")
    args = parser.parse_args()

    print("=== CISA KEV Fetch ===")
    print(f"source_url: {CISA_KEV_URL}")
    print("mode: dry-run" if args.dry_run else "mode: live-fetch")
    print("safety: defensive awareness only")

    if args.limit < 1:
        print("FAIL --limit must be >= 1")
        return 1

    if args.dry_run:
        print("PASS dry-run configuration")
        print("No network calls performed.")
        print("No files written.")
        return 0

    try:
        raw_data = fetch_bytes(CISA_KEV_URL)
        result = write_outputs(raw_data, args.limit)
    except urllib.error.URLError as exc:
        print(f"FAIL network error fetching CISA KEV: {exc}")
        return 2
    except json.JSONDecodeError as exc:
        print(f"FAIL invalid JSON from CISA KEV: {exc}")
        return 3
    except Exception as exc:
        print(f"FAIL unexpected error: {exc}")
        return 4

    print(f"PASS fetched records: {result.record_count}")
    print(f"retrieved_at_utc: {result.retrieved_at_utc}")
    print(f"raw_sha256: {result.raw_sha256}")
    print(f"raw_path: {result.raw_path}")
    print(f"summary_path: {result.summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
