#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BOUNDARY = (
    "Delivery closeout recommender only. It recommends buyer-safe next steps from bounded pilot status fields. "
    "It does not create legal advice, financial advice, binding terms, compliance certification, production validation, "
    "automated verdicts, free-pilot commitments, autonomous client action, truth validation, or hidden-mechanism claims."
)

VALID_RECOMMENDATIONS = [
    "NO_FIT",
    "REPEAT_WITH_CLEANER_DATA",
    "EXPAND_SAME_WORKFLOW",
    "TEST_SECOND_WORKFLOW",
    "PAID_STRATEGIC_PILOT",
    "STOP_UNTIL_LEGAL_CPA_REVIEW",
]

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

def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    return bool(value)

def choose_recommendation(status: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []

    professional_triggered = any(as_bool(status.get(k, False)) for k in PROFESSIONAL_TRIGGERS)
    if professional_triggered:
        reasons.append("professional threshold triggered")
        return "STOP_UNTIL_LEGAL_CPA_REVIEW", reasons

    if not as_bool(status.get("observable_trace_available", False)):
        reasons.append("no observable trace available")
        return "NO_FIT", reasons

    if not as_bool(status.get("buyer_human_adjudication_available", False)):
        reasons.append("buyer human adjudication unavailable")
        return "NO_FIT", reasons

    if as_bool(status.get("redaction_needed", False)):
        reasons.append("redaction needed before useful repeat")
        return "REPEAT_WITH_CLEANER_DATA", reasons

    if as_bool(status.get("scope_boundary_violation", False)):
        reasons.append("scope boundary violation")
        return "REPEAT_WITH_CLEANER_DATA", reasons

    useful = int(status.get("useful_review_prompts", 0) or 0)
    ambiguous = int(status.get("ambiguous_review_prompts", 0) or 0)
    insufficient = int(status.get("insufficient_information_prompts", 0) or 0)
    false_positive = int(status.get("false_positive_count", 0) or 0)

    if useful <= 0 and insufficient > 0:
        reasons.append("insufficient information dominates")
        return "REPEAT_WITH_CLEANER_DATA", reasons

    if useful >= 5 and false_positive <= 2:
        reasons.append("useful prompts present with bounded false-positive count")
        if as_bool(status.get("buyer_requests_second_workflow", False)):
            reasons.append("buyer requests second workflow")
            return "TEST_SECOND_WORKFLOW", reasons
        return "EXPAND_SAME_WORKFLOW", reasons

    if useful >= 10 and as_bool(status.get("buyer_requests_paid_next_step", False)):
        reasons.append("buyer requests paid next step after useful prompts")
        return "PAID_STRATEGIC_PILOT", reasons

    if ambiguous > useful and useful > 0:
        reasons.append("ambiguous prompts exceed useful prompts")
        return "REPEAT_WITH_CLEANER_DATA", reasons

    if useful > 0:
        reasons.append("some useful prompts but not enough for expansion")
        return "REPEAT_WITH_CLEANER_DATA", reasons

    reasons.append("no strong fit signal")
    return "NO_FIT", reasons

def closeout(status: dict[str, Any]) -> dict[str, Any]:
    recommendation, reasons = choose_recommendation(status)

    return {
        "engine": "delivery_closeout_recommender_v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "recommendation": recommendation,
        "reasons": reasons,
        "reviewed": {
            "workflow_name": status.get("workflow_name", ""),
            "artifacts_reviewed": status.get("artifacts_reviewed", []),
            "artifacts_excluded": status.get("artifacts_excluded", []),
            "candidate_discrepancies": status.get("candidate_discrepancies", []),
            "limitations": status.get("limitations", []),
            "buyer_decisions_required": status.get("buyer_decisions_required", []),
            "error_accounting_available": as_bool(status.get("error_accounting_available", False)),
        },
        "required_next_controls": controls_for_recommendation(recommendation),
        "allowed_recommendations": VALID_RECOMMENDATIONS,
        "claim_boundary": BOUNDARY,
    }

def controls_for_recommendation(recommendation: str) -> list[str]:
    base = [
        "preserve observable-only boundary",
        "buyer retains labels and final adjudication",
        "candidate-discrepancy memos only",
        "no automated verdict",
        "no production validation claim",
        "no compliance/certification claim",
    ]

    if recommendation == "STOP_UNTIL_LEGAL_CPA_REVIEW":
        return base + ["engage qualified legal and CPA support before proceeding"]

    if recommendation == "PAID_STRATEGIC_PILOT":
        return base + [
            "engage qualified legal and CPA support before money or contract terms",
            "written scope required",
            "acceptance criteria required",
            "payment terms required",
            "no free pilot",
        ]

    if recommendation in {"EXPAND_SAME_WORKFLOW", "TEST_SECOND_WORKFLOW"}:
        return base + ["new bounded scope memo required", "risk gate all new artifacts"]

    if recommendation == "REPEAT_WITH_CLEANER_DATA":
        return base + ["request redaction, cleaner observable export, or field dictionary"]

    return base + ["close or park without further action"]

def main() -> int:
    parser = argparse.ArgumentParser(description="Recommend buyer-safe pilot closeout next step.")
    parser.add_argument("--status-json", required=True, help="Path to pilot status JSON")
    parser.add_argument("--output", default="", help="Optional closeout JSON output path")
    parser.add_argument("--json", action="store_true", help="Print JSON only")
    args = parser.parse_args()

    status = json.loads(Path(args.status_json).read_text(encoding="utf-8"))
    result = closeout(status)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print("Delivery Closeout Recommender")
        print("=" * 72)
        print(f"recommendation: {result['recommendation']}")
        print()
        print("Reasons:")
        for reason in result["reasons"]:
            print(f"  - {reason}")
        print()
        print("Required next controls:")
        for control in result["required_next_controls"]:
            print(f"  - {control}")
        print()
        print(f"Boundary: {BOUNDARY}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
