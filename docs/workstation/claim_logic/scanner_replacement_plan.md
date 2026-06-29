# Scanner Replacement Plan

Status: scaffold
Date: 2026-06-29

## Purpose

Document which blunt scanners should be replaced and in what order.

## Core rule

The word is not the risk.

The claimed authority is the risk.

## Category policy

| Category | Action |
|---|---|
| `SAFE_DENIAL` | `ALLOW` |
| `SAFE_BOUNDARY` | `ALLOW` |
| `UNSAFE_ASSERTION` | `BLOCK_OR_REWRITE` |
| `UNSAFE_CERTIFICATION` | `BLOCK_OR_REWRITE` |
| `UNSAFE_VERDICT` | `BLOCK_OR_REWRITE` |
| `UNSAFE_HIDDEN_MECHANISM` | `BLOCK_OR_REWRITE` |
| `AMBIGUOUS_REVIEW` | `REVIEW` |

## Replacement order

### Priority 1: `tools/pilot_intake/delivery_packet_generator.py`

Reason: Already produced false positives on non-claim boundary language such as does not provide production validation.

Replacement: Use claim_logic_classifier.py category/action results instead of local blunt forbidden phrase scanning.

Planned phase: `phase_5_integrate_claim_logic_with_packet_generator`

### Priority 2: `Phase 7 audit/closeout gates`

Reason: Blunt overclaim scan was suspended during simulator closeout because it punished protective non-claims.

Replacement: Use claim logic categories: allow SAFE_DENIAL and SAFE_BOUNDARY, block UNSAFE_* categories, review AMBIGUOUS_REVIEW.

Planned phase: `phase_6_integrate_claim_logic_with_audit_gates`

### Priority 3: `tools/pilot_intake/red_team_intake_test.py`

Reason: It needed custom negation-aware logic and should eventually share the central classifier.

Replacement: Replace local forbidden phrase logic with claim logic classifier for response posture checks.

Planned phase: `future_cleanup`

### Priority 4: `tools/pilot_intake/folder_policy_checker.py`

Reason: This checker mostly scans artifact placement and file-risk terms; full claim logic integration is lower priority.

Replacement: Keep file placement checks; use claim logic only for client-facing text if needed.

Planned phase: `future_cleanup`

## Non-goals

- Do not remove safety gates.
- Do not weaken boundary language.
- Do not mark legal/compliance/production claims as safe.
- Do not use claim logic as legal advice or compliance certification.
- Do not make autonomous client decisions.

## Boundary

This is scanner replacement planning only.

It does not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdicts, free-pilot commitments, autonomous client action, truth validation, or hidden-mechanism claims.
