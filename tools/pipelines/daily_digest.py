#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

REPORT_ROOT = Path("reports/fast_relevance")

DIGEST_SECTIONS = [
    ("Critical Security", "cybersecurity"),
    ("AI / Technical Releases", "ai_models"),
    ("Research Literature", "research"),
    ("Policy and Regulatory", "policy"),
    ("Financial / Corporate Filings", "finance"),
    ("Earth / Space / Infrastructure", "earth"),
    ("World News", "world_news"),
]


def today_dir() -> Path:
    now = datetime.now(timezone.utc)
    return REPORT_ROOT / now.strftime("%Y-%m-%d")


def read_matching(day_dir: Path, key: str) -> list[Path]:
    return sorted(p for p in day_dir.glob(f"*{key}*.md") if p.name != "daily_digest.md")


def make_digest(day_dir: Path) -> Path:
    day_dir.mkdir(parents=True, exist_ok=True)
    output = day_dir / "daily_digest.md"
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    lines: list[str] = []
    lines.append("# SpecShift Fast Relevance Daily Digest")
    lines.append("")
    lines.append(f"Generated at UTC: {now}")
    lines.append(f"Report folder: {day_dir}")
    lines.append("")
    lines.append("## Safety Boundary")
    lines.append("")
    lines.append("This digest is triage and awareness only. It preserves source provenance and uncertainty labels. It does not establish cause, intent, legal obligation, medical guidance, investment advice, or validated scientific conclusion.")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append("")
    lines.append("Review the sections below. Items remain bounded by their source tier and uncertainty labels.")
    lines.append("")

    for section_title, key in DIGEST_SECTIONS:
        lines.append(f"## {section_title}")
        lines.append("")
        matches = read_matching(day_dir, key)
        if not matches:
            lines.append("No generated source digest found for this section yet.")
            lines.append("")
            continue
        for path in matches:
            lines.append(f"- Source digest: {path}")
        lines.append("")

    lines.append("## Epistemic Friction")
    lines.append("")
    lines.append("Contradiction detection is not active yet. Treat single-source items as preliminary.")
    lines.append("")
    lines.append("## Pipeline Health")
    lines.append("")
    lines.append("Use tools/status/pipeline_progress.py and tools/pipelines/source_health_check.py for current pipeline status.")
    lines.append("")
    lines.append("## Claim Safety")
    lines.append("")
    lines.append("Run:")
    lines.append("")
    lines.append("python3 tools/pipelines/claim_safety_gate.py --path reports/fast_relevance")
    lines.append("")

    output.write_text("\n".join(lines), encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate daily digest from local generated source digests.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--day-dir", default=None, help="Optional report day directory.")
    args = parser.parse_args()

    print("=== Daily Digest Generator ===")
    print("mode: dry-run" if args.dry_run else "mode: generate")
    print("safety: digest is awareness only; no conclusion promotion")

    target = Path(args.day_dir) if args.day_dir else today_dir()
    print(f"target_dir: {target}")

    if args.dry_run:
        print("PASS dry-run configuration")
        print("No files written.")
        return 0

    output = make_digest(target)
    print(f"PASS wrote digest: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
