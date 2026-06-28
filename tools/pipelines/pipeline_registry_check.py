#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

REGISTRY_PATH = Path("docs/workstation/minimum_viable_source_registry.md")

REQUIRED_SOURCES = [
    "cisa_kev",
    "usgs_earthquake",
    "federal_register",
    "arxiv",
    "noaa_alerts",
    "huggingface_metadata",
    "sec_edgar",
    "bbc_world_rss",
    "reuters_ap_rss",
]

REQUIRED_FIELDS = [
    "Name:",
    "Tier:",
    "Category:",
    "Access:",
    "Key required:",
    "Format:",
    "Cadence:",
    "Guardrails:",
    "Status:",
]


def section_for_source(text: str, source_id: str) -> str:
    marker = f"### {source_id}"
    start = text.find(marker)
    if start == -1:
        return ""
    next_start = text.find("\n### ", start + len(marker))
    if next_start == -1:
        return text[start:]
    return text[start:next_start]


def main() -> int:
    print("=== Pipeline Registry Check ===")

    if not REGISTRY_PATH.exists():
        print(f"FAIL missing registry: {REGISTRY_PATH}")
        return 1

    text = REGISTRY_PATH.read_text(encoding="utf-8")
    failures: list[str] = []

    for source_id in REQUIRED_SOURCES:
        section = section_for_source(text, source_id)
        if not section:
            failures.append(f"missing source section: {source_id}")
            continue

        for field in REQUIRED_FIELDS:
            if field not in section:
                failures.append(f"{source_id}: missing field {field}")

    if failures:
        print("FAIL registry validation")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"PASS registry exists: {REGISTRY_PATH}")
    print(f"PASS required sources: {len(REQUIRED_SOURCES)}")
    print(f"PASS required fields per source: {len(REQUIRED_FIELDS)}")
    print("No network calls performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
