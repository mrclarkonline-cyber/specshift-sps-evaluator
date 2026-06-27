# SpecShift Buyer-Safe Viability Packet Refresh

Date created: 2026-06-27
Status: Draft v0.1
Audience: Buyer-facing / first-send-safe after review
Scope: Refreshed viability packet language aligned to Claim Gauntlet, buyer category page, ΔΔF public explanation, and pilot acceptance criteria.

## Purpose

This packet refresh provides a buyer-safe version of the SpecShift viability case.

It is designed to explain what SpecShift is, why it may matter, how it can be tested, and what it does not yet claim.

This packet should be used only after review against:

- `docs/specshift_core/claim_gauntlet_overclaim_prevention_checklist.md`
- `docs/specshift_core/what_specshift_is_and_is_not.md`
- `docs/specshift_core/ddf_public_explanation_layer.md`
- `docs/specshift_core/pilot_acceptance_criteria.md`

## One-Sentence Buyer Summary

SpecShift is a buyer-controlled, observable-only trajectory review layer that examines exported workflow traces and returns structured candidate-discrepancy memos for buyer-retained human review.

## Corrected Commercial Status

SpecShift is an early-stage observable-only reliability review layer demonstrated in synthetic environments.

It presents plausible buyer value, but it has not been validated as live production failure-prediction.

Production value should be tested through a bounded blind pilot with buyer-retained labels and pre-registered success criteria.

## Scope-Control Sentence

Use this sentence in buyer packets and outreach where appropriate:

> This packet evaluates the review layer as a standalone applied diagnostic; broader theoretical context is intentionally outside scope and is not required for the proposed blind audit.

## Buyer Problem

AI agents, automations, and complex workflows increasingly produce final outputs that may look complete while the observable workflow path contains unresolved gaps, unexplained transitions, skipped steps, or boundary drift.

A buyer may need to know not only what the system claimed at the end, but whether the visible trajectory supports that claim.

SpecShift focuses on that review gap.

## What SpecShift Reviews

SpecShift reviews exported observable workflow traces.

Examples may include:

- Time-ordered workflow events.
- Agent or automation steps.
- Visible tool calls.
- Claimed final states.
- Visible approval or escalation steps.
- Error, retry, exception, or override events.
- Process checkpoints.
- Observable handoffs.

SpecShift does not require hidden reasoning, private chain-of-thought, model weights, source code, private prompts, hidden activations, or internal architecture.

## What SpecShift Returns

SpecShift returns structured candidate-discrepancy memos for buyer-retained human review.

A memo may identify:

- Candidate mismatch between visible trajectory and claimed final state.
- Possible false completion.
- Possible skipped required step.
- Possible authority or permission drift.
- Possible unexplained transition.
- Possible process discontinuity.
- Possible unresolved intermediate issue.
- Ambiguous cases requiring human adjudication.

The memo is not an automated final verdict.

## Why This Is Different

SpecShift may use raw material that overlaps with traces, logs, evals, monitoring, or observability systems.

The overlap is in the raw material.

The category distinction is in the trust architecture.

Conventional trace, eval, and observability tools often support developer-side or operator-side debugging, scoring, dashboards, monitoring, and optimization.

SpecShift is framed as buyer-controlled observable-only trajectory review:

- Exported traces in.
- Candidate-discrepancy memos out.
- Buyer-retained labels.
- Buyer-controlled ground truth.
- Pre-registered pilot criteria.
- Human adjudication retained by the buyer.
- No protected internals required.

## Why It May Matter

A final answer, ledger state, workflow completion marker, or agent report can look clean while the underlying visible sequence contains warning signs.

SpecShift is designed to help reviewers inspect whether the observable path supports the claimed final state.

The value hypothesis is that some important workflow problems may be easier to review when the buyer examines trajectory structure, not just final outputs.

This is a hypothesis for buyer-controlled validation, not a claim of live production proof.

## ΔΔF Relationship, Buyer-Safe Version

ΔΔF provides a simple public way to explain attention to second-order change in observable trajectories.

Plain-language version:

> F(t) shows the visible behavior. ΔF shows how the behavior changes. ΔΔF shows stress in the change pattern.

