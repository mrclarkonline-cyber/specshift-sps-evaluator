# Unsafe Assertion Tests

Status: scaffold
Date: 2026-06-29

## Purpose

Ensure the claim logic scanner blocks unsafe affirmative authority claims.

## Unsafe categories tested

- UNSAFE_ASSERTION
- UNSAFE_CERTIFICATION
- UNSAFE_VERDICT
- UNSAFE_HIDDEN_MECHANISM
- AMBIGUOUS_REVIEW

## Rule

The scanner should block or rewrite affirmative claims that imply SpecShift is certifying, validating, proving, issuing verdicts, or determining hidden mechanisms.

## Examples blocked

- We certify compliance.
- SpecShift validates production safety.
- Automated verdict: pass.
- The model intended to deceive.
- Internal reasoning proves deception.

## Ambiguous review

Some language should not be automatically blocked, but should require review.

Example:

- Production validation may be relevant here.

## Test result

All Phase 3 unsafe assertion tests passed before the workplan was updated.

## Boundary

These are internal scanner tests only.

They do not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdicts, free-pilot commitments, autonomous client action, truth validation, or hidden-mechanism claims.
