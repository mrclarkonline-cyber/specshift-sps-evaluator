# SpecShift AI-for-Science Simulation Fidelity Packet

Date created: 2026-06-27
Status: Draft v0.1
Audience: Research-facing / buyer-safe / pilot-scoping-safe
Scope: Observable-only trajectory review for AI-for-science simulation fidelity, discrepancy review, and model-output integrity.

## One-Sentence Summary

SpecShift reviews exported AI-for-science simulation trajectories and returns structured candidate-discrepancy memos for researcher-retained human adjudication.

## Corrected Commercial Status

SpecShift is an early-stage observable-only reliability review layer demonstrated in synthetic environments.

It presents plausible buyer and research value, but it has not been validated as live production failure-prediction or scientific truth verification.

Simulation-fidelity value should be tested through a bounded blind pilot with researcher-retained labels and pre-registered success criteria.

## Scope-Control Sentence

> This packet evaluates the review layer as a standalone applied diagnostic; broader theoretical context is intentionally outside scope and is not required for the proposed blind audit.

## Research Problem

AI-for-science systems can produce simulation outputs, forecasts, candidate structures, or modeled trajectories that appear plausible at the final state.

But a final output may look acceptable while the visible simulation trajectory contains unresolved strain, unexplained transitions, unstable intermediate behavior, skipped constraints, discontinuities, or mismatches between process and claim.

SpecShift focuses on reviewing the observable trajectory, not asserting scientific truth.

## What SpecShift Reviews

SpecShift reviews exported observable simulation or workflow traces.

Possible inputs include:

- Time-ordered simulation states.
- Model-generated candidate trajectories.
- Intermediate checkpoints.
- Constraint checks.
- Energy, stability, loss, or residual summaries where available.
- Claimed final state.
- Evaluation logs.
- Solver steps.
- Retry or correction events.
- Human review checkpoints.
- Validation or comparison outputs.
- Observable model workflow events.

SpecShift does not require model weights, source code, private prompts, hidden activations, private chain-of-thought, or internal architecture.

## What SpecShift Returns

SpecShift returns structured candidate-discrepancy memos.

A memo may identify:

- Candidate mismatch between trajectory and claimed final state.
- Possible unstable intermediate transition.
- Possible unexplained discontinuity.
- Possible constraint inconsistency.
- Possible false completion.
- Possible unsupported convergence claim.
- Possible discrepancy between visible process and final assertion.
- Ambiguous case requiring researcher adjudication.

The memo is not a scientific verdict.

## What This Does Not Claim

SpecShift does not claim:

- Scientific proof.
- Discovery validation.
- Replacement of domain experts.
- Production-validated failure prediction.
- Guaranteed simulation error detection.
- Certification of model correctness.
- Causation from trajectory structure alone.
- Full fidelity validation across all scientific domains.
- Access to hidden model reasoning or internals.

## Candidate Research Use Cases

Potential pilot areas include:

- Physics simulation trajectory review.
- Materials candidate stability review.
- Climate or fluid simulation workflow review.
- Molecular or protein candidate workflow review.
- Astronomy or cosmology simulation review.
- Agentic AI-for-science workflow review.
- Multi-step computational experiment review.
- Scientific claim-to-process consistency review.
- Solver or model convergence review.
- Synthetic benchmark replay.

Each pilot should be scoped to one bounded simulation or workflow type.

## Observable Trace Requirements

A pilot should define the observable trace format in advance.

Useful trace components may include:

- State sequence.
- Input parameters.
- Claimed output or final state.
- Intermediate checkpoints.
- Constraint or conservation checks where available.
- Residuals or error summaries where available.
- Failure, retry, or correction events.
- Evaluation metrics.
- Human review notes where included.
- Comparison baseline outputs.

The trace should be sufficient for trajectory review without requiring hidden internals.

## Pilot Design

A research-facing pilot should include:

1. One bounded simulation or workflow type.
2. Exported observable trajectories.
3. Researcher-retained labels.
4. Researcher-controlled ground truth or adjudication standard.
5. Pre-registered success criteria.
6. False-positive accounting.
7. False-negative accounting.
8. Ambiguous-case handling.
9. Baseline comparison where available.
10. Human expert adjudication.
11. No code transfer.
12. No training rights.
13. No protected method disclosure.
14. No claim that SpecShift proves scientific correctness.

## Label Categories

Preferred label categories:

