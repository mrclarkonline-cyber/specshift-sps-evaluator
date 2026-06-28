#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
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

HEALTH_FIELDS = [
    "last_successful_fetch",
    "last_failure",
    "failure_count",
    "format_valid",
    "rate_limited",
    "status",
]


@dataclass
class SourceHealth:
    source_id: str
    registry_present: bool
    planned_status: str
    health_status: str
    notes: str


def section_for_source(text: str, source_id: str) -> str:
    marker = f"### {source_id}"
    start = text.find(marker)
    if start == -1:
        return ""
    next_start = text.find("\n### ", start + len(marker))
    if next_start == -1:
        return text[start:]
    return text[start:next_start]


def extract_status(section: str) -> str:
    lines = section.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "Status:" and i + 1 < len(lines):
            return lines[i + 1].strip()
    return "unknown"


def main() -> int:
    print("=== Source Health Check ===")

    if not REGISTRY_PATH.exists():
        print(f"FAIL missing registry: {REGISTRY_PATH}")
        return 1

    text = REGISTRY_PATH.read_text(encoding="utf-8")
    results: list[SourceHealth] = []

    for source_id in REQUIRED_SOURCES:
        section = section_for_source(text, source_id)
        if not section:
            results.append(SourceHealth(
                source_id=source_id,
                registry_present=False,
                planned_status="missing",
                health_status="failing",
                notes="Source is missing from registry.",
            ))
            continue

        planned_status = extract_status(section)
        if "ready" in planned_status.lower():
            health_status = "registered_ready"
        elif "verify" in planned_status.lower():
            health_status = "registered_verify_before_build"
        else:
            health_status = "registered_unknown_status"

        results.append(SourceHealth(
            source_id=source_id,
            registry_present=True,
            planned_status=planned_status,
            health_status=health_status,
            notes="Local registry-only check. No network fetch performed.",
        ))

    failures = [r for r in results if not r.registry_present]

    for r in results:
        print(f"{r.source_id}: {r.health_status} | planned_status={r.planned_status}")

    print()
    print("Health fields reserved for future live fetch stage:")
    for field in HEALTH_FIELDS:
        print(f"- {field}")

    print()
    print("No network calls performed.")
    print("No credentials required.")
    print("No source files mutated.")

    if failures:
        print()
        print("FAIL missing registry sources:")
        for r in failures:
            print(f"- {r.source_id}")
        return 1

    print()
    print("PASS source health registry baseline")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
