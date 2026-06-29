# Lint and Style Gate

Status: advisory
Date: 2026-06-29

## Purpose

Add lint and style visibility without making style failures block business-critical work too early.

## Hard gate

The hard QA gate is:

    python3 tools/status/specshift_qa.py

This must pass before a QA phase is promoted.

## Advisory checks

Recommended advisory commands:

    source .venv_specshift_qa/bin/activate
    ruff check tools tests
    shellcheck tools/bin/specshift_qa

## Rule

Lint findings should be reviewed and fixed when practical, but Phase 3 does not make style warnings a release blocker.

## Why advisory first

SpecShift is still stabilizing its workstation scaffolds. The important immediate safety property is repeatable functional regression testing. Style gates can become stricter after the QA harness is stable.

## Boundary

This lint and style gate is an internal QA scaffold only.

It does not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdict, free pilot commitment, autonomous client action, truth validation, or hidden-mechanism claim.
