#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import re
from datetime import datetime, timezone
from pathlib import Path

BOUNDARY = "Delivery packet generator only. It creates a client-facing bounded packet from approved project materials. It uses claim logic for internal safety scanning. It does not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdict, free pilot commitment, autonomous client action, truth validation, or hidden-mechanism claim."

CLAIM_LOGIC_PATH = Path("tools/claim_logic/claim_logic_classifier.py")

def load_claim_logic():
    if not CLAIM_LOGIC_PATH.exists():
        raise SystemExit(f"Missing claim logic classifier: {CLAIM_LOGIC_PATH}")
    spec = importlib.util.spec_from_file_location("claim_logic_classifier", CLAIM_LOGIC_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def split_sentences(text: str) -> list[str]:
    compact = re.sub(r"\s+", " ", text.strip())
    if not compact:
        return []
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", compact) if s.strip()]

def scan_claim_posture(text: str) -> dict:
    module = load_claim_logic()
    sentences = split_sentences(text)
    classifications = [module.classify_sentence(sentence) for sentence in sentences]

    blocked = [row for row in classifications if row.get("action") == "BLOCK_OR_REWRITE"]
    review = [row for row in classifications if row.get("action") == "REVIEW"]

    return {
        "engine": "delivery_packet_claim_logic_scan_v1",
        "scanned_at_utc": datetime.now(timezone.utc).isoformat(),
        "sentence_count": len(sentences),
        "blocked_count": len(blocked),
        "review_count": len(review),
        "blocked": blocked,
        "review": review,
        "claim_boundary": BOUNDARY,
    }

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

This packet does not provide legal advice.
This packet does not provide financial advice.
This packet does not create binding terms.
This packet does not provide compliance certification.
This packet does not provide production validation.
This packet does not create an automated verdict.
This packet does not provide truth validation.
This packet does not authorize autonomous client action.
This packet does not make hidden-mechanism or intent claims.

Buyer retains labels, human adjudication, and final decisions.

## 5. Buyer Questions

{questions}

## 6. Next-Step Recommendation

Recommended next step: {recommendation}

This recommendation is a workflow next-step prompt only. It does not authorize production action or create a commercial, legal, compliance, or certification conclusion.

## Boundary

{BOUNDARY}
"""

    scan = scan_claim_posture(packet)
    if scan["blocked"]:
        raise SystemExit("Blocked unsafe claim posture in delivery packet: " + json.dumps(scan["blocked"], ensure_ascii=False, indent=2))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(packet, encoding="utf-8")

    return {
        "engine": "delivery_packet_generator_v2_claim_logic_integrated",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "project_dir": str(project_dir),
        "output_path": str(output_path),
        "recommendation": recommendation,
        "claim_logic_scan": scan,
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
    print(f"blocked_claims: {report['claim_logic_scan']['blocked_count']}")
    print(f"review_claims: {report['claim_logic_scan']['review_count']}")
    print()
    print(f"Boundary: {BOUNDARY}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
