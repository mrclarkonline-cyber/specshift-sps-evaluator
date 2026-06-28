# SpecShift Normalized Trace Schema

Status: scaffold  
Date: 2026-06-28

## Purpose

Create one standard review shape for accepted buyer-exported observable traces.

Different buyers may send different field names. The normalizer maps them into this shape.

## Normalized fields

| Field | Purpose | Required |
|---|---|---|
| `trace_id` | Stable trace, case, record, workflow, ticket, or generated row identifier. | yes |
| `timestamp` | Observable event time, sequence time, or ordered step marker. | no |
| `actor_system` | Visible actor, system, service, component, or pseudonymized identifier. | no |
| `step_action` | Visible workflow step, action, event type, operation, or state transition. | yes |
| `input_context` | Visible input, request, trigger, context, or input summary if available. | no |
| `claimed_output` | Visible output, response, result, or claimed result if available. | no |
| `final_state` | Claimed final state, status, completion state, ledger/payment state, or endpoint if available. | no |
| `observable_evidence` | Source row, log reference, trace reference, or supporting observable record. | yes |
| `notes` | Limitations, review notes, redaction notes, or bounded context. | no |

## Command

Normalize a CSV:

    python3 tools/pilot_intake/trace_schema_normalizer.py --input tests/fixtures/pilot_intake/sample_buyer_trace.csv --output /tmp/normalized_trace.csv --report /tmp/normalized_trace_report.json

## Boundary

Only accepted observable trace artifacts should be normalized.

Do not normalize protected/internal material, unredacted regulated data, source code, model weights, private prompts, hidden activations, or private chain-of-thought.

This schema does not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdicts, free-pilot commitments, autonomous client action, truth validation, or hidden-mechanism claims.
