# What SpecShift Is and Is Not

Date created: 2026-06-27
Status: Draft v0.1
Audience: Buyer-facing / first-call-safe
Scope: Plain-English category explanation with protected method withheld.

## One-Sentence Description

SpecShift is an observable-only trajectory review layer that examines exported workflow traces and returns structured candidate-discrepancy memos for buyer-retained human review.

## Plain-English Version

SpecShift helps a buyer review what an AI agent, automation, or complex workflow visibly did over time.

It does not require model weights, source code, private prompts, hidden activations, private chain-of-thought, or internal architecture.

The buyer supplies or controls the observable workflow records. SpecShift reviews the visible trajectory and helps identify places where the workflow may not align with the claimed final result, expected process, or control boundary.

The output is not an automatic final verdict. It is a structured memo for human review.

## Corrected Commercial Status

SpecShift is an early-stage observable-only reliability review layer demonstrated in synthetic environments.

It presents plausible buyer value, but it has not been validated as live production failure-prediction.

Production value should be tested through a bounded blind pilot with buyer-retained labels and pre-registered success criteria.

## What SpecShift Is

SpecShift is:

- An observable-only trajectory review layer.
- A buyer-controlled review process.
- A way to examine exported, time-ordered workflow behavior.
- A candidate-discrepancy memo generator.
- A pilot-ready diagnostic layer for bounded blind testing.
- A review aid for human adjudication.
- A way to test whether visible workflow behavior aligns with claimed final states.
- A boundary-preserving process that does not require access to protected internals.

## What SpecShift Is Not

SpecShift is not:

- A replacement for human reviewers.
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

## The Category Distinction

SpecShift may use some of the same raw material that appears in trace tools, eval tools, monitoring tools, or observability systems.

The category distinction is not the raw material alone.

The category distinction is the trust architecture.

Safe category line:

> The overlap is in the raw material. The category distinction is in the trust architecture.

Conventional trace, eval, and observability tools often serve developer or operator-side monitoring, debugging, scoring, dashboarding, or optimization workflows.

SpecShift is framed differently:

- Exported observable traces in.
- Candidate-discrepancy memos out.
- Buyer-retained labels.
- Buyer-controlled ground truth.
- Pre-registered pilot criteria.
- Human adjudication retained by the buyer.
- No protected internals required.

## Buyer-Controlled Review

A valid SpecShift pilot should preserve buyer control.

The buyer should retain:

- Ground-truth labels.
- Final adjudication.
- Success criteria.
- Dataset selection or approval.
- Ambiguous-case handling.
- False-positive and false-negative review.
- Final decision authority.

SpecShift should not control the final label set or retroactively adjust criteria after seeing outputs.

## Observable-Only Boundary

SpecShift can be evaluated using exported observable workflow traces.

It does not require:

- Model weights.
- Source code.
- Private prompts.
- Hidden activations.
- Private chain-of-thought.
- Internal architecture.
- Full internal telemetry access.
- Training data.
- Customer secrets beyond the approved pilot dataset.

This boundary is part of the value proposition. It allows the buyer to test the review layer without handing over unnecessary internal access.

## What the Output Looks Like

A SpecShift output should be understood as a structured review memo.

The memo may identify:

- Candidate mismatches between visible behavior and claimed outcome.
- Possible completion gaps.
- Possible authority or permission drift.
- Possible unexplained transitions.
- Possible process discontinuities.
- Ambiguous cases needing human review.

The memo should not be described as a final verdict.

Preferred wording:

> SpecShift returns structured candidate-discrepancy memos for buyer-retained human review.

## Pilot-Ready Framing

A safe pilot should be bounded, paid, and blind where possible.

A buyer-safe pilot should include:

- A defined workflow type.
- A limited dataset.
- Buyer-retained labels.
- Pre-registered success criteria.
- False-positive accounting.
- False-negative accounting.
- Ambiguous-case handling.
- A comparison baseline where available.
- No code transfer.
- No training rights.
- No broad exclusivity by default.

## What SpecShift Can Help Test

SpecShift can help a buyer test whether observable workflow behavior contains candidate discrepancies that merit review.

Possible pilot questions:

- Did the visible trajectory support the claimed final state?
- Did the workflow skip a required step?
- Did the agent appear to exceed or drift beyond an expected boundary?
- Did the final output mask unresolved intermediate problems?
- Did the visible process contain unexplained transitions?
- Did the workflow appear complete when the observable record suggests otherwise?

## What SpecShift Does Not Claim

SpecShift does not currently claim:

- Proven live production failure prediction.
- Guaranteed prevention of failures.
- Replacement of existing controls.
- Complete detection of all workflow issues.
- Legal, compliance, or audit certification.
- Access to hidden model reasoning.
- Proof that broader theoretical claims are correct.
- Commercial validation without buyer-side testing.

## Scope-Control Sentence

Use this sentence in packets and outreach where appropriate:

> This packet evaluates the review layer as a standalone applied diagnostic; broader theoretical context is intentionally outside scope and is not required for the proposed blind audit.

## Safer Buyer-Facing Summary

SpecShift is a buyer-controlled, observable-only trajectory review layer.

It reviews exported workflow traces and returns structured candidate-discrepancy memos for human adjudication.

It is designed for bounded blind pilot testing where the buyer retains labels, criteria, ground truth, and final decision authority.

It does not require protected internals and does not claim production-validated failure prediction.

## Claim Gauntlet Link

Before release, this page should be checked against:

`docs/specshift_core/claim_gauntlet_overclaim_prevention_checklist.md`

Global release gate:

> This claim is allowed only if it preserves observable-only review, buyer-retained adjudication, bounded validation status, and no protected method disclosure.

## Release Status

Draft v0.1 is suitable for internal review.

Do not treat as final buyer copy until it has been checked against the Claim Gauntlet and the pilot acceptance criteria document.
