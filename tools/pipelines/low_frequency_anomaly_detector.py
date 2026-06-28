#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, pstdev

REPORT_ROOT = Path("reports/fast_relevance")

SKIP_FILES = {
    "daily_digest.md",
    "specshift_buyer_triggers.md",
    "finance_integrity_watch.md",
    "contradiction_watch.md",
    "claim_overstatement_watch.md",
    "low_frequency_anomaly_watch.md",
}

EVENT_HINTS = [
    "earthquake",
    "alert",
    "warning",
    "watch",
    "vulnerability",
    "cve",
    "kev",
    "rule",
    "notice",
    "preprint",
    "model",
    "filing",
    "incident",
    "outage",
    "reconciliation",
    "settlement",
    "ledger",
    "payment",
    "agent",
    "workflow",
    "failure",
]

NUMBER_PATTERN = re.compile(r"\b\d+(?:,\d{3})*(?:\.\d+)?\b")
HEADING_PATTERN = re.compile(r"^(#{1,4})\s+(.+)$", re.MULTILINE)


@dataclass
class DayMetrics:
    day: str
    markdown_files: int
    headings: int
    numbers: int
    event_hint_counts: dict[str, int]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def day_dirs(root: Path) -> list[Path]:
    if not root.exists():
        return []
    dirs = []
    for path in root.iterdir():
        if path.is_dir() and re.match(r"^\d{4}-\d{2}-\d{2}$", path.name):
            dirs.append(path)
    return sorted(dirs)


def collect_markdown(day_dir: Path) -> list[Path]:
    return sorted(p for p in day_dir.glob("*.md") if p.name not in SKIP_FILES)


def metrics_for_day(day_dir: Path) -> DayMetrics:
    files = collect_markdown(day_dir)
    all_text = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in files)
    lowered = all_text.lower()

    hint_counts = {}
    for hint in EVENT_HINTS:
        hint_counts[hint] = lowered.count(hint)

    headings = len(HEADING_PATTERN.findall(all_text))
    numbers = len(NUMBER_PATTERN.findall(all_text))

    return DayMetrics(
        day=day_dir.name,
        markdown_files=len(files),
        headings=headings,
        numbers=numbers,
        event_hint_counts=hint_counts,
    )


def z_score(value: float, values: list[float]) -> float | None:
    if len(values) < 3:
        return None
    baseline = values[:-1]
    if len(baseline) < 2:
        return None
    sigma = pstdev(baseline)
    if sigma == 0:
        return None
    return (value - mean(baseline)) / sigma


def classify_z(z: float | None, threshold: float) -> str:
    if z is None:
        return "insufficient_baseline"
    if abs(z) >= threshold:
        return "candidate_anomaly"
    return "within_baseline"


