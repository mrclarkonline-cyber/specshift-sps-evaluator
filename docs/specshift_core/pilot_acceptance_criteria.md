# SpecShift Pilot Acceptance Criteria

Date created: 2026-06-27
Status: Draft v0.1
Audience: Buyer-facing / pilot-scoping-safe
Scope: Acceptance criteria for bounded blind trajectory review pilots.

## Purpose

This document defines buyer-safe pilot acceptance criteria for SpecShift.

A valid pilot should test whether SpecShift can review exported observable workflow traces and return useful structured candidate-discrepancy memos for buyer-retained human adjudication.

The pilot should not require model weights, source code, private prompts, hidden activations, private chain-of-thought, internal architecture, or protected buyer internals beyond the approved pilot dataset.

## Corrected Commercial Status

SpecShift is an early-stage observable-only reliability review layer demonstrated in synthetic environments.

It presents plausible buyer value, but it has not been validated as live production failure-prediction.

Production value must be tested through bounded blind pilots with buyer-retained labels and pre-registered success criteria.

## Core Pilot Question

The pilot should answer this question:

> Given exported observable workflow traces, can SpecShift identify candidate discrepancies that are useful enough for buyer-retained human review to justify further evaluation, procurement, or deployment consideration?

## What the Pilot Tests

The pilot tests whether SpecShift can help reviewers identify:

- Candidate mismatch between visible workflow behavior and claimed final state.
- Possible false completion.
- Possible skipped required step.
- Possible authority, permission, or boundary drift.
- Possible unexplained transition.
- Possible process discontinuity.
- Possible unresolved intermediate issue masked by a final output.
- Ambiguous cases requiring human adjudication.

## What the Pilot Does Not Test

The pilot does not test or claim:

- Guaranteed failure prediction.
- Replacement of human reviewers.
- Full production validation.
- Legal or compliance certification.
- Detection of every failure.
- Causation from trajectory structure alone.
- Access to hidden reasoning or internal model state.
- Broad generalization across all workflows.

## Required Pilot Boundaries

A valid pilot should include:

1. A bounded workflow type.
2. A defined dataset size or review volume.
3. Exported observable workflow traces.
4. Buyer-retained labels.
5. Buyer-controlled ground truth.
6. Pre-registered success criteria.
7. False-positive accounting.
8. False-negative accounting.
9. Ambiguous-case handling.
10. Buyer-retained final adjudication.
11. No code transfer.
12. No training rights.
13. No broad exclusivity by default.
14. No protected method disclosure.

## Dataset Requirements

The buyer should provide or approve a dataset containing exported observable traces.

Each trace should include enough visible sequence information to support review, such as:

- Timestamped workflow events.
- Agent or system actions.
- Tool calls or workflow steps where available.
- Claimed final state or outcome.
- Relevant visible checkpoints.
- Approval or escalation events where available.
- Error, exception, retry, or override events where available.

The pilot should not require hidden model reasoning or private chain-of-thought.

## Label Requirements

The buyer should retain control of ground-truth labels.

Preferred label categories:

- Confirmed discrepancy.
- Confirmed non-discrepancy.
- Ambiguous or insufficient evidence.
- Out of scope.
- Excluded from scoring.

The buyer should not retroactively redefine labels after reviewing SpecShift outputs unless the change is documented and excluded from the primary score.

## Blind Review Design

Where possible, the pilot should be blind.

SpecShift should receive observable traces without final ground-truth labels.

The buyer should retain labels separately until after SpecShift outputs are submitted.

This supports a cleaner evaluation of whether candidate-discrepancy memos align with buyer-controlled ground truth.

## Pre-Registered Success Criteria

Success criteria should be written before review begins.

A pilot may define success using some combination of:

- Precision of candidate-discrepancy flags.
- Recall against buyer-labeled discrepancies.
- False-positive rate.
- False-negative rate.
- Reviewer usefulness rating.
- Time saved in review.
- Quality of explanation in candidate-discrepancy memos.
- Ability to surface cases missed by existing review.
- Comparison against baseline review process.

Do not define success after seeing the outputs.

## Minimum Acceptance Template

