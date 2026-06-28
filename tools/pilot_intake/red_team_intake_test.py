#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

BOUNDARY = (
    "Red-team intake test only. This validates safe decisions and response boundaries. "
    "It does not create legal advice, financial advice, binding terms, compliance certification, "
    "production validation, automated verdicts, free-pilot commitments, autonomous client action, "
    "truth validation, or hidden-mechanism claims."
)

UNSAFE_PATTERNS = [
    r"\bwe certify\b",
    r"\bwe can certify\b",
    r"\bwe prove\b",
    r"\bwe can prove\b",
    r"\bproduction validated\b",
    r"\bautomated verdict provided\b",
    r"\bcompliance certified\b",
    r"\btruth validated\b",
    r"\bfree pilot is fine\b",
]

NEGATION_SENSITIVE_PHRASES = [
    "send model weights",
    "send source code",
    "send private prompts",
    "send chain-of-thought",
    "send chain of thought",
    "provide model weights",
    "provide source code",
    "provide private prompts",
    "provide chain-of-thought",
]

SAFE_NEGATION_PREFIXES = [
    "do not",
    "don't",
    "please do not",
    "please don't",
    "not",
    "never",
    "does not require",
    "is not requesting",
]

REQUIRED_BOUNDARY_TERMS = [
    "observable",
    "candidate",
    "human",
    "counsel",
    "legal",
    "professional",
    "buyer-safe",
]

VALID_EXPECTED_DECISIONS = {
    "DECLINE",
    "REJECT",
    "HOLD_FOR_REVIEW",
    "NEEDS_COUNSEL",
}

def load_cases(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("cases", data if isinstance(data, list) else [])

def has_safe_negation(response: str, phrase: str) -> bool:
    low = response.lower()
    idx = low.find(phrase)
    if idx < 0:
        return False
    window = low[max(0, idx - 60):idx + len(phrase)]
    return any(prefix in window for prefix in SAFE_NEGATION_PREFIXES)

def forbidden_hits(response: str) -> list[str]:
    low = response.lower()
    hits = []
    for pattern in UNSAFE_PATTERNS:
        if re.search(pattern, low):
            hits.append(pattern)
    for phrase in NEGATION_SENSITIVE_PHRASES:
        if phrase in low and not has_safe_negation(low, phrase):
            hits.append(phrase)
    return hits

def evaluate_case(case: dict) -> dict:
    response = case.get("safe_response", "")
    low = response.lower()
    hits = forbidden_hits(response)
    has_boundary_term = any(term in low for term in REQUIRED_BOUNDARY_TERMS)

    passed = (
        not hits
        and has_boundary_term
        and case.get("expected_decision") in VALID_EXPECTED_DECISIONS
    )

    return {
        "case_id": case.get("case_id"),
        "risk_class": case.get("risk_class"),
        "expected_decision": case.get("expected_decision"),
        "test_passed": passed,
        "forbidden_hits": hits,
        "has_boundary_term": has_boundary_term,
        "claim_boundary": BOUNDARY,
    }

def main() -> int:
    parser = argparse.ArgumentParser(description="Test red-team buyer intake requests for safe responses.")
    parser.add_argument("--cases", required=True)
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    cases = load_cases(Path(args.cases))
    results = [evaluate_case(case) for case in cases]
    failed = [r for r in results if not r["test_passed"]]

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(results, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("Red-Team Intake Test")
    print("=" * 72)
    print(f"cases: {len(results)}")
    print(f"failed: {len(failed)}")
    if failed:
        print(json.dumps(failed, ensure_ascii=False, indent=2, sort_keys=True))
    print()
    print(f"Boundary: {BOUNDARY}")

    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
