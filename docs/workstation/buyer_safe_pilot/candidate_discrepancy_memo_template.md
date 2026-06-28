# Candidate-Discrepancy Memo Template

Status: scaffold  
Date: 2026-06-28

## Memo header

- Project name:
- Buyer workflow:
- Sample window:
- Trace export reference:
- Review date:
- Reviewer:
- Memo status: draft / human-review-needed / delivered / parked

## Scope boundary

This memo reviews buyer-exported observable traces only.

This memo does not evaluate:

- model weights
- source code
- private prompts
- hidden activations
- private chain-of-thought
- internal architecture

This memo is a candidate-discrepancy memo only.

It is not an automated verdict.

## Observable trace summary

Summarize only:

- visible trace fields
- visible sequence
- claimed final state
- buyer-provided labels, if available
- redaction or pseudonymization notes

## Candidate-discrepancy prompts

Use this section to list possible human-review prompts.

| Candidate ID | Observable event or record | Claimed state | Candidate-discrepancy prompt | Trace reference | Limitation | Buyer human review needed |
|---|---|---|---|---|---|---|
| CD-001 |  |  |  |  |  | yes |

## Allowed language

- candidate discrepancy
- review prompt
- possible mismatch
- insufficient information
- requires buyer human adjudication
- observable trace suggests
- bounded review note

## Forbidden language

- verdict
- confirmed failure
- validated defect
- truth determination
- compliance finding
- certification conclusion
- production validation
- automated alert
- legal conclusion
- financial conclusion

## Limitations

This memo does not validate truth.

This memo does not certify compliance.

This memo does not provide legal, financial, or technical production approval.

This memo does not prove a defect.

This memo does not authorize automated action.

## Buyer adjudication

Final determination remains with buyer-controlled human adjudication.

## Next-step options

- buyer human review
- request one bounded additional observable export
- park as insufficient information
- carry forward as ambiguous
- close with no further review

## Boundary

This is a candidate-discrepancy memo scaffold only.

It does not create automated verdicts, truth validation, compliance certification, production validation, legal advice, financial advice, binding terms, free-pilot commitments, or autonomous client action.
