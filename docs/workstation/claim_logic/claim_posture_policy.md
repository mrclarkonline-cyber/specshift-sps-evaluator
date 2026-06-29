# Claim Posture Policy

Status: scaffold
Date: 2026-06-29

## Purpose

Replace blunt keyword scanning with claim-posture classification.

## Core rule

The word is not the risk.

The claimed authority is the risk.

## Categories

- SAFE_DENIAL
- SAFE_BOUNDARY
- UNSAFE_ASSERTION
- UNSAFE_CERTIFICATION
- UNSAFE_VERDICT
- UNSAFE_HIDDEN_MECHANISM
- AMBIGUOUS_REVIEW

## Examples

SAFE_DENIAL:

- SpecShift does not provide production validation.
- This is not legal advice.
- This packet does not create an automated verdict.

SAFE_BOUNDARY:

- Buyer retains human adjudication.
- This is an observable-only candidate-discrepancy memo.

UNSAFE_ASSERTION:

- SpecShift validates production safety.
- We prove the system is safe.

UNSAFE_CERTIFICATION:

- We certify compliance.
- This certifies that the AI is compliant.

UNSAFE_VERDICT:

- Automated verdict: pass.
- Verdict: approved.

UNSAFE_HIDDEN_MECHANISM:

- The model intended to deceive.
- We determine hidden intent.

AMBIGUOUS_REVIEW:

- Production validation is discussed without a clear denial or boundary.

## Boundary

This policy is an internal claim-posture scaffold only.

It does not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdicts, free-pilot commitments, autonomous client action, truth validation, or hidden-mechanism claims.
