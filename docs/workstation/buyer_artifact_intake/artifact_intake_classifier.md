# Artifact Intake Classifier

Status: scaffold  
Date: 2026-06-28

## Purpose

Classify buyer-provided artifacts or artifact descriptions before routing them into a buyer-safe pilot folder.

The classifier answers:

- artifact type
- accept, hold, reject, or needs redaction
- target folder
- recommended SpecShift output
- missing information
- boundary warnings

## Command

Run a plain-text classification:

    python3 tools/pilot_intake/artifact_intake_classifier.py --filename "workflow_events.csv" --description "CSV export of observable workflow events with timestamp and claimed final state"

Run JSON output:

    python3 tools/pilot_intake/artifact_intake_classifier.py --filename "workflow_events.csv" --description "CSV export of observable workflow events with timestamp and claimed final state" --json

## Artifact classes

- trace_data
- final_state_claim
- buyer_retained_label_file
- support_context
- prohibited_internal_material
- out_of_scope_material

## Decisions

- ACCEPT
- HOLD_FOR_REVIEW
- REJECT
- NEEDS_REDACTION

## Routing folders

- 01_intake
- 02_buyer_exports_observable_only
- 03_labels_buyer_controlled
- 04_redaction_and_field_dictionary
- DO_NOT_SEND
- PROTECTED

## Safety-first behavior

The classifier rejects or holds likely protected/internal/out-of-scope materials before ordinary routing.

It flags possible sensitive or regulated data for redaction.

## Boundary

This is an artifact intake classification scaffold only.

It does not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdicts, free-pilot commitments, autonomous client action, or hidden-mechanism claims.
