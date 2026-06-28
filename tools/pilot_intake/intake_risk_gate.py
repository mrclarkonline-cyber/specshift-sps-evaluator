#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from typing import Any

BOUNDARY = (
    "Intake risk gate only. This does not create legal advice, financial advice, binding terms, "
    "compliance certification, production validation, automated verdicts, free-pilot commitments, "
    "autonomous client action, or hidden-mechanism claims."
)

REJECT_TERMS = {
    "source_code": [
        "source code",
        "repository",
        "repo dump",
        "github zip",
        "implementation code",
        "python package",
        "private library",
    ],
    "model_weights": [
        "model weights",
        "checkpoint",
        "ckpt",
        "safetensors",
        "weights file",
        "fine-tuned model",
    ],
    "private_prompts": [
        "private prompt",
        "system prompt",
        "developer prompt",
        "hidden prompt",
        "prompt chain",
    ],
    "private_chain_of_thought": [
        "private chain-of-thought",
        "chain-of-thought",
        "chain of thought",
        "cot",
        "hidden reasoning",
        "scratchpad",
    ],
    "hidden_activations": [
        "hidden activation",
        "activation dump",
        "latent state",
        "internal activations",
        "attention maps",
    ],
    "secrets": [
        "password",
        "api key",
        "secret key",
        "token",
        "credential",
        "private key",
        "ssh key",
        "oauth",
    ],
}

HOLD_TERMS = {
    "customer_pii": [
        "pii",
        "personal data",
        "customer names",
        "email addresses",
        "phone numbers",
        "addresses",
        "unredacted",
        "ssn",
        "social security",
    ],
    "regulated_data": [
        "hipaa",
        "medical",
        "patient",
        "health record",
        "student record",
        "ferpa",
        "financial account",
        "bank account",
        "credit card",
        "regulated data",
    ],
    "legal_compliance_request": [
        "legal opinion",
        "legal conclusion",
        "compliance certification",
        "compliance finding",
        "certify compliance",
        "regulatory approval",
        "audit opinion",
    ],
    "production_incident": [
        "production incident",
        "urgent outage",
        "incident response",
        "live production",
        "real-time monitoring",
        "production monitoring",
    ],
    "out_of_scope": [
        "automated verdict",
        "truth validation",
        "production validation",
        "guaranteed detection",
        "autonomous action",
        "financial advice",
        "medical advice",
    ],
}

ACCEPT_HINTS = [
    "observable trace",
    "event log",
    "workflow events",
    "timestamp",
    "sequence",
    "field dictionary",
    "redaction note",
    "pseudonymized",
    "claimed final state",
    "buyer label",
    "human adjudication",
    "scope memo",
]

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())

def find_hits(text: str, catalog: dict[str, list[str]]) -> list[dict[str, Any]]:
    low = normalize(text)
    hits: list[dict[str, Any]] = []
    for category, terms in catalog.items():
        for term in terms:
            if term in low:
                hits.append({"category": category, "term": term})
    return hits

def accept_hints(text: str) -> list[str]:
    low = normalize(text)
    return [term for term in ACCEPT_HINTS if term in low]

def gate(description: str, filename: str = "", artifact_type: str = "") -> dict[str, Any]:
    text = f"{filename}\n{artifact_type}\n{description}"

    reject_hits = find_hits(text, REJECT_TERMS)
    hold_hits = find_hits(text, HOLD_TERMS)
    hints = accept_hints(text)

    if reject_hits:
        decision = "REJECT"
        target_folder = "PROTECTED"
        required_action = "Do not accept this artifact. Ask buyer to remove protected/internal material and resend only observable exports if appropriate."
    elif hold_hits:
        if any(hit["category"] in {"customer_pii", "regulated_data"} for hit in hold_hits):
            decision = "NEEDS_REDACTION"
            target_folder = "DO_NOT_SEND"
            required_action = "Request redaction, pseudonymization, written terms, or professional review before intake."
        else:
            decision = "HOLD_FOR_REVIEW"
            target_folder = "DO_NOT_SEND"
            required_action = "Pause intake and require human/professional review before accepting."
    elif hints:
        decision = "ACCEPT"
        target_folder = "02_buyer_exports_observable_only" if "trace" in " ".join(hints) or "event" in " ".join(hints) else "01_intake"
        required_action = "Accept only into the appropriate buyer-safe pilot folder and preserve provenance."
    else:
        decision = "HOLD_FOR_REVIEW"
        target_folder = "01_intake"
        required_action = "Ask for scope clarification and confirm this is observable-only before accepting."

    warnings = [
        "Do not accept model weights, source code, private prompts, hidden activations, or private chain-of-thought.",
        "Do not accept secrets, credentials, keys, tokens, or passwords.",
        "Do not accept unredacted sensitive/regulated data without written terms and professional review.",
        "Do not accept requests for legal/compliance conclusions, production validation, automated verdicts, or truth validation.",
        "Buyer retains labels and final adjudication.",
    ]

    if decision in {"REJECT", "HOLD_FOR_REVIEW", "NEEDS_REDACTION"}:
        warnings.append("Do not route into working review until the risk gate is resolved.")

    return {
        "engine": "intake_risk_gate_v1",
        "gated_at_utc": datetime.now(timezone.utc).isoformat(),
        "filename": filename,
        "artifact_type": artifact_type,
        "decision": decision,
        "target_folder": target_folder,
        "required_action": required_action,
        "reject_hits": reject_hits,
        "hold_hits": hold_hits,
        "accept_hints": hints,
        "boundary_warnings": warnings,
        "claim_boundary": BOUNDARY,
    }

def main() -> int:
    parser = argparse.ArgumentParser(description="Risk-gate buyer artifacts before routing.")
    parser.add_argument("--description", required=True, help="Plain-language artifact description")
    parser.add_argument("--filename", default="", help="Optional filename")
    parser.add_argument("--artifact-type", default="", help="Optional classifier artifact type")
    parser.add_argument("--json", action="store_true", help="Print JSON only")
    args = parser.parse_args()

    result = gate(args.description, args.filename, args.artifact_type)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print("Buyer Artifact Intake Risk Gate")
        print("=" * 72)
        print(f"decision:        {result['decision']}")
        print(f"target_folder:   {result['target_folder']}")
        print(f"required_action: {result['required_action']}")
        print()
        print("Reject hits:")
        for item in result["reject_hits"] or ["none"]:
            print(f"  - {item}")
        print()
        print("Hold/redaction hits:")
        for item in result["hold_hits"] or ["none"]:
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
