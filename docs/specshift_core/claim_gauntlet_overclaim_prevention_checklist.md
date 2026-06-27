# SpecShift Claim Gauntlet / Overclaim-Prevention Checklist

Date created: 2026-06-27
Status: Draft v0.1
Scope: Internal release gate for buyer-facing, public-facing, outreach, packet, and scoping-call materials.

## Purpose

The Claim Gauntlet is an internal review layer for SpecShift materials.

It prevents SpecShift from overstating validation, implying live production proof, disclosing protected method, or collapsing buyer-controlled review into automated judgment.

Every buyer-facing or public-facing claim should pass this checklist before release.

## Global Release Gate

A claim is allowed only if it preserves all four boundaries:

1. Observable-only review.
2. Buyer-retained adjudication.
3. Bounded validation status.
4. No protected method disclosure.

Safe release sentence:

> This claim is allowed only if it preserves observable-only review, buyer-retained adjudication, bounded validation status, and no protected method disclosure.

## Corrected Commercial Status

Use this status language as the default:

> SpecShift is an early-stage observable-only reliability review layer demonstrated in synthetic environments. It presents plausible buyer value, but it has not been validated as live production failure-prediction.

Do not replace this with stronger language unless external validation supports it.

## Core Claim Tests

### 1. Evidence Check

Question:

Does the claim match what has actually been demonstrated?

Allowed:
- Synthetic demonstration.
- Design-layer value.
- Observable-only review concept.
- Candidate-discrepancy memo generation.
- Buyer-controlled pilot framing.

Not allowed:
- Claiming proven live operational value.
- Claiming production failure prediction.
- Claiming externally validated commercial performance without evidence.
- Claiming confirmed detection rates without labeled buyer data.

Safer replacement:

> SpecShift is designed to help reviewers examine observable workflow trajectories for candidate discrepancies under buyer-controlled testing.

---

### 2. Validation Check

Question:

Does the wording imply live production validation when only synthetic, offline, or design-layer evidence exists?

Allowed:
- “Demonstrated in synthetic environments.”
- “Prepared for bounded blind pilot validation.”
- “Plausible buyer value.”
- “Evidence-ready for controlled evaluation.”

Not allowed:
- “Validated in production.”
- “Proven on live systems.”
- “Detects production failures.”
- “Predicts failures before they happen.”

Safer replacement:

> Production value remains unvalidated and should be tested through a bounded blind pilot with buyer-retained labels and pre-registered success criteria.

---

### 3. Authority Check

Question:

Does the claim accidentally make SpecShift sound like the final decision-maker?

Allowed:
- Candidate-discrepancy memo.
- Reviewer aid.
- Buyer-retained adjudication.
- Human review.
- Decision-support layer.

Not allowed:
- Automated final verdict.
- Autonomous compliance judgment.
- SpecShift decides correctness.
- SpecShift certifies a workflow as safe.

Safer replacement:

> SpecShift returns structured candidate-discrepancy memos for buyer-retained human review.

---

### 4. Access Check

Question:

Does the claim imply access to internals or private information?

Allowed:
- Observable traces.
- Exported workflow events.
- Time-ordered visible actions.
- External trajectory review.
- No hidden reasoning required.

Not allowed:
- Model weights.
- Source code.
- Private prompts.
- Hidden activations.
- Private chain-of-thought.
- Internal architecture.
- Proprietary telemetry not supplied by the buyer.

Safer replacement:

> SpecShift reviews exported observable workflow traces and does not require model weights, source code, private prompts, hidden activations, private chain-of-thought, or internal architecture.

---

### 5. Prediction Check

Question:

Does the claim imply guaranteed failure prediction instead of candidate-discrepancy detection?

Allowed:
- Flags potential mismatch.
- Identifies candidate discrepancy.
- Highlights trajectory strain.
- Supports review.
- Tests whether observable workflow behavior aligns with claimed final state.

Not allowed:
- Guarantees prevention.
- Predicts all failures.
- Detects every discrepancy.
- Eliminates audit risk.
- Replaces existing controls.

Safer replacement:

> SpecShift flags candidate discrepancies for reviewer-controlled testing and does not guarantee detection or prevention of all failures.

---

### 6. Procurement Check

Question:

Does the claim clearly distinguish SpecShift from ordinary evals, monitoring, observability, or trace tooling?

Allowed:
- Buyer-controlled observable-only trajectory review.
- Blind audit posture.
- Candidate-discrepancy memo.
- Buyer-retained labels.
- Pre-registered criteria.
- No internals required.

Not allowed:
- Framing SpecShift as just another dashboard.
- Framing it as ordinary observability.
- Framing it as developer-side tracing.
- Framing it as model eval scoring.

