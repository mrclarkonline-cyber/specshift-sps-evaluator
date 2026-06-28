#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPORT_ROOT = Path("reports/fast_relevance")

NUMERIC_PATTERN = re.compile(r"\b\d+(?:,\d{3})*(?:\.\d+)?\b")
ENTITY_HINT_PATTERN = re.compile(
    r"\b(?:CVE-\d{4}-\d+|[A-Z][A-Za-z0-9&.\-]+(?:\s+[A-Z][A-Za-z0-9&.\-]+){0,4})\b"
)

SKIP_FILES = {
    "daily_digest.md",
    "specshift_buyer_triggers.md",
    "finance_integrity_watch.md",
    "contradiction_watch.md",
}


def today_dir() -> Path:
    return REPORT_ROOT / datetime.now(timezone.utc).strftime("%Y-%m-%d")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def collect_markdown(day_dir: Path) -> list[Path]:
    if not day_dir.exists():
        return []
    return sorted(p for p in day_dir.glob("*.md") if p.name not in SKIP_FILES)


def source_label(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("Source name:"):
            return stripped.split(":", 1)[1].strip()
        if stripped.startswith("Source:"):
            return stripped.split(":", 1)[1].strip()
        if stripped.startswith("Source query:"):
            return stripped.split(":", 1)[1].strip()
    return fallback


def title_label(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
        if stripped.startswith("### "):
            return stripped[4:].strip()
    return fallback


def extract_entities(text: str) -> set[str]:
    candidates = set()
    for match in ENTITY_HINT_PATTERN.findall(text):
        cleaned = match.strip()
        if len(cleaned) < 3:
            continue
        if cleaned.lower() in {
            "source",
            "retrieved",
            "safety",
            "boundary",
            "claim",
            "note",
            "unknown",
            "digest",
            "record",
            "records",
        }:
            continue
        candidates.add(cleaned)
    return candidates


def extract_numbers(text: str) -> set[str]:
    return set(NUMERIC_PATTERN.findall(text))


def source_tier(text: str) -> str:
    lowered = text.lower()
    if "tier_1_authoritative" in lowered:
        return "tier_1_authoritative"
    if "tier_2" in lowered:
        return "tier_2"
    if "tier_3" in lowered:
        return "tier_3"
    if "tier_4" in lowered:
        return "tier_4"
    return "unknown"


def uncertainty_label(text: str) -> str:
    for line in text.splitlines():
        lowered = line.lower()
        if "uncertainty label" in lowered:
            return line.strip()
    return "uncertainty label: unknown"


def build_report(day_dir: Path, min_shared_entities: int) -> Path:
    day_dir.mkdir(parents=True, exist_ok=True)
    output = day_dir / "contradiction_watch.md"

    files = collect_markdown(day_dir)
    records = []

    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        records.append({
            "path": path,
            "text": text,
            "title": title_label(text, path.name),
            "source": source_label(text, path.name),
            "tier": source_tier(text),
            "uncertainty": uncertainty_label(text),
            "entities": extract_entities(text),
            "numbers": extract_numbers(text),
        })

    candidates = []
    for i, left in enumerate(records):
        for right in records[i + 1:]:
            if left["path"] == right["path"]:
                continue

            shared_entities = sorted(left["entities"] & right["entities"])
            if len(shared_entities) < min_shared_entities:
                continue

            left_numbers = left["numbers"]
            right_numbers = right["numbers"]
            shared_numbers = left_numbers & right_numbers
            left_only_numbers = left_numbers - right_numbers
            right_only_numbers = right_numbers - left_numbers

            divergence_notes = []
            if left_only_numbers or right_only_numbers:
                divergence_notes.append("numeric_variance")
            if left["tier"] != right["tier"]:
                divergence_notes.append("source_tier_difference")
            if left["uncertainty"] != right["uncertainty"]:
                divergence_notes.append("uncertainty_label_difference")

            if not divergence_notes:
                divergence_notes.append("shared_entity_overlap_no_direct_conflict")

            candidates.append({
                "left": left,
                "right": right,
                "shared_entities": shared_entities[:15],
                "shared_numbers": sorted(shared_numbers)[:15],
                "left_only_numbers": sorted(left_only_numbers)[:15],
                "right_only_numbers": sorted(right_only_numbers)[:15],
                "divergence_notes": divergence_notes,
            })

    lines: list[str] = []
    lines.append("# Multi-Source Contradiction Watch")
    lines.append("")
    lines.append(f"Generated at UTC: {utc_now()}")
    lines.append(f"Report folder: {day_dir}")
    lines.append("")
    lines.append("## Safety Boundary")
    lines.append("")
    lines.append("This output flags unresolved variance or anomaly for review; it does not establish cause, intent, origin, or validated conclusion.")
    lines.append("")
    lines.append("The contradiction detector does not pick a winner. It only surfaces possible divergence, overlap, or uncertainty differences for human review.")
    lines.append("")
    lines.append("## Method")
    lines.append("")
    lines.append("- Scans local generated markdown digests only.")
    lines.append("- Extracts rough entity and numeric overlaps.")
    lines.append("- Flags numeric variance, source-tier differences, and uncertainty-label differences.")
    lines.append("- Does not fetch network data.")
    lines.append("- Does not mutate source digests.")
    lines.append("")
    lines.append("## Candidate Divergence / Friction Items")
    lines.append("")

    if not candidates:
        lines.append("No candidate contradiction or source-friction items met the current threshold.")
        lines.append("")
    else:
        for idx, item in enumerate(candidates[:30], start=1):
            left = item["left"]
            right = item["right"]

            lines.append(f"### {idx}. Candidate source friction")
            lines.append("")
            lines.append(f"- Left source digest: {left['path']}")
            lines.append(f"- Left title: {left['title']}")
            lines.append(f"- Left source: {left['source']}")
            lines.append(f"- Left tier: {left['tier']}")
            lines.append(f"- Left uncertainty: {left['uncertainty']}")
            lines.append(f"- Right source digest: {right['path']}")
            lines.append(f"- Right title: {right['title']}")
            lines.append(f"- Right source: {right['source']}")
            lines.append(f"- Right tier: {right['tier']}")
            lines.append(f"- Right uncertainty: {right['uncertainty']}")
            lines.append(f"- Shared entities: {', '.join(item['shared_entities']) if item['shared_entities'] else 'none'}")
            lines.append(f"- Shared numbers: {', '.join(item['shared_numbers']) if item['shared_numbers'] else 'none'}")
            lines.append(f"- Left-only numbers: {', '.join(item['left_only_numbers']) if item['left_only_numbers'] else 'none'}")
            lines.append(f"- Right-only numbers: {', '.join(item['right_only_numbers']) if item['right_only_numbers'] else 'none'}")
            lines.append(f"- Divergence notes: {', '.join(item['divergence_notes'])}")
            lines.append("- Claim safety note: unresolved variance only; human review required.")
            lines.append("")

    lines.append("## Forbidden Conclusions")
    lines.append("")
    lines.append("- Do not call a source false based only on this report.")
    lines.append("- Do not call a source true based only on this report.")
    lines.append("- Do not label disagreement as misinformation by default.")
    lines.append("- Do not infer intent, cause, concealment, fraud, or manipulation.")
    lines.append("- Do not promote unresolved variance to validated conclusion.")
    lines.append("")
    lines.append("## Kira Recommendation")
    lines.append("")
    lines.append("Use this report as an epistemic friction board. The correct next move is source review, not conclusion.")
    lines.append("")

    output.write_text("\n".join(lines), encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate multi-source contradiction/friction watch from local digests.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--day-dir", default=None)
    parser.add_argument("--min-shared-entities", type=int, default=1)
    args = parser.parse_args()

    target = Path(args.day_dir) if args.day_dir else today_dir()

    print("=== Multi-Source Contradiction Detector ===")
    print(f"target_dir: {target}")
    print(f"min_shared_entities: {args.min_shared_entities}")
    print("mode: dry-run" if args.dry_run else "mode: generate")
    print("safety: unresolved variance only; no automated truth adjudication")

    if args.min_shared_entities < 1:
        print("FAIL --min-shared-entities must be >= 1")
        return 1

    if args.dry_run:
        print("PASS dry-run configuration")
        print("No files written.")
        return 0

    output = build_report(target, args.min_shared_entities)
    print(f"PASS wrote contradiction watch: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
