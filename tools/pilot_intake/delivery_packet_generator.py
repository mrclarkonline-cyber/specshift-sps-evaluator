#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

BOUNDARY = "Delivery packet generator only. It creates a client-facing bounded packet from approved project materials. It does not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdict, free pilot commitment, autonomous client action, truth validation, or hidden-mechanism claim."

# Scan only affirmative overclaims. Do not flag non-claim boundary language.
AFFIRMATIVE_FORBIDDEN_PATTERNS = [
    r"\bwe certify\b",
    r"\bwe can certify\b",
    r"\bwe prove\b",
    r"\bwe can prove\b",
    r"\bthis certifies\b",
    r"\bthis proves\b",
    r"\bcompliance certified\b",
    r"\bproduction validated\b",
    r"\btruth validated\b",
    r"\bguaranteed detection\b",
    r"\bautomated verdict\s*:\s*(pass|fail|approved|rejected)\b",
    r"\blegal conclusion\s*:\b",
    r"\bfinancial conclusion\s*:\b",
]

def forbidden_hits(text: str) -> list[str]:
    low = text.lower()
    return [pattern for pattern in AFFIRMATIVE_FORBIDDEN_PATTERNS if re.search(pattern, low)]

def read_text(path: Path, fallback: str) -> str:
    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8", errors="ignore").strip()
    return fallback.strip()

def build_packet(project_dir: Path, output_path: Path, recommendation: str = "REPEAT_WITH_CLEANER_DATA") -> dict:
    manifest = read_text(project_dir / "01_received_manifest.md", "No reviewed artifact manifest was provided. Buyer review is required.")
    scope = read_text(project_dir / "02_scope_boundary_check.md", "Scope boundary not provided. Observable-only, buyer-controlled scope must be confirmed.")
    memo = read_text(project_dir / "04_candidate_discrepancy_memo_draft.md", "No candidate-discrepancy memo draft was provided.")
    questions = read_text(project_dir / "06_buyer_questions.md", "Buyer should confirm labels, adjudication process, and whether more observable context is available.")

    packet = f"""# SpecShift Buyer-Safe Pilot Delivery Packet

Status: draft
Generated at UTC: {datetime.now(timezone.utc).isoformat()}

## 1. Reviewed Artifacts Manifest

{manifest}

## 2. Scope Boundary

{scope}

## 3. Candidate-Discrepancy Memo

{memo}

## 4. Limitations and Non-Claims

This packet is based on buyer-provided observable materials only.

This packet does not provide:

- legal advice
- financial advice
- binding terms
- compliance certification
- production validation
- automated verdict
- truth validation
- autonomous client action
- hidden-mechanism or intent claims

Buyer retains labels, human adjudication, and final decisions.

## 5. Buyer Questions

{questions}

## 6. Next-Step Recommendation

Recommended next step: {recommendation}

This recommendation is a workflow next-step prompt only. It does not authorize production action or create a commercial, legal, compliance, or certification conclusion.

## Boundary

{BOUNDARY}
"""

    hits = forbidden_hits(packet)
    if hits:
        raise SystemExit(f"Forbidden affirmative claim pattern(s): {hits}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(packet, encoding="utf-8")

    return {
        "engine": "delivery_packet_generator_v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "project_dir": str(project_dir),
        "output_path": str(output_path),
        "recommendation": recommendation,
        "forbidden_hits": hits,
        "claim_boundary": BOUNDARY,
    }

def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a buyer-safe pilot delivery packet.")
    parser.add_argument("--project-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--recommendation", default="REPEAT_WITH_CLEANER_DATA")
    parser.add_argument("--report", default="")
    args = parser.parse_args()

    report = build_packet(Path(args.project_dir), Path(args.output), args.recommendation)

    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("Delivery Packet Generator")
    print("=" * 72)
    print(f"output: {report['output_path']}")
    print(f"recommendation: {report['recommendation']}")
    print(f"forbidden_hits: {len(report['forbidden_hits'])}")
    print()
    print(f"Boundary: {BOUNDARY}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