A buyer-safe minimum acceptance template:

> The pilot is successful if SpecShift produces candidate-discrepancy memos that meet the pre-registered usefulness and error-accounting thresholds on buyer-retained labels, without requiring protected internals, code transfer, training rights, or hidden reasoning access.

## Suggested Quantitative Measures

Use quantitative measures only when labels support them.

Possible measures:

- True positives: flagged candidate discrepancies later confirmed by buyer labels.
- False positives: flagged candidate discrepancies later rejected by buyer labels.
- True negatives: unflagged traces later confirmed as non-discrepant.
- False negatives: unflagged traces later confirmed as discrepant.
- Precision: confirmed discrepancies among flagged cases.
- Recall: confirmed discrepancies found among all labeled discrepancies.
- False-positive rate: non-discrepant traces incorrectly flagged.
- False-negative rate: discrepant traces missed.

These metrics should be interpreted cautiously when label quality is incomplete or ambiguous.

## Suggested Qualitative Measures

Qualitative measures may include:

- Did the memo help the reviewer understand the issue?
- Did the memo point to the right part of the trajectory?
- Did the memo preserve uncertainty?
- Did the memo avoid unsupported conclusions?
- Did the memo help triage review priority?
- Did the memo identify ambiguity clearly?
- Did the memo avoid exposing protected buyer information beyond the pilot scope?

## Ambiguous-Case Handling

Ambiguous cases should be tracked separately.

Do not hide ambiguous cases inside success counts.

Possible ambiguous labels:

- Insufficient evidence.
- Conflicting trace evidence.
- Buyer label unavailable.
- Trace incomplete.
- Outside pilot scope.
- Requires domain reviewer.

Ambiguous cases may be reported but should not be used to inflate performance claims.

## Baseline Comparison

Where available, compare SpecShift output against a baseline.

Possible baselines:

- Current internal review process.
- Existing monitoring or observability tool.
- Existing eval or test suite.
- Manual reviewer without SpecShift memo.
- Null baseline.

The baseline should use the same dataset and buyer-retained labels where possible.

## Pilot Output

The expected output is a structured candidate-discrepancy memo.

A memo may include:

- Trace identifier.
- Candidate discrepancy summary.
- Relevant observable sequence.
- Claimed final state or expected process.
- Reason for concern.
- Confidence or uncertainty language, if used.
- Ambiguity note.
- Suggested human review question.
- Scope limitation.

The output should not be described as a final verdict.

## Required Safe Output Sentence

Use this sentence where appropriate:

> SpecShift returns structured candidate-discrepancy memos for buyer-retained human review.

## Acceptance Decision Categories

At the end of the pilot, the buyer and SpecShift may classify the result as:

### Pass

The pilot met pre-registered criteria and supports further commercial evaluation.

### Conditional Pass

The pilot showed useful signal but requires narrowed scope, improved data quality, or additional validation.

### Inconclusive

The pilot did not provide enough evidence because of label, dataset, scope, or process limitations.

### Fail

The pilot did not meet pre-registered criteria.

## Commercial Boundary

A pilot should be paid, scoped, and bounded.

Default commercial boundaries:

- No free pilot.
- No code transfer.
- No training rights.
- No broad exclusivity by default.
- No protected method disclosure.
- No open-ended trial.
- No indefinite data access.
- No production deployment claim from pilot alone.

## Legal / Accounting Threshold

At the stage where contracts, procurement, paid pilots, budget, or money movement becomes real, SpecShift should engage CPA and legal support before committing terms.

## Scope-Control Sentence

Use this sentence in packets and outreach where appropriate:

> This packet evaluates the review layer as a standalone applied diagnostic; broader theoretical context is intentionally outside scope and is not required for the proposed blind audit.

## Relationship to Claim Gauntlet

Before release, this document should be checked against:

`docs/specshift_core/claim_gauntlet_overclaim_prevention_checklist.md`

Global release gate:

> This claim is allowed only if it preserves observable-only review, buyer-retained adjudication, bounded validation status, and no protected method disclosure.

## Release Status

Draft v0.1 is suitable for internal review and pilot-scoping preparation.

Do not treat as final contract language without legal review.