Safe distinction:

> The overlap is in the raw material. The category distinction is in the trust architecture.

Expanded distinction:

> Conventional trace, eval, and observability tools often serve developer or operator-side monitoring and debugging workflows. SpecShift is framed as buyer-controlled observable-only trajectory review: exported traces in, candidate-discrepancy memos out, with buyer-retained labels and human adjudication.

---

### 7. Disclosure Check

Question:

Does the claim reveal protected implementation details?

Allowed:
- Public conceptual framing.
- Buyer-safe workflow description.
- Observable-only boundary.
- Pilot protocol.
- Review outputs at a high level.

Not allowed:
- Protected scoring method.
- Internal algorithms.
- Sensitive code.
- Reproducible protected implementation details.
- Private heuristics not intended for first-send materials.

Safer replacement:

> Protected implementation details are intentionally withheld. The proposed evaluation tests the review layer as a standalone applied diagnostic.

---

### 8. Buyer-Control Check

Question:

Does the claim preserve buyer-retained labels, blind review, human adjudication, and pre-registered criteria?

Allowed:
- Buyer retains labels.
- Buyer controls ground truth.
- Criteria are pre-registered.
- Human reviewers adjudicate.
- Ambiguous cases are tracked.

Not allowed:
- SpecShift controls final labels.
- Criteria shift after output review.
- Ambiguous cases are hidden.
- Human review is removed.
- Buyer governance is bypassed.

Safer replacement:

> A valid pilot should use buyer-retained labels, pre-registered success criteria, false-positive and false-negative accounting, ambiguous-case handling, and buyer-retained human adjudication.

---

### 9. Scope Check

Question:

Does the claim keep broader theory outside the applied diagnostic unless explicitly needed?

Allowed:
- Standalone applied diagnostic.
- Observable-only trajectory review.
- Bounded reliability review.
- Pilot-ready evaluation layer.

Not allowed:
- Requiring acceptance of broader theory.
- Making speculative physics, consciousness, or social-system claims part of the buyer case.
- Using theory as proof of commercial function.

Required scope-control sentence:

> This packet evaluates the review layer as a standalone applied diagnostic; broader theoretical context is intentionally outside scope and is not required for the proposed blind audit.

---

### 10. Commercial Check

Question:

Does the claim avoid free-pilot language, code-transfer language, exclusivity creep, or training-rights leakage?

Allowed:
- Paid pilot.
- Narrow evaluation scope.
- Non-exclusive default.
- Buyer-retained labels.
- No code transfer.
- No training rights.
- Limited access to approved artifacts only.

Not allowed:
- Free pilot.
- Open-ended trial.
- Code transfer.
- Training rights.
- Broad exclusivity.
- First-send ZIPs or protected files.
- Attaching protected method documents to cold outreach.

Safer replacement:

> SpecShift pilots should be paid, scoped, non-exclusive by default, and limited to approved buyer-facing materials unless legal and commercial terms are in place.

## Forbidden Claim Patterns

Avoid these patterns:

- “SpecShift proves...”
- “SpecShift guarantees...”
- “SpecShift validates production systems...”
- “SpecShift predicts failures...”
- “SpecShift replaces auditors...”
- “SpecShift certifies correctness...”
- “SpecShift requires access to hidden reasoning...”
- “SpecShift exposes model internals...”
- “SpecShift is just observability...”
- “SpecShift is just evals...”
- “SpecShift has already demonstrated live commercial value...”

## Preferred Claim Patterns

Use these patterns:

- “SpecShift reviews observable workflow trajectories...”
- “SpecShift flags candidate discrepancies...”
- “SpecShift supports buyer-retained human adjudication...”
- “SpecShift does not require model weights, source code, private prompts, hidden activations, private chain-of-thought, or internal architecture...”
- “SpecShift is ready for bounded blind pilot testing...”
- “Production value remains subject to external validation...”
- “The buyer retains labels, ground truth, criteria, and final decision authority...”

## Release Decision

For each claim, choose one:

### Pass

The claim can be used as written.

### Pass with edits

The claim is usable after safer wording is substituted.

### Hold

The claim needs more evidence, legal review, or buyer validation before use.

### Reject

The claim overstates evidence, leaks protected method, misstates authority, or creates commercial/legal risk.

## One-Line Final Gate

Before release, ask:

> Would a skeptical buyer, attorney, evaluator, or technical reviewer read this as stronger than the evidence supports?

If yes, revise.

## Legal / Accounting Threshold

At the stage where contracts, procurement, paid pilots, budget, or money movement becomes real, SpecShift should engage CPA and legal support before committing terms.
