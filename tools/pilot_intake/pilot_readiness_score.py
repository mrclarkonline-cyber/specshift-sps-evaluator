#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BOUNDARY = (
    "Pilot readiness score only. It is an internal buyer-safe intake scaffold. "
    "It does not create legal advice, financial advice, binding terms, compliance certification, "
    "production validation, automated verdicts, free-pilot commitments, autonomous client action, "
    "truth validation, or hidden-mechanism claims."
)

PROFESSIONAL_TRIGGERS = [
    "procurement",
    "contract_terms",
    "paid_pilot",
    "licensing",
    "exclusivity",
    "acquisition",
    "ip_assignment",
    "data_transfer",
    "money_movement",
]

REQUIRED_TRUE_FOR_READY = [
    "workflow_bounded",
    "observable_traces_available",
    "buyer_retains_labels",
    "human_adjudication_available",
    "success_criteria_exist",
    "prohibited_materials_excluded",
    "timeline_realistic",
    "data_boundaries_safe",
    "no_legal_compliance_certification_claim",
    "no_free_pilot_expectation",
]

def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    return bool(value)

def score_readiness(status: dict[str, Any]) -> dict[str, Any]:
    missing = []
    warnings = []

    professional_triggered = [key for key in PROFESSIONAL_TRIGGERS if as_bool(status.get(key, False))]
    if professional_triggered:
        decision = "NEEDS_COUNSEL"
        reason = "professional threshold triggered"
    elif as_bool(status.get("buyer_requests_certification", False)) or as_bool(status.get("buyer_requests_automated_verdict", False)) or as_bool(status.get("buyer_requests_production_validation", False)):
        decision = "DECLINE"
        reason = "buyer request is outside pilot boundary"
    elif as_bool(status.get("redaction_needed", False)) or as_bool(status.get("regulated_or_sensitive_data_present", False)):
        decision = "NEEDS_REDACTION"
        reason = "redaction or sensitive-data handling needed before intake"
    else:
        for key in REQUIRED_TRUE_FOR_READY:
            if not as_bool(status.get(key, False)):
                missing.append(key)

        if not as_bool(status.get("workflow_bounded", False)) or not as_bool(status.get("observable_traces_available", False)):
            decision = "NEEDS_SCOPING"
            reason = "workflow scope or observable trace availability is incomplete"
        elif missing:
            decision = "NOT_READY"
            reason = "one or more readiness conditions are missing"
        else:
            decision = "READY"
            reason = "bounded observable-only pilot appears internally ready to proceed"

    if not as_bool(status.get("buyer_retains_labels", False)):
        warnings.append("buyer label ownership/final adjudication not confirmed")
    if not as_bool(status.get("no_free_pilot_expectation", False)):
        warnings.append("free-pilot expectation not excluded")
    if professional_triggered:
        warnings.append("engage qualified legal and CPA support before proceeding")
    if decision == "READY":
        warnings.append("READY means internally intake-ready only, not certified, validated, or legally approved")

    score = sum(1 for key in REQUIRED_TRUE_FOR_READY if as_bool(status.get(key, False)))
    max_score = len(REQUIRED_TRUE_FOR_READY)
    percent = round((score / max_score) * 100, 1) if max_score else 0.0

    return {
        "engine": "pilot_readiness_score_v1",
        "scored_at_utc": datetime.now(timezone.utc).isoformat(),
        "decision": decision,
        "reason": reason,
        "readiness_score": score,
        "readiness_max_score": max_score,
        "readiness_percent": percent,
        "missing_conditions": missing,
        "professional_triggers": professional_triggered,
        "warnings": warnings,
        "allowed_decisions": [
            "READY",
            "NOT_READY",
            "NEEDS_SCOPING",
            "NEEDS_REDACTION",
            "NEEDS_COUNSEL",
            "DECLINE",
        ],
        "claim_boundary": BOUNDARY,
    }

def main() -> int:
    parser = argparse.ArgumentParser(description="Score whether a buyer-safe pilot is ready to accept.")
    parser.add_argument("--status-json", required=True, help="Path to buyer pilot readiness status JSON")
    parser.add_argument("--output", default="", help="Optional JSON output path")
    parser.add_argument("--json", action="store_true", help="Print JSON only")
    args = parser.parse_args()

    status = json.loads(Path(args.status_json).read_text(encoding="utf-8"))
    result = score_readiness(status)

    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print("Pilot Readiness Score")
        print("=" * 72)
        print(f"decision: {result['decision']}")
        print(f"reason:   {result['reason']}")
        print(f"score:    {result['readiness_score']}/{result['readiness_max_score']} ({result['readiness_percent']}%)")
        print()
        print("Missing conditions:")
        for item in result["missing_conditions"] or ["none"]:
            print(f"  - {item}")
        print()
        print("Professional triggers:")
        for item in result["professional_triggers"] or ["none"]:
            print(f"  - {item}")
        print()
        print("Warnings:")
        for item in result["warnings"] or ["none"]:
            print(f"  - {item}")
        print()
        print(f"Boundary: {BOUNDARY}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
