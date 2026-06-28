#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ARTIFACT_CLASSES = {
    "trace_data": {
        "target_folder": "02_buyer_exports_observable_only",
        "recommended_output": "normalized trace workspace",
        "keywords": [
            "trace",
            "event log",
            "workflow events",
            "timestamp",
            "sequence",
            "observable events",
            "jsonl",
            "csv export",
            "steps",
            "actions",
            "state transition",
        ],
    },
    "final_state_claim": {
        "target_folder": "01_intake",
        "recommended_output": "scope clarification or claimed-final-state reference",
        "keywords": [
            "final state",
            "claimed final",
            "completion status",
            "ledger state",
            "payment status",
            "resolved",
            "closed",
            "done",
            "final output",
            "claimed completion",
        ],
    },
    "buyer_retained_label_file": {
        "target_folder": "03_labels_buyer_controlled",
        "recommended_output": "label reconciliation input after buyer-controlled reveal",
        "keywords": [
            "label",
            "ground truth",
            "adjudication",
            "human review outcome",
            "true positive",
            "false positive",
            "reviewer decision",
            "buyer labels",
            "validation sheet",
        ],
    },
    "support_context": {
        "target_folder": "04_redaction_and_field_dictionary",
        "recommended_output": "field dictionary, scope clarification, or context note",
        "keywords": [
            "field dictionary",
            "data dictionary",
            "schema",
            "scope memo",
            "redaction",
            "pseudonymization",
            "context",
            "readme",
            "notes",
            "mapping",
            "glossary",
        ],
    },
    "prohibited_internal_material": {
        "target_folder": "PROTECTED",
        "recommended_output": "reject or hold for review",
        "keywords": [
            "model weights",
            "source code",
            "private prompt",
            "system prompt",
            "hidden activation",
            "chain-of-thought",
            "chain of thought",
            "cot",
            "internal architecture",
            "training data",
            "credentials",
            "password",
            "secret key",
            "api key",
            "token",
        ],
    },
    "out_of_scope_material": {
        "target_folder": "DO_NOT_SEND",
        "recommended_output": "scope clarification or reject",
        "keywords": [
            "legal opinion",
            "compliance certification",
            "production incident",
            "urgent production outage",
            "automated verdict",
            "production validation",
            "truth validation",
            "financial advice",
            "medical advice",
            "regulated decision",
            "background check",
        ],
    },
}

DECISION_RULES = {
    "prohibited_internal_material": "REJECT",
    "out_of_scope_material": "HOLD_FOR_REVIEW",
    "trace_data": "ACCEPT",
    "final_state_claim": "ACCEPT",
    "buyer_retained_label_file": "HOLD_FOR_REVIEW",
    "support_context": "ACCEPT",
}

BOUNDARY = (
    "Artifact intake classification only. This does not create legal advice, financial advice, "
    "binding terms, compliance certification, production validation, automated verdicts, free-pilot "
    "commitments, autonomous client action, or hidden-mechanism claims."
)

REDACTION_TERMS = [
    "pii",
    "personal data",
    "email addresses",
    "phone numbers",
    "ssn",
    "social security",
    "patient",
    "medical",
    "hipaa",
    "student record",
    "ferpa",
    "customer names",
    "unredacted",
    "regulated data",
]

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())

def score_classes(text: str) -> dict[str, int]:
    low = normalize(text)
    scores: dict[str, int] = {}
    for artifact_class, cfg in ARTIFACT_CLASSES.items():
        score = 0
        for keyword in cfg["keywords"]:
            if keyword in low:
                score += 2 if " " in keyword else 1
        scores[artifact_class] = score
    return scores

def choose_class(scores: dict[str, int]) -> str:
    # Safety-first tie breakers.
    if scores.get("prohibited_internal_material", 0) > 0:
        return "prohibited_internal_material"
    if scores.get("out_of_scope_material", 0) > 0:
        return "out_of_scope_material"

    ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    if not ranked or ranked[0][1] == 0:
        return "support_context"
    return ranked[0][0]

