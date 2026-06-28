# Claim-Overstatement Detector

Date created: 2026-06-27
Status: Draft v0.1
Scope: Local language-control guardrail for generated source digests and synthesis reports.

## Tool

tools/pipelines/claim_overstatement_detector.py

## Dry-run

python3 tools/pipelines/claim_overstatement_detector.py --dry-run

## Generate

python3 tools/pipelines/claim_overstatement_detector.py

## Purpose

This detector flags language that may assert more certainty than the source record supports.

It is not a truth engine.

It is not a legal, medical, financial, compliance, scientific, or audit adjudicator.

It is a wording-control guardrail.

## What It Flags

- proof language
- guarantee language
- unsupported validation language
- forbidden advice language
- unsupported intent or causation language

## Safety Boundary

Allowed:

- flag risky language
- preserve source and uncertainty context
- recommend downgrades
- support human review
- protect outward-facing artifacts from overclaiming

Not allowed:

- deciding whether a claim is true
- deciding whether a source is false
- inferring intent
- inferring cause
- replacing legal/medical/financial/compliance review
- silently rewriting source material
- promoting claims to validated conclusions

## Required Warning

This output flags language that may assert more certainty than the source record supports. It does not adjudicate truth, falsity, intent, cause, liability, safety, compliance, investment value, medical validity, or production readiness.

## Safe Replacement Examples

Instead of:

proves

Use:

reports, suggests, is consistent with, or flags for review.

Instead of:

guarantees

Use:

is designed to support reviewer-controlled testing.

Instead of:

validated in production

Use:

not yet validated in live production unless a source and validation record support it.

Instead of:

detects fraud

Use:

flags candidate discrepancies for human review.

## Next Step

After this tool is committed, the next and final workplan item is:

tools/pipelines/low_frequency_anomaly_detector.py

Reason:

The anomaly detector must be built last because it is the highest interpretive-risk layer and requires explicit baseline/null-hypothesis language.