- Confirmed discrepancy.
- Confirmed non-discrepancy.
- Ambiguous or insufficient evidence.
- Out of scope.
- Excluded from scoring.

Optional science-specific sublabels:

- Unsupported convergence.
- Constraint mismatch.
- Stability inconsistency.
- Trajectory discontinuity.
- Residual / final-state mismatch.
- Boundary-condition mismatch.
- Solver-step anomaly.
- Intermediate-state inconsistency.
- Unsupported final claim.

## Pre-Registered Success Criteria

A pilot may evaluate:

- Precision of candidate-discrepancy flags.
- Recall against researcher-labeled discrepancies.
- False-positive rate.
- False-negative rate.
- Expert usefulness rating.
- Ability to surface cases missed by baseline review.
- Quality of trace-grounded explanation.
- Ability to identify ambiguous cases without overclaiming.
- Comparison against existing evaluation or validation workflow.

Do not define success after seeing SpecShift outputs.

## Minimum Acceptance Template

> The pilot is successful if SpecShift produces candidate-discrepancy memos that meet pre-registered usefulness and error-accounting thresholds on researcher-retained labels, without requiring protected internals, code transfer, training rights, hidden reasoning access, or claims of scientific proof.

## Baseline Comparison

Where possible, compare SpecShift against:

- Existing model evaluation workflow.
- Human expert review without SpecShift memo.
- Existing simulation validation checks.
- Standard residual or error checks.
- Current benchmark process.
- Null baseline.

The baseline should use the same scoped trajectories and retained labels where possible.

## Buyer / Researcher Control Boundary

The buyer or research team retains:

- Labels.
- Ground truth.
- Scientific adjudication.
- Dataset approval.
- Success criteria.
- Baseline selection.
- Ambiguous-case treatment.
- Final decision authority.

SpecShift should not control scientific truth claims.

## Relationship to ΔΔF

ΔΔF can provide a public intuition for second-order attention to simulation trajectories.

Safe explanation:

> F(t) shows the visible behavior. ΔF shows how the behavior changes. ΔΔF shows stress in the change pattern.

For this packet, ΔΔF is explanatory intuition only.

It should not be treated as proof of scientific validity, discovery, or causation.

## Research-Safe Outreach Blurb

> I am reaching out about SpecShift, an observable-only trajectory review layer for AI-for-science workflows. The narrow pilot question is whether exported simulation or workflow traces can support useful candidate-discrepancy memos for researcher-retained human adjudication. SpecShift does not require model weights, source code, private prompts, hidden activations, private chain-of-thought, or internal architecture. The current status is early-stage and pilot-ready: demonstrated in synthetic environments, with research value to be tested through a bounded blind pilot using retained labels and pre-registered success criteria.

## First Call Opening

> SpecShift reviews exported observable AI-for-science trajectories and returns structured candidate-discrepancy memos for human review. We are not asking for model weights, source code, private prompts, hidden activations, private chain-of-thought, or internal architecture. The purpose of this call is to determine whether one bounded simulation or workflow type has enough trace data, adjudication standards, and review pain to justify a pilot.

## Protected Method Boundary

Do not disclose:

- Protected scoring method.
- Source code.
- Sensitive algorithms.
- Private heuristics.
- Reproducible protected implementation details.
- Internal method notes.

Safe language:

> I can describe the review structure, pilot boundary, input/output expectations, and validation design. Protected implementation details are not part of first-contact materials and would require appropriate commercial and legal terms before disclosure.

## Legal / Accounting Trigger

If the discussion turns toward contracts, procurement, paid pilots, budget, pricing, exclusivity, data rights, code access, security terms, publication rights, or money movement, pause before committing terms and engage CPA/legal support.

## Relationship to Core SpecShift Documents

This packet should be checked against:

- `docs/specshift_core/claim_gauntlet_overclaim_prevention_checklist.md`
- `docs/specshift_core/what_specshift_is_and_is_not.md`
- `docs/specshift_core/ddf_public_explanation_layer.md`
- `docs/specshift_core/pilot_acceptance_criteria.md`
- `docs/specshift_core/buyer_safe_viability_packet_refresh.md`

## Global Release Gate

> This claim is allowed only if it preserves observable-only review, buyer-retained adjudication, bounded validation status, and no protected method disclosure.

## Release Status

Draft v0.1 is suitable for internal review and AI-for-science pilot scoping.

Do not treat as scientific validation, legal language, procurement language, or publication-ready claims.
