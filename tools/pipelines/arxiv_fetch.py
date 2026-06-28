#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ARXIV_API_URL = "https://export.arxiv.org/api/query"
REPORT_ROOT = Path("reports/fast_relevance")

ATOM_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}


@dataclass
class FetchResult:
    retrieved_at_utc: str
    source_url: str
    raw_sha256: str
    raw_path: Path
    summary_path: Path
    json_path: Path
    record_count: int


def utc_now_slug() -> tuple[str, str]:
    now = datetime.now(timezone.utc)
    iso = now.isoformat().replace("+00:00", "Z")
    slug = now.strftime("%Y%m%dT%H%M%SZ")
    return iso, slug


def build_query(categories: list[str], search_term: str | None) -> str:
    category_query = "+OR+".join(f"cat:{cat}" for cat in categories)
    if search_term:
        term = urllib.parse.quote(search_term)
        return f"({category_query})+AND+all:{term}"
    return category_query


def build_url(categories: list[str], max_results: int, search_term: str | None) -> str:
    params = {
        "search_query": build_query(categories, search_term),
        "start": "0",
        "max_results": str(max_results),
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    return ARXIV_API_URL + "?" + urllib.parse.urlencode(params)


def fetch_bytes(url: str, timeout: int = 30) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "SpecShiftLabsResearchWorkstation/0.1 ben@specshiftlabs.com",
            "Accept": "application/atom+xml, application/xml, text/xml",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def text_or_empty(element: ET.Element | None) -> str:
    if element is None or element.text is None:
        return ""
    return html.unescape(element.text).strip()


def clean_text(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return value


def parse_entries(raw_data: bytes) -> list[dict[str, Any]]:
    root = ET.fromstring(raw_data)
    entries = []

    for entry in root.findall("atom:entry", ATOM_NS):
        title = clean_text(text_or_empty(entry.find("atom:title", ATOM_NS)))
        summary = clean_text(text_or_empty(entry.find("atom:summary", ATOM_NS)))
        published = text_or_empty(entry.find("atom:published", ATOM_NS))
        updated = text_or_empty(entry.find("atom:updated", ATOM_NS))
        arxiv_id_url = text_or_empty(entry.find("atom:id", ATOM_NS))
        arxiv_id = arxiv_id_url.rsplit("/", 1)[-1] if arxiv_id_url else "unknown"

        authors = []
        for author in entry.findall("atom:author", ATOM_NS):
            name = text_or_empty(author.find("atom:name", ATOM_NS))
            if name:
                authors.append(name)

        categories = []
        for category in entry.findall("atom:category", ATOM_NS):
            term = category.attrib.get("term", "")
            if term:
                categories.append(term)

        links = []
        for link in entry.findall("atom:link", ATOM_NS):
            href = link.attrib.get("href", "")
            rel = link.attrib.get("rel", "")
            link_type = link.attrib.get("type", "")
            if href:
                links.append({"href": href, "rel": rel, "type": link_type})

        doi = text_or_empty(entry.find("arxiv:doi", ATOM_NS))
        journal_ref = text_or_empty(entry.find("arxiv:journal_ref", ATOM_NS))
        comment = text_or_empty(entry.find("arxiv:comment", ATOM_NS))

        entries.append({
            "arxiv_id": arxiv_id,
            "source_url": arxiv_id_url,
            "title": title,
            "authors": authors,
            "summary": summary,
            "published": published,
            "updated": updated,
            "categories": categories,
            "doi": doi,
            "journal_ref": journal_ref,
            "comment": comment,
            "links": links,
            "source_tier": "tier_3_preprint",
            "uncertainty_label": "preprint_not_peer_reviewed",
            "claim_safety_note": "arXiv record is a preprint/discovery record; do not treat as peer-reviewed or validated conclusion.",
        })

    return entries


def build_summary(
    entries: list[dict[str, Any]],
    raw_sha256: str,
    source_url: str,
    retrieved_at_utc: str,
    raw_path: Path,
    json_path: Path,
    limit: int,
) -> str:
    lines: list[str] = []
    lines.append("# arXiv Research Intake Digest")
    lines.append("")
    lines.append(f"Retrieved at UTC: {retrieved_at_utc}")
    lines.append(f"Source query: {source_url}")
    lines.append(f"Raw payload SHA256: {raw_sha256}")
    lines.append(f"Raw payload path: {raw_path}")
    lines.append(f"Parsed JSON path: {json_path}")
    lines.append(f"Record count: {len(entries)}")
    lines.append("")
    lines.append("## Safety Boundary")
    lines.append("")
    lines.append("This digest is research awareness only.")
    lines.append("")
    lines.append("arXiv records are preprints or repository records unless otherwise documented. Do not treat these entries as peer-reviewed, replicated, validated conclusions, product claims, safety claims, medical advice, or legal advice.")
    lines.append("")
    lines.append("## Latest arXiv Records")
    lines.append("")

    for idx, record in enumerate(entries[:limit], start=1):
        title = record.get("title", "unknown")
        arxiv_id = record.get("arxiv_id", "unknown")
        source_record_url = record.get("source_url", "")
        authors = record.get("authors", [])
        categories = record.get("categories", [])
        published = record.get("published", "unknown")
        updated = record.get("updated", "unknown")
        doi = record.get("doi", "")
        journal_ref = record.get("journal_ref", "")
        comment = record.get("comment", "")
        summary = record.get("summary", "")

        author_label = "; ".join(authors[:8]) if isinstance(authors, list) and authors else "unknown"
        category_label = ", ".join(categories) if isinstance(categories, list) and categories else "unknown"

        lines.append(f"### {idx}. {title}")
        lines.append("")
        lines.append(f"- arXiv ID: {arxiv_id}")
        if source_record_url:
            lines.append(f"- arXiv URL: {source_record_url}")
        lines.append(f"- Authors: {author_label}")
        lines.append(f"- Categories: {category_label}")
        lines.append(f"- Published: {published}")
        lines.append(f"- Updated: {updated}")
        if doi:
            lines.append(f"- DOI: {doi}")
        if journal_ref:
            lines.append(f"- Journal reference: {journal_ref}")
        if comment:
            lines.append(f"- Comment: {comment}")
        if summary:
            lines.append(f"- Abstract summary excerpt: {summary[:900]}")
        lines.append("- Uncertainty label: preprint_not_peer_reviewed")
        lines.append("- Source tier: tier_3_preprint")
        lines.append("- Claim safety note: discovery/preprint record only; not validated conclusion")
        lines.append("")

    lines.append("## Claim Safety Note")
    lines.append("")
    lines.append("An arXiv item confirms that an author-submitted research record exists in arXiv. It does not by itself establish correctness, peer review, replication, production readiness, scientific consensus, safety, or commercial validity.")
    lines.append("")

    return "\n".join(lines)


def write_outputs(raw_data: bytes, source_url: str, limit: int) -> FetchResult:
    retrieved_at_utc, slug = utc_now_slug()
    day = slug[:8]
    day_dir = REPORT_ROOT / f"{day[:4]}-{day[4:6]}-{day[6:8]}"
    raw_dir = day_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    raw_sha256 = sha256_bytes(raw_data)
    raw_path = raw_dir / f"arxiv_{slug}.xml"
    json_path = raw_dir / f"arxiv_{slug}.json"
    summary_path = day_dir / "research_arxiv.md"

    entries = parse_entries(raw_data)

    raw_path.write_bytes(raw_data)
    json_path.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")

    summary = build_summary(
        entries=entries,
        raw_sha256=raw_sha256,
        source_url=source_url,
        retrieved_at_utc=retrieved_at_utc,
        raw_path=raw_path,
        json_path=json_path,
        limit=limit,
    )
    summary_path.write_text(summary, encoding="utf-8")

    return FetchResult(
        retrieved_at_utc=retrieved_at_utc,
        source_url=source_url,
        raw_sha256=raw_sha256,
        raw_path=raw_path,
        summary_path=summary_path,
        json_path=json_path,
        record_count=len(entries),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch arXiv records for research awareness.")
    parser.add_argument("--dry-run", action="store_true", help="Validate configuration without network fetch.")
    parser.add_argument("--limit", type=int, default=10, help="Number of arXiv records to summarize.")
    parser.add_argument("--categories", default="cs.AI,cs.LG,cs.CL,cs.CR,stat.ML", help="Comma-separated arXiv categories.")
    parser.add_argument("--search-term", default=None, help="Optional search term.")
    args = parser.parse_args()

    if args.limit < 1:
        print("FAIL --limit must be >= 1")
        return 1

    categories = [cat.strip() for cat in args.categories.split(",") if cat.strip()]
    if not categories:
        print("FAIL at least one category is required")
        return 1

    source_url = build_url(categories, args.limit, args.search_term)

    print("=== arXiv Fetch ===")
    print(f"source_url: {source_url}")
    print(f"categories: {', '.join(categories)}")
    print("mode: dry-run" if args.dry_run else "mode: live-fetch")
    print("safety: research awareness only; preprints are not validated conclusions")

    if args.dry_run:
        print("PASS dry-run configuration")
        print("No network calls performed.")
        print("No files written.")
        return 0

    try:
        raw_data = fetch_bytes(source_url)
        result = write_outputs(raw_data, source_url, args.limit)
    except urllib.error.URLError as exc:
        print(f"FAIL network error fetching arXiv: {exc}")
        return 2
    except ET.ParseError as exc:
        print(f"FAIL invalid Atom/XML from arXiv: {exc}")
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
