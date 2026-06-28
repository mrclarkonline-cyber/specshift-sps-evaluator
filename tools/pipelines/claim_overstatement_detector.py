#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

REPORT_ROOT = Path("reports/fast_relevance")

SKIP_FILES = {
    "daily_digest.md",
    "specshift_buyer_triggers.md",
    "finance_integrity_watch.md",
    "contradiction_watch.md",
    "claim_overstatement_watch.md",
}

OVERSTATEMENT_PATTERNS = {
    "proof_language": [
        r"\bproves?\b",
        r"\bproof\b",
        r"\bdefinitively\b",
        r"\bconclusive(?:ly)?\b",
        r"\bestablishes beyond doubt\b",
    ],
    "guarantee_language": [
        r"\bguarantees?\b",
        r"\bassures?\b",
        r"\bensures?\b",
        r"\bfail-?safe\b",
    ],
    "unsupported_validation_language": [
        r"\bvalidated conclusion\b",
        r"\bvalidated in production\b",
        r"\bproduction[- ]validated\b",
        r"\bpeer[- ]reviewed\b",
        r"\bscientific consensus\b",
        r"\bindependently verified\b",
    ],
    "forbidden_advice_language": [
        r"\binvestment advice\b",
        r"\btrading signal\b",
        r"\blegal advice\b",
        r"\bmedical advice\b",
        r"\bclinical recommendation\b",
        r"\bcompliance certification\b",
        r"\baudit opinion\b",
    ],
    "intent_or_cause_overclaim": [
        r"\bintent\b",
        r"\bintended to\b",
        r"\bcaused by\b",
        r"\bcausation\b",
        r"\bfraud\b",
        r"\bconcealment\b",
        r"\bmanipulation\b",
    ],
}

SAFE_DOWNGRADE_HINTS = {
    "proof_language": "Use observation/hypothesis language. Example: 'suggests', 'reports', 'is consistent with', or 'requires review'.",
    "guarantee_language": "Remove guarantee language. Use bounded capability language and human-review requirements.",
    "unsupported_validation_language": "Only use validation language when supported by a source and logged verification state.",
    "forbidden_advice_language": "Replace with awareness/triage language. Do not provide investment, legal, medical, compliance, or audit conclusions.",
    "intent_or_cause_overclaim": "Do not infer intent or cause from source digests. Use 'reported', 'flagged', or 'unresolved variance'.",
}


def today_dir() -> Path:
    return REPORT_ROOT / datetime.now(timezone.utc).strftime("%Y-%m-%d")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def collect_markdown(day_dir: Path) -> list[Path]:
    if not day_dir.exists():
        return []
    return sorted(p for p in day_dir.glob("*.md") if p.name not in SKIP_FILES)


