#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone, date, timedelta
from pathlib import Path
from typing import Any

FEDREG_API_URL = "https://www.federalregister.gov/api/v1/documents.json"
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


def build_url(days: int, per_page: int, search_term: str | None) -> str:
    start_date = (date.today() - timedelta(days=days)).isoformat()
    params: dict[str, Any] = {
        "per_page": str(per_page),
        "order": "newest",
        "conditions[publication_date][gte]": start_date,
        "conditions[type][]": ["RULE", "PRORULE", "NOTICE"],
    }
    if search_term:
        params["conditions[term]"] = search_term

    return FEDREG_API_URL + "?" + urllib.parse.urlencode(params, doseq=True)


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


def result_records(payload: dict[str, Any]) -> list[dict[str, Any]]:
    results = payload.get("results", [])
    if not isinstance(results, list):
        raise ValueError("Federal Register payload field 'results' is not a list")
    return [r for r in results if isinstance(r, dict)]


def normalize_action(record: dict[str, Any]) -> str:
    doc_type = safe_get(record, "type", "unknown")
    action = safe_get(record, "action", "")
    if action:
        return f"{doc_type}: {action}"
    return doc_type


def build_summary(
    payload: dict[str, Any],
    raw_sha256: str,
    source_url: str,
    retrieved_at_utc: str,
    raw_path: Path,
    limit: int,
) -> str:
    records = result_records(payload)
    count = len(records)
    total_pages = payload.get("total_pages", "unknown")
    total_count = payload.get("count", "unknown")

    lines: list[str] = []
    lines.append("# Federal Register Policy Intake Digest")
    lines.append("")
    lines.append(f"Retrieved at UTC: {retrieved_at_utc}")
    lines.append(f"Source query: {source_url}")
    lines.append(f"Raw payload SHA256: {raw_sha256}")
    lines.append(f"Raw payload path: {raw_path}")
    lines.append(f"Returned record count: {count}")
    lines.append(f"API reported count: {total_count}")
    lines.append(f"API total pages: {total_pages}")
    lines.append("")
    lines.append("## Safety Boundary")
    lines.append("")
    lines.append("This digest is official public policy/regulatory awareness only.")
    lines.append("")
    lines.append("Do not treat this summary as legal advice. Link back to the primary Federal Register document for actual text, status, dates, and obligations.")
    lines.append("")
    lines.append("## Latest Federal Register Records")
    lines.append("")

    for idx, record in enumerate(records[:limit], start=1):
        title = safe_get(record, "title", "unknown")
        doc_type = safe_get(record, "type", "unknown")
        publication_date = safe_get(record, "publication_date", "unknown")
        effective_on = safe_get(record, "effective_on", "")
        comment_url = safe_get(record, "comments_close_on", "")
        agency_names = record.get("agencies", [])
        agency_label = "unknown"
        if isinstance(agency_names, list) and agency_names:
            agency_bits = []
            for agency in agency_names:
                if isinstance(agency, dict):
                    name = safe_get(agency, "name", "")
                    if name:
                        agency_bits.append(name)
            if agency_bits:
                agency_label = "; ".join(agency_bits)

        html_url = safe_get(record, "html_url", "")
        pdf_url = safe_get(record, "pdf_url", "")
        abstract = safe_get(record, "abstract", "")
        action = normalize_action(record)

        lines.append(f"### {idx}. {title}")
        lines.append("")
        lines.append(f"- Type/action: {action}")
        lines.append(f"- Publication date: {publication_date}")
        if effective_on:
            lines.append(f"- Effective on: {effective_on}")
        if comment_url:
            lines.append(f"- Comments close on: {comment_url}")
        lines.append(f"- Agency: {agency_label}")
        if html_url:
            lines.append(f"- Federal Register HTML: {html_url}")
        if pdf_url:
            lines.append(f"- Federal Register PDF: {pdf_url}")
        if abstract:
            lines.append(f"- Source abstract: {abstract[:600]}")
        lines.append("- Uncertainty label: institutional_source_policy_record")
        lines.append("- Source tier: tier_1_authoritative")
        lines.append("- Claim safety note: agency/publication record only; not legal advice")
        lines.append("")

    lines.append("## Claim Safety Note")
    lines.append("")
    lines.append("A Federal Register item confirms a public federal document record. It does not by itself establish how the rule applies to a specific person, company, product, workflow, or jurisdiction without legal review.")
    lines.append("")

    return "\n".join(lines)


def write_outputs(raw_data: bytes, source_url: str, limit: int) -> FetchResult:
    retrieved_at_utc, slug = utc_now_slug()
    day = slug[:8]
    day_dir = REPORT_ROOT / f"{day[:4]}-{day[4:6]}-{day[6:8]}"
    raw_dir = day_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    raw_sha256 = sha256_bytes(raw_data)
    raw_path = raw_dir / f"federal_register_{slug}.json"
    summary_path = day_dir / "policy_federal_register.md"

    payload = json.loads(raw_data.decode("utf-8"))
    records = result_records(payload)

    raw_path.write_bytes(raw_data)
    summary = build_summary(
        payload=payload,
        raw_sha256=raw_sha256,
        source_url=source_url,
        retrieved_at_utc=retrieved_at_utc,
        raw_path=raw_path,
        limit=limit,
    )
    summary_path.write_text(summary, encoding="utf-8")

    return FetchResult(
        retrieved_at_utc=retrieved_at_utc,
        source_url=source_url,
        raw_sha256=raw_sha256,
        raw_path=raw_path,
        summary_path=summary_path,
        record_count=len(records),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch Federal Register records for policy awareness.")
    parser.add_argument("--dry-run", action="store_true", help="Validate configuration without network fetch.")
    parser.add_argument("--limit", type=int, default=10, help="Number of Federal Register records to summarize.")
    parser.add_argument("--days", type=int, default=7, help="Look back this many days.")
    parser.add_argument("--search-term", default=None, help="Optional search term.")
    args = parser.parse_args()

    if args.limit < 1:
        print("FAIL --limit must be >= 1")
        return 1
    if args.days < 1:
        print("FAIL --days must be >= 1")
        return 1

    per_page = max(args.limit, 10)
    source_url = build_url(args.days, per_page, args.search_term)

    print("=== Federal Register Fetch ===")
    print(f"source_url: {source_url}")
    print("mode: dry-run" if args.dry_run else "mode: live-fetch")
    print("safety: policy awareness only, not legal advice")

    if args.dry_run:
        print("PASS dry-run configuration")
        print("No network calls performed.")
        print("No files written.")
        return 0

    try:
        raw_data = fetch_bytes(source_url)
        result = write_outputs(raw_data, source_url, args.limit)
    except urllib.error.URLError as exc:
        print(f"FAIL network error fetching Federal Register: {exc}")
        return 2
    except json.JSONDecodeError as exc:
        print(f"FAIL invalid JSON from Federal Register: {exc}")
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
