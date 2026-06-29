# SpecShift QA Regression Harness

Status: scaffold
Date: 2026-06-29

## Purpose

Turn trusted SpecShift scripts and safety boundaries into repeatable pytest regression tests.

## Current pytest targets

- `tests/test_claim_logic.py`
- `tests/test_claim_logic_audit_gate.py`
- `tests/test_delivery_packet_generator.py`
- `tests/test_evidence_ledger.py`

## Run

Use the isolated QA venv:

    source .venv_specshift_qa/bin/activate
    python -m pytest

## Boundary

This QA harness is an internal regression scaffold only.

It does not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdict, free pilot commitment, autonomous client action, truth validation, or hidden-mechanism claim.