def title_label(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
        if stripped.startswith("### "):
            return stripped[4:].strip()
    return fallback


def source_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        lowered = stripped.lower()
        if lowered.startswith("source:") or lowered.startswith("source query:") or "source digest:" in lowered:
            return stripped
    return "Source: see source digest"


def uncertainty_lines(text: str) -> list[str]:
    lines = []
    for line in text.splitlines():
        lowered = line.lower()
        if "uncertainty label" in lowered or "claim safety note" in lowered or "source tier" in lowered:
            lines.append(line.strip())
    return lines[:10]


def matched_patterns(text: str) -> list[tuple[str, str, str]]:
    matches: list[tuple[str, str, str]] = []
    lowered = text.lower()

    for category, patterns in OVERSTATEMENT_PATTERNS.items():
        for pattern in patterns:
            for match in re.finditer(pattern, lowered, flags=re.IGNORECASE):
                start = max(match.start() - 70, 0)
                end = min(match.end() + 110, len(text))
                excerpt = text[start:end].replace("\n", " ").strip()
                matches.append((category, match.group(0), excerpt))

    return matches


def build_report(day_dir: Path) -> Path:
    day_dir.mkdir(parents=True, exist_ok=True)
    output = day_dir / "claim_overstatement_watch.md"

    files = collect_markdown(day_dir)
    findings = []

    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        matches = matched_patterns(text)
        if matches:
            findings.append({
                "path": path,
                "title": title_label(text, path.name),
                "source": source_line(text),
                "uncertainty": uncertainty_lines(text),
                "matches": matches,
            })

    lines: list[str] = []
    lines.append("# Claim-Overstatement Watch")
    lines.append("")
    lines.append(f"Generated at UTC: {utc_now()}")
    lines.append(f"Report folder: {day_dir}")
    lines.append("")
    lines.append("## Safety Boundary")
    lines.append("")
    lines.append("This output flags language that may assert more certainty than the source record supports. It does not adjudicate truth, falsity, intent, cause, liability, safety, compliance, investment value, medical validity, or production readiness.")
    lines.append("")
    lines.append("The detector is a language-control guardrail, not a source-of-truth engine.")
    lines.append("")
    lines.append("## Method")
    lines.append("")
    lines.append("- Scans local generated markdown digests only.")
    lines.append("- Flags risky proof, guarantee, validation, advice, intent, and causation language.")
    lines.append("- Preserves source, uncertainty, and claim-safety context.")
    lines.append("- Does not fetch network data.")
    lines.append("- Does not mutate source digests.")
    lines.append("")
    lines.append("## Candidate Overstatement Items")
    lines.append("")

    if not findings:
        lines.append("No candidate overstatement items found.")
        lines.append("")
    else:
        for idx, finding in enumerate(findings[:40], start=1):
            lines.append(f"### {idx}. {finding['title']}")
            lines.append("")
            lines.append(f"- Source digest: {finding['path']}")
            lines.append(f"- Source line: {finding['source']}")
            if finding["uncertainty"]:
                lines.append("- Local uncertainty / safety context:")
                for item in finding["uncertainty"]:
                    lines.append(f"  - {item}")
            lines.append("")
            lines.append("Potential overstatement flags:")
            for category, phrase, excerpt in finding["matches"][:12]:
                lines.append(f"- Category: {category}")
                lines.append(f"  - Matched phrase: {phrase}")
                lines.append(f"  - Excerpt: {excerpt}")
                lines.append(f"  - Suggested downgrade: {SAFE_DOWNGRADE_HINTS.get(category, 'Use bounded, source-linked language.')}")
            lines.append("")
            lines.append("Claim safety note: language flag only; human review required before revision or conclusion.")
            lines.append("")

    lines.append("## Required Downgrade Rules")
    lines.append("")
    lines.append("- Replace proof language with source-reporting language.")
    lines.append("- Replace guarantees with bounded, testable claims.")
    lines.append("- Replace validation claims with explicit evidence status.")
    lines.append("- Replace advice language with awareness/triage language.")
    lines.append("- Replace intent/cause claims with unresolved-variance or source-reported language.")
    lines.append("")
    lines.append("## Safe Replacement Examples")
    lines.append("")
    lines.append("- Instead of: proves")
    lines.append("  Use: reports, suggests, is consistent with, or flags for review.")
    lines.append("- Instead of: guarantees")
    lines.append("  Use: is designed to support reviewer-controlled testing.")
    lines.append("- Instead of: validated in production")
    lines.append("  Use: not yet validated in live production unless a source and validation record support it.")
    lines.append("- Instead of: detects fraud")
    lines.append("  Use: flags candidate discrepancies for human review.")
    lines.append("")
    lines.append("## Forbidden Conclusions")
    lines.append("")
    lines.append("- Do not infer cause from a headline.")
    lines.append("- Do not infer intent from a workflow trace.")
    lines.append("- Do not treat preprints as peer-reviewed.")
    lines.append("- Do not treat model-card claims as independently verified.")
    lines.append("- Do not convert a source record into legal, medical, investment, compliance, or audit advice.")
    lines.append("")
    lines.append("## Kira Recommendation")
    lines.append("")
    lines.append("Use this report as a wording-control pass before any outward-facing digest, outreach note, or buyer-safe artifact. The right move is language downgrade, not dramatic conclusion.")
    lines.append("")

    output.write_text("\n".join(lines), encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate claim-overstatement watch from local digests.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--day-dir", default=None)
    args = parser.parse_args()

    target = Path(args.day_dir) if args.day_dir else today_dir()

    print("=== Claim-Overstatement Detector ===")
    print(f"target_dir: {target}")
    print("mode: dry-run" if args.dry_run else "mode: generate")
    print("safety: language-control guardrail only; no truth adjudication")

    if args.dry_run:
        print("PASS dry-run configuration")
        print("No files written.")
        return 0

    output = build_report(target)
    print(f"PASS wrote claim-overstatement watch: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
