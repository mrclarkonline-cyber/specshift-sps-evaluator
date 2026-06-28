# Claim Safety Gate

Date created: 2026-06-27
Status: Draft v0.1
Scope: Lightweight local claim-safety scan for generated markdown digests.

## Tool

tools/pipelines/claim_safety_gate.py

## Dry-run

python3 tools/pipelines/claim_safety_gate.py --dry-run

## Scan reports

python3 tools/pipelines/claim_safety_gate.py --path reports/fast_relevance

## Boundary

This is a first-pass guardrail, not a truth adjudicator. It flags missing provenance/uncertainty markers and risky overclaiming phrases.
