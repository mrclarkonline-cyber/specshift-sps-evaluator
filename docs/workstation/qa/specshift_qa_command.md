# specshift_qa Command

Status: scaffold
Date: 2026-06-29

## Purpose

Run the core SpecShift QA regression harness from one command.

## Command

    python3 tools/status/specshift_qa.py

or:

    tools/bin/specshift_qa

## Current checks

- pytest regression suite
- claim logic safe-denial classifier smoke check
- claim logic safe audit gate
- claim logic unsafe audit gate expected-block check
- delivery packet generator smoke check
- evidence ledger summary smoke check

## Boundary

This command is an internal workstation QA scaffold only.

It does not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdict, free pilot commitment, autonomous client action, truth validation, or hidden-mechanism claim.
