# Claim Logic Audit Gate

Status: scaffold
Date: 2026-06-29

## Purpose

Use `claim_logic_classifier.py` in audit and closeout gates.

## Behavior

- `SAFE_DENIAL` passes.
- `SAFE_BOUNDARY` passes.
- `UNSAFE_ASSERTION` fails.
- `UNSAFE_CERTIFICATION` fails.
- `UNSAFE_VERDICT` fails.
- `UNSAFE_HIDDEN_MECHANISM` fails.
- `AMBIGUOUS_REVIEW` returns review status by default.
- `AMBIGUOUS_REVIEW` fails only when `--fail-on-review` is used.

## Command

    python3 tools/claim_logic/claim_logic_audit_gate.py --file docs/workstation/buyer_artifact_simulator/sample_delivery_packet.md --output /tmp/claim_gate.json

## Boundary

This audit gate is an internal scanner scaffold only.

It does not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdicts, free-pilot commitments, autonomous client action, truth validation, or hidden-mechanism claims.