For buyer-facing SpecShift materials, ΔΔF should be treated as explanatory intuition only.

SpecShift's applied product case does not require a buyer to accept any broader theory.

SpecShift's commercial value must be tested through bounded blind pilots with buyer-retained labels and pre-registered success criteria.

## Candidate Pilot Use Cases

SpecShift may be evaluated in bounded workflow areas such as:

- AI agent task completion review.
- Financial reconciliation workflow review.
- Procurement or approval-flow review.
- Support escalation workflow review.
- Incident response workflow review.
- Automation handoff review.
- Multi-step process completion review.

Each pilot should be scoped to one defined workflow type.

## Pilot Design

A buyer-safe pilot should include:

1. A bounded workflow type.
2. A limited dataset or review volume.
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

## Minimum Pilot Acceptance Template

> The pilot is successful if SpecShift produces candidate-discrepancy memos that meet the pre-registered usefulness and error-accounting thresholds on buyer-retained labels, without requiring protected internals, code transfer, training rights, or hidden reasoning access.

## Evidence Boundary

Current evidence supports:

- Synthetic demonstration.
- Design-layer value.
- Observable-only review framing.
- Candidate-discrepancy memo concept.
- Buyer-controlled pilot readiness.

Current evidence does not yet support:

- Live production failure-prediction claims.
- Guaranteed detection.
- Compliance certification.
- Replacement of human reviewers.
- Broad cross-domain generalization.
- Commercial validation without buyer-side testing.

## What SpecShift Is Not

SpecShift is not:

- A replacement for human review.
- An automated final judgment system.
- A production-validated failure-prediction engine.
- A guarantee that all failures will be detected.
- A compliance certification tool.
- A model-weight inspection tool.
- A source-code audit.
- A private-prompt inspection process.
- A hidden-chain-of-thought review process.
- A dashboard-only observability product.
- A conventional developer-side trace debugger.
- A free consulting engagement.
- A request for code transfer, training rights, or broad exclusivity.

## Protected Method Boundary

This packet should not disclose protected implementation details.

Allowed:

- High-level workflow description.
- Observable-only boundary.
- Buyer-controlled pilot structure.
- Candidate-discrepancy memo description.
- Evidence status.
- Commercial boundary.

Not allowed:

- Protected scoring method.
- Sensitive algorithms.
- Source code.
- Reproducible protected implementation details.
- Private heuristics.
- Internal method details not intended for first-send or first-call materials.

## Commercial Boundary

Default commercial posture:

- Paid pilot.
- Narrow scope.
- Non-exclusive by default.
- No free pilot.
- No code transfer.
- No training rights.
- No broad exclusivity.
- No protected method disclosure.
- No open-ended trial.
- No indefinite data access.
- No production deployment claim from pilot alone.

## Legal / Accounting Threshold

At the stage where contracts, procurement, paid pilots, budget, or money movement becomes real, SpecShift should engage CPA and legal support before committing terms.

## Suggested Buyer Conversation Opening

> SpecShift is an observable-only trajectory review layer. We do not need model weights, source code, private prompts, hidden activations, private chain-of-thought, or internal architecture. The goal of a pilot would be to test whether exported workflow traces can support useful candidate-discrepancy memos for your human reviewers, using your labels and pre-registered success criteria.

## Suggested First-Send Summary

> I am reaching out about SpecShift, a buyer-controlled observable-only trajectory review layer for reviewing exported workflow traces. It returns structured candidate-discrepancy memos for human review and does not require model weights, source code, private prompts, hidden activations, private chain-of-thought, or internal architecture. The current status is early-stage and pilot-ready: demonstrated in synthetic environments, with production value to be tested through a bounded blind pilot using buyer-retained labels and pre-registered success criteria.

## Claim Gauntlet Final Check

Before release, every claim in this packet must pass this gate:

> This claim is allowed only if it preserves observable-only review, buyer-retained adjudication, bounded validation status, and no protected method disclosure.

## Release Status

Draft v0.1 is suitable for internal review.

Do not treat as final buyer copy until it has passed the Claim Gauntlet and any needed legal/commercial review.
