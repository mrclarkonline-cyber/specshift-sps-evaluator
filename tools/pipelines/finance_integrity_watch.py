#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

REPORT_ROOT = Path("reports/fast_relevance")

FINANCE_KEYWORDS = [
    "reconciliation",
    "settlement",
    "payment",
    "payments",
    "ledger",
    "invoice",
    "billing",
    "close process",
    "month-end",
    "journal",
    "audit",
    "controls",
    "8-k",
    "10-k",
    "10-q",
    "material weakness",
    "restatement",
    "fintech",
    "bank",
    "treasury",
    "accounts payable",
    "accounts receivable",
    "revenue recognition",
    "chargeback",
    "refund",
    "payout",
]

ROLE_HINTS = [
    "VP Finance Operations",
    "Head of Reconciliation",
    "Controller",
    "Head of Payments Operations",
    "FinOps Platform Lead",
    "Principal Engineer, Ledger Infrastructure",
    "Head of Settlement Operations",
    "Finance Systems Lead",
]


def today_dir() -> Path:
    return REPORT_ROOT / datetime.now(timezone.utc).strftime("%Y-%m-%d")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def score_text(text: str) -> tuple[int, list[str]]:
    lowered = text.lower()
    hits = []
    for keyword in FINANCE_KEYWORDS:
        if keyword.lower() in lowered:
            hits.append(keyword)
    return len(set(hits)), sorted(set(hits))


def collect_markdown(day_dir: Path) -> list[Path]:
    if not day_dir.exists():
        return []
    skip_names = {
        "finance_integrity_watch.md",
        "specshift_buyer_triggers.md",
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
    output = day_dir / "finance_integrity_watch.md"
    files = collect_markdown(day_dir)

    candidates = []
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        score, hits = score_text(text)
        if score >= min_score:
            candidates.append((score, hits, path, text))

    candidates.sort(key=lambda item: item[0], reverse=True)

    lines: list[str] = []
    lines.append("# Finance Integrity Watch")
    lines.append("")
    lines.append(f"Generated at UTC: {utc_now()}")
    lines.append(f"Report folder: {day_dir}")
    lines.append("")
    lines.append("## Safety Boundary")
    lines.append("")
    lines.append("This report is finance-workflow triage only. It is not investment advice, trading advice, compliance certification, audit opinion, or legal advice.")
    lines.append("")
    lines.append("SpecShift relevance remains a buyer-controlled evaluation hypothesis.")
    lines.append("")
    lines.append("## Finance Workflow Signals")
    lines.append("")
    lines.append("Relevant signals may include reconciliation, settlement, payment operations, ledger workflows, invoicing, revenue recognition, close process, and audit/control traceability.")
    lines.append("")
    lines.append("## Candidate Finance Integrity Triggers")
    lines.append("")

    if not candidates:
        lines.append("No finance-integrity candidates met the current threshold.")
        lines.append("")
    else:
        for idx, (score, hits, path, text) in enumerate(candidates[:20], start=1):
            title = extract_title(text, path.name)
            source_line = first_source_line(text)
            role_hint = ROLE_HINTS[(idx - 1) % len(ROLE_HINTS)]

            lines.append(f"### {idx}. {title}")
            lines.append("")
            lines.append(f"- Source digest: {path}")
            lines.append(f"- Source/provenance line: {source_line}")
            lines.append(f"- Finance score: {score}")
            lines.append(f"- Matched finance terms: {', '.join(hits)}")
            lines.append(f"- Buyer role hypothesis: {role_hint}")
            lines.append("- SpecShift fit hypothesis: observable-only review may be relevant if finance workflow trace, reconciliation steps, approval path, ledger state, or claimed final state can be compared for discrepancies.")
            lines.append("- Claim safety note: hypothesis only; no compliance, audit, or investment conclusion.")
            lines.append("")

    lines.append("## Buyer-Safe Sentence")
    lines.append("")
    lines.append("SpecShift compares observable reconciliation or finance workflow traces against claimed final ledger or payment states and returns structured candidate-discrepancy memos for reviewer-controlled testing.")
    lines.append("")
    lines.append("## Forbidden Language")
    lines.append("")
    lines.append("- certifies compliance")
    lines.append("- proves fraud")
    lines.append("- predicts financial failure")
    lines.append("- generates trading signals")
    lines.append("- replaces audit")
    lines.append("- guarantees ledger correctness")
    lines.append("")
    lines.append("## Kira Recommendation")
    lines.append("")
    lines.append("Use this watch to identify cautious finance-workflow pilot openings. Keep all scoring evaluator-controlled and avoid severity claims.")
    lines.append("")

    output.write_text("\n".join(lines), encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Finance Integrity Watch from local source digests.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--day-dir", default=None)
    parser.add_argument("--min-score", type=int, default=1)
    args = parser.parse_args()

    target = Path(args.day_dir) if args.day_dir else today_dir()

    print("=== Finance Integrity Watch ===")
    print(f"target_dir: {target}")
    print(f"min_score: {args.min_score}")
    print("mode: dry-run" if args.dry_run else "mode: generate")
    print("safety: synthesis only; no finance/legal/compliance overclaiming")

    if args.min_score < 1:
        print("FAIL --min-score must be >= 1")
        return 1

    if args.dry_run:
        print("PASS dry-run configuration")
        print("No files written.")
        return 0

    output = build_report(target, args.min_score)
    print(f"PASS wrote finance integrity report: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
