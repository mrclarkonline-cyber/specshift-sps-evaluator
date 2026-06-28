#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import re

REPORT_ROOT = Path("reports/fast_relevance")

TRIGGER_KEYWORDS = [
    "agent",
    "automation",
    "workflow",
    "reliability",
    "incident",
    "postmortem",
    "failure",
    "audit",
    "governance",
    "approval",
    "permission",
    "reconciliation",
    "settlement",
    "ledger",
    "false completion",
    "autonomous",
    "handoff",
    "escalation",
    "compliance",
]

BUYER_ROLE_HINTS = [
    "VP Engineering",
    "Head of Product",
    "CTO",
    "Head of AI",
    "Head of Reliability",
    "Head of Risk",
    "Head of Operations",
    "Head of Finance Operations",
    "Principal Engineer",
    "Platform Engineering Lead",
]


def today_dir() -> Path:
    now = datetime.now(timezone.utc)
    return REPORT_ROOT / now.strftime("%Y-%m-%d")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def score_text(text: str) -> tuple[int, list[str]]:
    lowered = text.lower()
    hits = []
    for keyword in TRIGGER_KEYWORDS:
        if keyword.lower() in lowered:
            hits.append(keyword)
    return len(set(hits)), sorted(set(hits))


def collect_markdown(day_dir: Path) -> list[Path]:
    if not day_dir.exists():
        return []
    skip_names = {
        "specshift_buyer_triggers.md",
        "finance_integrity_watch.md",
        "daily_digest.md",
    }
    return sorted(p for p in day_dir.glob("*.md") if p.name not in skip_names)


def extract_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
        if stripped.startswith("### "):
            return stripped[4:].strip()
    return fallback


def first_source_line(text: str) -> str:
    for line in text.splitlines():
        if "Source" in line or "URL:" in line or "Source query:" in line:
            return line.strip()
    return "Source link: see source digest"


def build_report(day_dir: Path, min_score: int) -> Path:
    day_dir.mkdir(parents=True, exist_ok=True)
    output = day_dir / "specshift_buyer_triggers.md"
    files = collect_markdown(day_dir)

    candidates = []
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        score, hits = score_text(text)
        if score >= min_score:
            candidates.append((score, hits, path, text))

    candidates.sort(key=lambda item: item[0], reverse=True)

    lines: list[str] = []
    lines.append("# SpecShift Buyer Trigger Watch")
    lines.append("")
    lines.append(f"Generated at UTC: {utc_now()}")
    lines.append(f"Report folder: {day_dir}")
    lines.append("")
    lines.append("## Safety Boundary")
    lines.append("")
    lines.append("This report is buyer-trigger triage only. It does not claim production validation, incident causation, buyer need, liability, or commercial fit.")
    lines.append("")
    lines.append("SpecShift relevance remains a hypothesis for human review.")
    lines.append("")
    lines.append("## Trigger Rules")
    lines.append("")
    lines.append("- Look for observable workflow, audit, reliability, handoff, approval, reconciliation, or agent-operation signals.")
    lines.append("- Preserve source uncertainty labels from upstream reports.")
    lines.append("- Do not use incident language exploitatively.")
    lines.append("- Do not claim hidden internals, protected method access, or validated failure prediction.")
    lines.append("")
    lines.append("## Candidate Buyer Triggers")
    lines.append("")

    if not candidates:
        lines.append("No buyer-trigger candidates met the current threshold.")
        lines.append("")
    else:
        for idx, (score, hits, path, text) in enumerate(candidates[:20], start=1):
            title = extract_title(text, path.name)
            source_line = first_source_line(text)
            role_hint = BUYER_ROLE_HINTS[(idx - 1) % len(BUYER_ROLE_HINTS)]

            lines.append(f"### {idx}. {title}")
            lines.append("")
            lines.append(f"- Source digest: {path}")
            lines.append(f"- Source/provenance line: {source_line}")
            lines.append(f"- Trigger score: {score}")
            lines.append(f"- Matched trigger terms: {', '.join(hits)}")
            lines.append(f"- Buyer role hypothesis: {role_hint}")
            lines.append("- SpecShift fit hypothesis: observable-only workflow review may be relevant if the event involves visible workflow trace, handoff, approval, reconciliation, or agent execution evidence.")
            lines.append("- Claim safety note: hypothesis only; requires human review and buyer-provided workflow details.")
            lines.append("- Outreach posture: do not overclaim; ask whether they want to evaluate a bounded, buyer-controlled pilot.")
            lines.append("")

    lines.append("## Buyer-Safe Language")
    lines.append("")
    lines.append("Safe sentence:")
    lines.append("")
    lines.append("SpecShift can review observable workflow traces and return candidate-discrepancy memos for human adjudication without requiring model internals, private prompts, weights, or hidden chain-of-thought.")
    lines.append("")
    lines.append("## Forbidden Language")
    lines.append("")
    lines.append("- proves failure prediction")
    lines.append("- detects hidden intent")
    lines.append("- guarantees compliance")
    lines.append("- validates production reliability")
    lines.append("- replaces internal audit")
    lines.append("- proves causation")
    lines.append("")
    lines.append("## Kira Recommendation")
    lines.append("")
    lines.append("Use this report to identify where a cautious buyer-trigger note might be drafted, not to claim the buyer has a problem or that SpecShift has already solved it.")
    lines.append("")

    output.write_text("\n".join(lines), encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate SpecShift buyer-trigger watch from local source digests.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--day-dir", default=None)
    parser.add_argument("--min-score", type=int, default=2)
    args = parser.parse_args()

    target = Path(args.day_dir) if args.day_dir else today_dir()

    print("=== SpecShift Buyer Trigger Watch ===")
    print(f"target_dir: {target}")
    print(f"min_score: {args.min_score}")
    print("mode: dry-run" if args.dry_run else "mode: generate")
    print("safety: synthesis only; no commercial overclaiming")

    if args.min_score < 1:
        print("FAIL --min-score must be >= 1")
        return 1

    if args.dry_run:
        print("PASS dry-run configuration")
        print("No files written.")
        return 0

    output = build_report(target, args.min_score)
    print(f"PASS wrote buyer trigger report: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
