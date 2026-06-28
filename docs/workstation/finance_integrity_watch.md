# Finance Integrity Watch

Date created: 2026-06-27
Status: Draft v0.1
Scope: Finance-workflow relevance synthesis from local public-source digests.

## Tool

tools/pipelines/finance_integrity_watch.py

## Dry-run

python3 tools/pipelines/finance_integrity_watch.py --dry-run

## Generate

python3 tools/pipelines/finance_integrity_watch.py

## Purpose

This tool scans local generated digests for finance-workflow terms related to reconciliation, settlement, ledger state, payments, billing, invoicing, close process, and audit/control traceability.

## Safety Boundary

Allowed:

- finance workflow triage
- buyer role hypothesis
- reconciliation/ledger workflow fit hypothesis
- source-linked review

Not allowed:

- investment advice
- trading signals
- compliance certification
- audit opinion
- legal advice
- fraud conclusion
- severity scoring unless buyer-defined

## Safe Sentence

SpecShift compares observable reconciliation or finance workflow traces against claimed final ledger or payment states and returns structured candidate-discrepancy memos for reviewer-controlled testing.