def redaction_needed(text: str) -> bool:
    low = normalize(text)
    return any(term in low for term in REDACTION_TERMS)

def missing_information(artifact_class: str, text: str) -> list[str]:
    low = normalize(text)
    missing: list[str] = []

    if artifact_class == "trace_data":
        if "timestamp" not in low and "sequence" not in low:
            missing.append("timestamp_or_sequence")
        if "field" not in low and "schema" not in low and "dictionary" not in low:
            missing.append("field_dictionary")
        if "final" not in low and "claimed" not in low:
            missing.append("claimed_final_state_if_available")

    if artifact_class == "final_state_claim":
        if "trace" not in low and "event" not in low:
            missing.append("linked_observable_trace_reference")

    if artifact_class == "buyer_retained_label_file":
        if "buyer" not in low:
            missing.append("buyer_label_ownership_confirmation")
        if "adjudication" not in low and "reviewer" not in low:
            missing.append("human_adjudication_process")

    if artifact_class == "support_context":
        if "scope" not in low and "schema" not in low and "field" not in low:
            missing.append("context_type")

    return missing

def boundary_warnings(artifact_class: str, needs_redaction: bool) -> list[str]:
    warnings = [
        "Use buyer-exported observable materials only.",
        "Do not request model weights, source code, private prompts, hidden activations, or private chain-of-thought.",
        "Buyer retains labels and final adjudication.",
        "Candidate-discrepancy memos only; no automated verdict.",
    ]
    if artifact_class in {"prohibited_internal_material", "out_of_scope_material"}:
        warnings.append("Do not accept this material without review; reject or hold according to policy.")
    if needs_redaction:
        warnings.append("Potential sensitive or regulated data indicated; request redaction or written authorization before intake.")
    return warnings

def classify(description: str, filename: str = "") -> dict[str, Any]:
    text = f"{filename}\n{description}"
    scores = score_classes(text)
    artifact_class = choose_class(scores)
    needs_redaction = redaction_needed(text)

    decision = DECISION_RULES.get(artifact_class, "HOLD_FOR_REVIEW")
    if needs_redaction and decision == "ACCEPT":
        decision = "NEEDS_REDACTION"

    cfg = ARTIFACT_CLASSES[artifact_class]

    return {
        "engine": "artifact_intake_classifier_v1",
        "classified_at_utc": datetime.now(timezone.utc).isoformat(),
        "filename": filename,
        "artifact_type": artifact_class,
        "decision": decision,
        "target_folder": cfg["target_folder"],
        "recommended_output": cfg["recommended_output"],
        "missing_information": missing_information(artifact_class, text),
        "boundary_warnings": boundary_warnings(artifact_class, needs_redaction),
        "needs_redaction": needs_redaction,
        "class_scores": scores,
        "claim_boundary": BOUNDARY,
    }

def main() -> int:
    parser = argparse.ArgumentParser(description="Classify buyer-provided artifact descriptions for buyer-safe pilot intake.")
    parser.add_argument("--description", required=True, help="Plain-language artifact description")
    parser.add_argument("--filename", default="", help="Optional filename")
    parser.add_argument("--json", action="store_true", help="Print JSON only")
    args = parser.parse_args()

    result = classify(args.description, args.filename)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print("Buyer Artifact Intake Classifier")
        print("=" * 72)
        print(f"artifact_type:      {result['artifact_type']}")
        print(f"decision:           {result['decision']}")
        print(f"target_folder:      {result['target_folder']}")
        print(f"recommended_output: {result['recommended_output']}")
        print()
        print("Missing information:")
        for item in result["missing_information"] or ["none"]:
            print(f"  - {item}")
        print()
        print("Boundary warnings:")
        for item in result["boundary_warnings"]:
            print(f"  - {item}")
        print()
        print(f"Boundary: {BOUNDARY}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
