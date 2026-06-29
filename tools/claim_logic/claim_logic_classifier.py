#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone

BOUNDARY = (
    "Claim logic classifier only. It classifies claim posture for internal safety scanning. "
    "It does not create legal advice, financial advice, binding terms, compliance certification, "
    "production validation, automated verdicts, free-pilot commitments, autonomous client action, "
    "truth validation, or hidden-mechanism claims."
)

CATEGORIES = [
    "SAFE_DENIAL",
    "SAFE_BOUNDARY",
    "UNSAFE_ASSERTION",
    "UNSAFE_CERTIFICATION",
    "UNSAFE_VERDICT",
    "UNSAFE_HIDDEN_MECHANISM",
    "AMBIGUOUS_REVIEW",
]

SAFE_DENIAL_PATTERNS = [
    r"\bdoes not\b",
    r"\bdo not\b",
    r"\bnot provide\b",
    r"\bnot claim\b",
    r"\bno\b",
    r"\bwithout\b",
    r"\bis not\b",
    r"\bare not\b",
    r"\bcannot\b",
]

BOUNDARY_PATTERNS = [
    r"\bbuyer retains\b",
    r"\bhuman adjudication\b",
    r"\bcandidate-discrepancy\b",
    r"\bobservable-only\b",
    r"\bbuyer-controlled\b",
    r"\bfor human review\b",
    r"\binternal scaffold\b",
]

UNSAFE_CERTIFICATION_PATTERNS = [
    r"\bwe certify\b",
    r"\bwe can certify\b",
    r"\bcertifies compliance\b",
    r"\bcompliance certified\b",
    r"\bcertification conclusion\b",
    r"\bcertified as compliant\b",
]

UNSAFE_VERDICT_PATTERNS = [
    r"\bautomated verdict\s*:\s*(pass|fail|approved|rejected)\b",
    r"\bverdict\s*:\s*(pass|fail|approved|rejected)\b",
    r"\bfinal judgment\s*:\b",
    r"\bwe determine\b",
    r"\bwe conclude\b",
]

UNSAFE_ASSERTION_PATTERNS = [
    r"\bwe validate\b",
    r"\bvalidate[s]?\b",
    r"\bvalidated\b",
    r"\bwe prove\b",
    r"\bwe can prove\b",
    r"\bproduction validated\b",
    r"\btruth validated\b",
    r"\bguaranteed detection\b",
    r"\bguarantees\b",
]

UNSAFE_HIDDEN_MECHANISM_PATTERNS = [
    r"\bintended to deceive\b",
    r"\bmodel intent\b",
    r"\bhidden intent\b",
    r"\bhidden mechanism\b",
    r"\binternal reasoning proves\b",
]

RISK_TERMS = [
    "legal advice",
    "financial advice",
    "binding terms",
    "compliance certification",
    "production validation",
    "automated verdict",
    "truth validation",
    "autonomous client action",
    "hidden-mechanism",
    "model intent",
    "production safety",
]

def has(patterns: list[str], text: str) -> bool:
    return any(re.search(pattern, text, flags=re.I) for pattern in patterns)

def classify_sentence(sentence: str) -> dict:
    text = sentence.strip()
    low = text.lower()

    matched_risk_terms = [term for term in RISK_TERMS if term in low]

    if has(UNSAFE_CERTIFICATION_PATTERNS, low):
        category = "UNSAFE_CERTIFICATION"
        action = "BLOCK_OR_REWRITE"
    elif has(UNSAFE_VERDICT_PATTERNS, low):
        category = "UNSAFE_VERDICT"
        action = "BLOCK_OR_REWRITE"
    elif has(UNSAFE_HIDDEN_MECHANISM_PATTERNS, low):
        category = "UNSAFE_HIDDEN_MECHANISM"
        action = "BLOCK_OR_REWRITE"
    elif has(UNSAFE_ASSERTION_PATTERNS, low):
        category = "UNSAFE_ASSERTION"
        action = "BLOCK_OR_REWRITE"
    elif matched_risk_terms and has(SAFE_DENIAL_PATTERNS, low):
        category = "SAFE_DENIAL"
        action = "ALLOW"
    elif has(BOUNDARY_PATTERNS, low):
        category = "SAFE_BOUNDARY"
        action = "ALLOW"
    elif matched_risk_terms:
        category = "AMBIGUOUS_REVIEW"
        action = "REVIEW"
    else:
        category = "SAFE_BOUNDARY"
        action = "ALLOW"

    return {
        "engine": "claim_logic_classifier_v1",
        "classified_at_utc": datetime.now(timezone.utc).isoformat(),
        "sentence": sentence,
        "category": category,
        "action": action,
        "matched_risk_terms": matched_risk_terms,
        "claim_boundary": BOUNDARY,
    }

def main() -> int:
    parser = argparse.ArgumentParser(description="Classify claim posture for safety scanning.")
    parser.add_argument("--text", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = classify_sentence(args.text)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print("Claim Logic Classifier")
        print("=" * 72)
        print(f"category: {result['category']}")
        print(f"action:   {result['action']}")
        print(f"risk_terms: {result['matched_risk_terms']}")
        print()
        print(f"Boundary: {BOUNDARY}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
