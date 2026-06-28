#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SEC_COMPANY_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
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
    return now.isoformat().replace("+00:00", "Z"), now.strftime("%Y%m%dT%H%M%SZ")


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


def cik_padded(cik: Any) -> str:
    try:
        return str(int(cik)).zfill(10)
    except Exception:
        return str(cik)


def ticker_records(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        raise ValueError("SEC ticker payload is not a dict")
    records = []
    for _, value in payload.items():
        if isinstance(value, dict):
            records.append(value)
    return records


def build_summary(records: list[dict[str, Any]], raw_sha256: str, source_url: str, retrieved_at_utc: str, raw_path: Path, limit: int) -> str:
    lines: list[str] = []
    lines.append("# SEC EDGAR Basic Company Ticker Digest")
    lines.append("")
    lines.append(f"Retrieved at UTC: {retrieved_at_utc}")
    lines.append(f"Source: {source_url}")
    lines.append(f"Raw payload SHA256: {raw_sha256}")
    lines.append(f"Raw payload path: {raw_path}")
    lines.append(f"Record count: {len(records)}")
    lines.append("")
    lines.append("## Safety Boundary")
    lines.append("")
    lines.append("This digest is public SEC company metadata awareness only.")
    lines.append("")
    lines.append("Do not treat this as investment advice, trading signal generation, valuation analysis, or legal/compliance determination.")
    lines.append("")
    lines.append("## Sample SEC Ticker Records")
    lines.append("")

    for idx, record in enumerate(records[:limit], start=1):
        cik = cik_padded(record.get("cik_str", "unknown"))
        ticker = str(record.get("ticker", "unknown")).strip()
        title = str(record.get("title", "unknown")).strip()
        submissions_url = f"https://data.sec.gov/submissions/CIK{cik}.json"

        lines.append(f"### {idx}. {ticker}")
        lines.append("")
        lines.append(f"- Company: {title}")
        lines.append(f"- Ticker: {ticker}")
        lines.append(f"- CIK: {cik}")
        lines.append(f"- SEC submissions JSON: {submissions_url}")
        lines.append("- Uncertainty label: official_sec_company_metadata")
        lines.append("- Source tier: tier_1_authoritative")
        lines.append("- Claim safety note: metadata only; no investment, legal, or trading conclusion")
        lines.append("")

    lines.append("## Claim Safety Note")
    lines.append("")
    lines.append("SEC EDGAR company metadata confirms public filing identifiers and links. It does not establish investment value, business quality, compliance status, or trading action.")
    lines.append("")
    return "\n".join(lines)


def write_outputs(raw_data: bytes, source_url: str, limit: int) -> FetchResult:
    retrieved_at_utc, slug = utc_now_slug()
    day = slug[:8]
    day_dir = REPORT_ROOT / f"{day[:4]}-{day[4:6]}-{day[6:8]}"
    raw_dir = day_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    raw_sha256 = sha256_bytes(raw_data)
    raw_path = raw_dir / f"sec_company_tickers_{slug}.json"
    summary_path = day_dir / "finance_sec_edgar_basic.md"

    payload = json.loads(raw_data.decode("utf-8"))
    records = ticker_records(payload)

    raw_path.write_bytes(raw_data)
    summary_path.write_text(build_summary(records, raw_sha256, source_url, retrieved_at_utc, raw_path, limit), encoding="utf-8")

    return FetchResult(retrieved_at_utc, source_url, raw_sha256, raw_path, summary_path, len(records))


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch SEC EDGAR company ticker metadata.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    print("=== SEC EDGAR Basic Metadata Fetch ===")
    print(f"source_url: {SEC_COMPANY_TICKERS_URL}")
    print("mode: dry-run" if args.dry_run else "mode: live-fetch")
    print("safety: public filing metadata only; no investment advice")

    if args.limit < 1:
        print("FAIL --limit must be >= 1")
        return 1

    if args.dry_run:
        print("PASS dry-run configuration")
        print("No network calls performed.")
        print("No files written.")
        return 0

    try:
        raw_data = fetch_bytes(SEC_COMPANY_TICKERS_URL)
        result = write_outputs(raw_data, SEC_COMPANY_TICKERS_URL, args.limit)
    except urllib.error.URLError as exc:
        print(f"FAIL network error fetching SEC metadata: {exc}")
        return 2
    except json.JSONDecodeError as exc:
        print(f"FAIL invalid JSON from SEC metadata: {exc}")
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
