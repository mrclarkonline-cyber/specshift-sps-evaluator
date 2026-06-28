#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPORT_ROOT = Path("reports/fast_relevance")

DEFAULT_FEEDS = {
    "bbc_world": "https://feeds.bbci.co.uk/news/world/rss.xml",
}

VERIFY_FIRST_FEEDS = {
    "reuters_verify_only": "https://www.reuters.com/tools/rss",
    "ap_verify_only": "https://apnews.com/rss",
}


@dataclass
class FetchResult:
    retrieved_at_utc: str
    source_name: str
    source_url: str
    raw_sha256: str
    raw_path: Path
    summary_path: Path
    json_path: Path
    record_count: int


def utc_now_slug() -> tuple[str, str]:
    now = datetime.now(timezone.utc)
    return now.isoformat().replace("+00:00", "Z"), now.strftime("%Y%m%dT%H%M%SZ")


def fetch_bytes(url: str, timeout: int = 30) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "SpecShiftLabsResearchWorkstation/0.1 ben@specshiftlabs.com",
            "Accept": "application/rss+xml, application/xml, text/xml, text/html",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def clean_text(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def text_at(parent: ET.Element, path: str) -> str:
    found = parent.find(path)
    if found is None or found.text is None:
        return ""
    return clean_text(found.text)


def parse_rss(raw_data: bytes, source_name: str, source_url: str) -> list[dict[str, Any]]:
    root = ET.fromstring(raw_data)
    channel = root.find("channel")
    if channel is None:
        raise ValueError("RSS channel element not found")

    records: list[dict[str, Any]] = []
    for item in channel.findall("item"):
        title = text_at(item, "title")
        link = text_at(item, "link")
        pub_date = text_at(item, "pubDate")
        description = text_at(item, "description")
        guid = text_at(item, "guid")

        records.append({
            "pipeline": "world_news_rss_fetch",
            "source_name": source_name,
            "source_url": source_url,
            "item_url": link,
            "guid": guid,
            "published_at": pub_date,
            "title": title,
            "summary": description,
            "source_tier": "tier_2_wire_or_reputable_news",
            "uncertainty_label": "single_source_preliminary",
            "claim_safety_note": "Single-source news item. Treat as preliminary until corroborated by independent sources or primary documentation.",
        })

    return records


def build_summary(records: list[dict[str, Any]], source_name: str, source_url: str, retrieved_at_utc: str, raw_sha256: str, raw_path: Path, json_path: Path, limit: int) -> str:
    lines: list[str] = []
    lines.append("# World News RSS Verification and Intake Digest")
    lines.append("")
    lines.append(f"Retrieved at UTC: {retrieved_at_utc}")
    lines.append(f"Source name: {source_name}")
    lines.append(f"Source URL: {source_url}")
    lines.append(f"Raw payload SHA256: {raw_sha256}")
    lines.append(f"Raw payload path: {raw_path}")
    lines.append(f"Parsed JSON path: {json_path}")
    lines.append(f"Record count: {len(records)}")
    lines.append("")
    lines.append("## Safety Boundary")
    lines.append("")
    lines.append("This digest is world-news awareness only.")
    lines.append("")
    lines.append("Single-source breaking news remains preliminary. Do not infer intent, cause, military meaning, financial action, legal conclusion, or validated truth from one feed item.")
    lines.append("")
    lines.append("## Latest Items")
    lines.append("")

    for idx, record in enumerate(records[:limit], start=1):
        lines.append(f"### {idx}. {record.get('title', 'unknown')}")
        lines.append("")
        lines.append(f"- Source: {record.get('source_name', 'unknown')}")
        lines.append(f"- Published: {record.get('published_at', 'unknown')}")
        if record.get("item_url"):
            lines.append(f"- URL: {record.get('item_url')}")
        if record.get("summary"):
            lines.append(f"- Source summary excerpt: {record.get('summary', '')[:700]}")
        lines.append("- Uncertainty label: single_source_preliminary")
        lines.append("- Source tier: tier_2_wire_or_reputable_news")
        lines.append("- Claim safety note: needs corroboration before high-confidence use")
        lines.append("")

    lines.append("## Claim Safety Note")
    lines.append("")
    lines.append("A world-news RSS item confirms that a source published an item. It does not by itself establish validated facts, cause, intent, or final event status.")
    lines.append("")
    return "\n".join(lines)


def write_outputs(raw_data: bytes, source_name: str, source_url: str, limit: int) -> FetchResult:
    retrieved_at_utc, slug = utc_now_slug()
    day = slug[:8]
    day_dir = REPORT_ROOT / f"{day[:4]}-{day[4:6]}-{day[6:8]}"
    raw_dir = day_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    raw_sha256 = sha256_bytes(raw_data)
    raw_path = raw_dir / f"world_news_{source_name}_{slug}.xml"
    json_path = raw_dir / f"world_news_{source_name}_{slug}.json"
    summary_path = day_dir / "world_news_rss.md"

    records = parse_rss(raw_data, source_name, source_url)

    raw_path.write_bytes(raw_data)
    json_path.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
    summary_path.write_text(build_summary(records, source_name, source_url, retrieved_at_utc, raw_sha256, raw_path, json_path, limit), encoding="utf-8")

    return FetchResult(retrieved_at_utc, source_name, source_url, raw_sha256, raw_path, summary_path, json_path, len(records))


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify/fetch public world-news RSS feeds.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verify-only", action="store_true", help="Do not fetch; print feed policy notes.")
    parser.add_argument("--feed", default="bbc_world", choices=sorted(DEFAULT_FEEDS.keys()))
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    if args.limit < 1:
        print("FAIL --limit must be >= 1")
        return 1

    source_name = args.feed
    source_url = DEFAULT_FEEDS[source_name]

    print("=== World News RSS Fetch ===")
    print(f"source_name: {source_name}")
    print(f"source_url: {source_url}")
    print("mode: dry-run" if args.dry_run else "mode: live-fetch")
    print("safety: single-source news remains preliminary")

    if args.verify_only:
        print("PASS verify-only notes")
        print("BBC World RSS is the initial build feed.")
        print("Reuters/AP are marked verify-first because feed locations and access patterns can change.")
        for name, url in VERIFY_FIRST_FEEDS.items():
            print(f"verify_first: {name} -> {url}")
        print("No network calls performed.")
        print("No files written.")
        return 0

    if args.dry_run:
        print("PASS dry-run configuration")
        print("No network calls performed.")
        print("No files written.")
        return 0

    try:
        raw_data = fetch_bytes(source_url)
        result = write_outputs(raw_data, source_name, source_url, args.limit)
    except urllib.error.URLError as exc:
        print(f"FAIL network error fetching world news RSS: {exc}")
        return 2
    except ET.ParseError as exc:
        print(f"FAIL invalid RSS/XML from world news feed: {exc}")
        return 3
    except Exception as exc:
        print(f"FAIL unexpected error: {exc}")
        return 4

    print(f"PASS fetched records: {result.record_count}")
    print(f"retrieved_at_utc: {result.retrieved_at_utc}")
    print(f"raw_sha256: {result.raw_sha256}")
    print(f"raw_path: {result.raw_path}")
    print(f"json_path: {result.json_path}")
    print(f"summary_path: {result.summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