def build_report(root: Path, threshold: float, min_days: int) -> Path:
    days = day_dirs(root)
    if days:
        target_day = days[-1]
    else:
        target_day = root / datetime.now(timezone.utc).strftime("%Y-%m-%d")
        target_day.mkdir(parents=True, exist_ok=True)

    output = target_day / "low_frequency_anomaly_watch.md"

    metrics = [metrics_for_day(day) for day in days]
    current = metrics[-1] if metrics else metrics_for_day(target_day)

    lines: list[str] = []
    lines.append("# Low-Frequency High-Impact Anomaly Watch")
    lines.append("")
    lines.append(f"Generated at UTC: {utc_now()}")
    lines.append(f"Report root: {root}")
    lines.append(f"Current report day: {target_day}")
    lines.append("")
    lines.append("## Safety Boundary")
    lines.append("")
    lines.append("This output flags candidate statistical outliers for review only. It does not establish cause, intent, origin, prediction, emergency status, risk level, or validated conclusion.")
    lines.append("")
    lines.append("The anomaly detector is deliberately conservative. It requires baseline context and keeps all findings at observation or hypothesis level unless independently validated elsewhere.")
    lines.append("")
    lines.append("## Null Hypothesis")
    lines.append("")
    lines.append("The default assumption is that observed variation in daily pipeline outputs is ordinary source-volume fluctuation, reporting cadence variation, or local ingestion artifact unless independently corroborated.")
    lines.append("")
    lines.append("## Baseline Requirements")
    lines.append("")
    lines.append(f"- Minimum recommended historical days: {min_days}")
    lines.append(f"- Available historical days: {len(metrics)}")
    lines.append(f"- Z-score threshold: {threshold}")
    lines.append("- Any candidate anomaly requires human review.")
    lines.append("- Any candidate anomaly requires source-level inspection before interpretation.")
    lines.append("- No automated action is permitted.")
    lines.append("")

    if len(metrics) < min_days:
        lines.append("## Baseline Status")
        lines.append("")
        lines.append("INSUFFICIENT BASELINE.")
        lines.append("")
        lines.append("The system does not yet have enough historical daily reports to make meaningful low-frequency anomaly claims. This is expected for a new pipeline stack.")
        lines.append("")
    else:
        lines.append("## Baseline Status")
        lines.append("")
        lines.append("Baseline threshold met for coarse local report-volume checks.")
        lines.append("")

    lines.append("## Current Day Metrics")
    lines.append("")
    lines.append(f"- Markdown source digest count: {current.markdown_files}")
    lines.append(f"- Heading count: {current.headings}")
    lines.append(f"- Numeric token count: {current.numbers}")
    lines.append("")

    lines.append("## Candidate Metric Deviations")
    lines.append("")

    if len(metrics) < 3:
        lines.append("No z-score analysis performed because fewer than three report days are available.")
        lines.append("")
    else:
        file_values = [m.markdown_files for m in metrics]
        heading_values = [m.headings for m in metrics]
        number_values = [m.numbers for m in metrics]

        metric_rows = [
            ("markdown_files", current.markdown_files, z_score(current.markdown_files, file_values)),
            ("headings", current.headings, z_score(current.headings, heading_values)),
            ("numbers", current.numbers, z_score(current.numbers, number_values)),
        ]

        for name, value, z in metric_rows:
            lines.append(f"### {name}")
            lines.append("")
            lines.append(f"- Current value: {value}")
            lines.append(f"- Z-score: {z if z is not None else 'insufficient_baseline'}")
            lines.append(f"- Status: {classify_z(z, threshold)}")
            lines.append("- Claim safety note: metric deviation only; no causal inference.")
            lines.append("")

    lines.append("## Event Hint Counts")
    lines.append("")
    for hint in EVENT_HINTS:
        count = current.event_hint_counts.get(hint, 0)
        if count:
            lines.append(f"- {hint}: {count}")
    if not any(current.event_hint_counts.values()):
        lines.append("No configured event hints found in current report day.")
    lines.append("")

    lines.append("## Candidate Hint Deviations")
    lines.append("")

    if len(metrics) < 3:
        lines.append("No hint-level z-score analysis performed because fewer than three report days are available.")
        lines.append("")
    else:
        any_hint = False
        for hint in EVENT_HINTS:
            values = [m.event_hint_counts.get(hint, 0) for m in metrics]
            current_value = values[-1]
            z = z_score(current_value, values)
            status = classify_z(z, threshold)
            if status == "candidate_anomaly":
                any_hint = True
                lines.append(f"### {hint}")
                lines.append("")
                lines.append(f"- Current count: {current_value}")
                lines.append(f"- Z-score: {z}")
                lines.append(f"- Status: {status}")
                lines.append("- Claim safety note: keyword-volume outlier only; inspect source records before interpretation.")
                lines.append("")
        if not any_hint:
            lines.append("No configured event-hint counts exceeded anomaly threshold.")
            lines.append("")

    lines.append("## Required Review Steps Before Any Interpretation")
    lines.append("")
    lines.append("1. Inspect the source digests directly.")
    lines.append("2. Confirm the relevant raw source records exist.")
    lines.append("3. Check whether the spike is caused by duplicate records or source format changes.")
    lines.append("4. Check contradiction and overstatement reports.")
    lines.append("5. Seek independent corroboration before upgrading any item beyond hypothesis.")
    lines.append("")
    lines.append("## Forbidden Conclusions")
    lines.append("")
    lines.append("- Do not infer cause.")
    lines.append("- Do not infer intent.")
    lines.append("- Do not infer coordinated manipulation.")
    lines.append("- Do not infer emergency status.")
    lines.append("- Do not infer buyer urgency.")
    lines.append("- Do not trigger automated operational action.")
    lines.append("- Do not promote anomaly to validated conclusion.")
    lines.append("")
    lines.append("## Output Classification")
    lines.append("")
    lines.append("classification: anomaly_hypothesis_scaffold")
    lines.append("")
    lines.append("confidence ceiling: hypothesis")
    lines.append("")
    lines.append("human_review_required: true")
    lines.append("")
    lines.append("## Kira Recommendation")
    lines.append("")
    lines.append("Treat this as a smoke alarm for the data room, not as a diagnosis. First check whether the smoke is toast, wiring, weather, or a real fire.")
    lines.append("")

    output.write_text("\n".join(lines), encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate conservative low-frequency anomaly watch from local report history.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--report-root", default=str(REPORT_ROOT))
    parser.add_argument("--threshold", type=float, default=3.0)
    parser.add_argument("--min-days", type=int, default=14)
    args = parser.parse_args()

    root = Path(args.report_root)

    print("=== Low-Frequency High-Impact Anomaly Detector ===")
    print(f"report_root: {root}")
    print(f"threshold: {args.threshold}")
    print(f"min_days: {args.min_days}")
    print("mode: dry-run" if args.dry_run else "mode: generate")
    print("safety: anomaly hypothesis scaffold only; no causal inference or automated action")

    if args.threshold <= 0:
        print("FAIL --threshold must be greater than 0")
        return 1
    if args.min_days < 3:
        print("FAIL --min-days must be >= 3")
        return 1

    if args.dry_run:
        print("PASS dry-run configuration")
        print("No files written.")
        return 0

    output = build_report(root, args.threshold, args.min_days)
    print(f"PASS wrote anomaly watch: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
