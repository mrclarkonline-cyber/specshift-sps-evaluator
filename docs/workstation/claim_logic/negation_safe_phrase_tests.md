# Negation-Safe Phrase Tests

Status: scaffold
Date: 2026-06-29

## Purpose

Ensure the claim logic scanner does not punish protective non-claim language.

## Rule

A risk term inside a denial is not an unsafe claim.

Examples:

- does not provide legal advice
- does not provide production validation
- does not create an automated verdict
- cannot determine model intent
- buyer retains human adjudication

## Test result

All Phase 2 negation-safe phrase tests passed before the workplan was updated.

## Boundary

These are internal scanner tests only.

They do not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdicts, free-pilot commitments, autonomous client action, truth validation, or hidden-mechanism claims.
