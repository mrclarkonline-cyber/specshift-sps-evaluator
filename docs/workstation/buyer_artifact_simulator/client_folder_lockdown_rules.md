# Client Folder Lockdown Rules

Status: scaffold
Date: 2026-06-28

## Purpose

Define what can and cannot live in each buyer-safe client project folder.

## 01_received_observable_traces

Required note: Raw exported observable traces only.

Allowed:
- observable trace exports
- raw buyer-exported observable event files

Forbidden:
- model weights
- source code
- private prompts
- hidden activations
- private chain-of-thought
- secrets
- credentials
- unredacted regulated data

## 02_sanitized_working_data

Required note: Only redacted or normalized working data.

Allowed:
- redacted normalized working copies
- pseudonymized trace files
- normalized trace templates

Forbidden:
- raw secrets
- credentials
- model weights
- source code
- private prompts
- private chain-of-thought

## 03_review_notes

Required note: Internal review notes only.

Allowed:
- internal review notes
- scope notes
- limitations
- review prompts

Forbidden:
- final legal conclusions
- financial conclusions
- compliance certification
- production validation
- automated verdicts

## 04_candidate_discrepancy_memos

Required note: Candidate-discrepancy memos only.

Allowed:
- candidate-discrepancy memo drafts
- human-review prompts
- limitations

Forbidden:
- validated defect claims
- confirmed failure claims
- truth validation
- compliance certification
- automated verdicts

## 05_delivery_packet

Required note: Client-facing bounded delivery only.

Allowed:
- client-facing package
- scope boundary
- limitations
- candidate memo index
- buyer questions
- next-step recommendation

Forbidden:
- legal advice
- financial advice
- binding terms
- compliance certification
- production validation
- truth validation
- automated verdicts

## 06_post_pilot_feedback

Required note: Post-pilot feedback and authorized label reconciliation only.

Allowed:
- buyer feedback
- buyer label reconciliation if provided
- closeout notes
- next-step decision

Forbidden:
- buyer labels without authorization
- new raw traces without risk gate
- contract terms without counsel
- payment terms without CPA/legal review

## DO_NOT_SEND

Required note: Material not approved for external sending.

Allowed:
- held material
- unapproved drafts
- materials pending review

Forbidden:
- client-facing delivery files

## PROTECTED

Required note: Protected/quarantined material only.

Allowed:
- restricted material requiring review
- quarantined accidental internal/prohibited material

Forbidden:
- external delivery files
- public materials

## Boundary

These rules are internal buyer-safe folder controls only.

They do not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdicts, free-pilot commitments, autonomous client action, truth validation, or hidden-mechanism claims.
