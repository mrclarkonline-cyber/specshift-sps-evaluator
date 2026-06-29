#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import re
from datetime import datetime, timezone
from pathlib import Path

BOUNDARY = (
    "Claim logic audit gate only. It scans text artifacts for claim posture. "
    "It allows safe denial and boundary language, blocks unsafe affirmative authority claims, "
    "and can optionally fail on ambiguous review items. It does not create legal advice, "
    "financial advice, binding terms, compliance certification, production validation, "
    "automated verdicts, free-pilot commitments, autonomous client action, truth validation, "
    "or hidden-mechanism claims."
)

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

def scan_text(text: str, fail_on_review: bool = False) -> dict:
    module = load_claim_logic()
    sentences = split_sentences(text)
    rows = [module.classify_sentence(sentence) for sentence in sentences]

    blocked = [row for row in rows if row.get("action") == "BLOCK_OR_REWRITE"]
    review = [row for row in rows if row.get("action") == "REVIEW"]
    allowed = [row for row in rows if row.get("action") == "ALLOW"]

    status = "pass"
    if blocked:
        status = "fail"
    elif review and fail_on_review:
        status = "review_fail"
    elif review:
        status = "review"

    return {
        "engine": "claim_logic_audit_gate_v1",
        "scanned_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "sentence_count": len(sentences),
        "allowed_count": len(allowed),
        "review_count": len(review),
        "blocked_count": len(blocked),
        "allowed": allowed,
        "review": review,
        "blocked": blocked,
        "fail_on_review": fail_on_review,
        "claim_boundary": BOUNDARY,
    }

def scan_file(path: Path, fail_on_review: bool = False) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    result = scan_text(text, fail_on_review=fail_on_review)
    result["path"] = str(path)
    return result

def main() -> int:
    parser = argparse.ArgumentParser(description="Claim-logic audit gate for text artifacts.")
    parser.add_argument("--file", required=True)
    parser.add_argument("--output", default="")
    parser.add_argument("--fail-on-review", action="store_true")
    args = parser.parse_args()

    result = scan_file(Path(args.file), fail_on_review=args.fail_on_review)

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("Claim Logic Audit Gate")
    print("=" * 72)
    print(f"file: {result['path']}")
    print(f"status: {result['status']}")
    print(f"allowed: {result['allowed_count']}")
    print(f"review: {result['review_count']}")
    print(f"blocked: {result['blocked_count']}")
    print()
    print(f"Boundary: {BOUNDARY}")

    return 0 if result["status"] in {"pass", "review"} else 1

if __name__ == "__main__":
    raise SystemExit(main())
