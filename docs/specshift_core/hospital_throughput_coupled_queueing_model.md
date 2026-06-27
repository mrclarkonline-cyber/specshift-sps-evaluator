# Hospital Throughput / Coupled Queueing Model

Date created: 2026-06-27
Status: Draft v0.1
Audience: Internal / operations-research-safe
Scope: Hospital throughput as an observable coordination and queueing problem, not a clinical decision system.

## One-Sentence Summary

This lane explores hospital throughput as a coupled queueing and coordination problem where observable workflow traces may reveal bottlenecks, handoff strain, and system-level delay patterns.

## Purpose

The hospital throughput lane examines whether SpecShift-style trajectory review can help identify candidate operational discrepancies in complex hospital workflows.

This is an operations and coordination-support lane.

It is not a medical diagnosis, treatment, triage, or clinical decision-making system.

## Corrected Status

This lane is exploratory.

It has not been validated in hospital operations.

It does not claim improved patient outcomes, clinical safety, staffing optimization, or regulatory compliance.

Any future claim would require domain expert review, hospital-controlled data, privacy compliance, and prospective or retrospective validation.

## Core Framing

Hospital throughput can be viewed as a coupled queueing network.

A delay in one queue can propagate into others.

A handoff failure in one unit can appear as congestion somewhere else.

A final metric, such as average wait time or bed occupancy, may hide the visible trajectory of how the system became strained.

The review question is:

> Given observable workflow traces, does the visible operational trajectory support the claimed state of throughput, capacity, or bottleneck location?

## Candidate Hospital Workflows

Potential workflows include:

- Emergency department intake-to-disposition.
- Bed assignment and transfer.
- Discharge readiness.
- Imaging order-to-result flow.
- Lab order-to-result flow.
- Consult request-to-completion.
- Operating room turnover.
- Inpatient transfer workflow.
- Transport queue.
- Environmental services room turnover.
- Medication delivery workflow.
- Case management discharge planning.

Each pilot should be scoped to one bounded operational workflow.

## Observable Trace Inputs

Potential trace inputs may include:

- Timestamped workflow events.
- Queue entry and exit times.
- Handoff events.
- Order placement and completion times.
- Bed request and assignment times.
- Discharge milestone timestamps.
- Transport request and completion times.
- Room cleaning request and completion times.
- Consult request and completion times.
- Status transitions.
- Escalation events.
- Exception or delay reason codes.

The pilot should use only approved, de-identified or appropriately governed data.

## What This Lane Could Return

A future review output may identify candidate operational discrepancies such as:

- Claimed bottleneck unsupported by visible queue trajectory.
- Downstream congestion caused by upstream handoff delay.
- Apparent completion marker inconsistent with unresolved workflow step.
- Repeated queue cycling.
- Delay propagation across coupled queues.
- Handoff discontinuity.
- Capacity strain appearing before visible failure.
- Ambiguous cases requiring operations expert review.

The output should be treated as a candidate operations memo, not a clinical verdict.

## What This Lane Does Not Claim

This lane does not claim:

- Medical diagnosis.
- Treatment recommendation.
- Patient triage authority.
- Clinical risk scoring.
- Replacement of clinicians.
- Replacement of hospital operations leaders.
- Regulatory compliance certification.
- Proven patient outcome improvement.
- Production-validated hospital deployment.
- Staffing instruction.
- Guaranteed bottleneck detection.

## Coupled Queueing Concept

A hospital is not one line.

It is a network of interacting queues.

Examples:

- Emergency department wait depends on inpatient bed availability.
- Inpatient bed availability depends on discharge readiness.
- Discharge readiness may depend on labs, imaging, consults, transport, and case management.
- Imaging delays may affect ED disposition and inpatient flow.
- Environmental services room turnover affects bed assignment.
- Bed assignment affects ED boarding.

The value of trajectory review is to inspect how delay moves through the network.

## Safe ΔΔF Relationship

ΔΔF may be used as a public intuition for second-order change in throughput behavior.

Safe version:

> F(t) shows visible throughput behavior. ΔF shows how that behavior changes. ΔΔF may highlight stress, acceleration, or transition pressure in the change pattern.

Do not claim that ΔΔF proves cause.

Do not claim that ΔΔF alone identifies the true bottleneck.

## Pilot Design

A safe hospital operations pilot should include:

1. One bounded operational workflow.
2. Hospital-approved observable traces.
3. De-identification or appropriate governance.
4. Hospital-retained labels.
5. Hospital-controlled ground truth or adjudication.
6. Pre-registered success criteria.
7. False-positive accounting.
8. False-negative accounting.
9. Ambiguous-case handling.
10. Baseline comparison where available.
11. Human operations review.
12. No clinical decision authority.
13. No protected method disclosure.
14. No claim of patient-specific recommendation.

## Label Categories

Preferred label categories:

- Confirmed operational discrepancy.
- Confirmed non-discrepancy.
- Ambiguous or insufficient evidence.
- Out of scope.
- Excluded from scoring.

Optional hospital-operations sublabels:

- Handoff delay.
- Queue cycling.
- Upstream bottleneck.
- Downstream bottleneck.
- Unsupported completion.
- Delay propagation.
- Missing milestone.
- Status mismatch.
- Capacity strain.
- Data-quality issue.

## Pre-Registered Success Criteria

A pilot may evaluate:

- Precision of candidate discrepancy flags.
- Recall against hospital-labeled operational discrepancies.
- False-positive rate.
- False-negative rate.
- Operations reviewer usefulness.
- Ability to surface overlooked bottleneck patterns.
- Time saved in review.
- Quality of trajectory-grounded explanation.
- Comparison against existing throughput dashboard or manual review.

Do not define success after seeing outputs.

## Minimum Acceptance Template

> The pilot is successful if the review process produces candidate operational-discrepancy memos that meet pre-registered usefulness and error-accounting thresholds on hospital-retained labels, without making clinical decisions, requiring protected internals, or replacing human operations review.

## Data and Privacy Boundary

Hospital data can be sensitive.

Any pilot must address:

- Patient privacy.
- De-identification.
- Minimum necessary data.
- Data retention.
- Access control.
- Security review.
- Institutional approval.
- Applicable law and policy.
- Human oversight.

Do not casually move patient-level data into external systems.

## Baseline Comparison

Where available, compare against:

- Existing throughput dashboard.
- Current operations review.
- Manual case review.
- Existing queueing or process-mining tool.
- Existing command-center workflow.
- Null baseline.

Use the same scoped dataset and hospital-retained labels where possible.

## Commercial / Professional Boundary

Any hospital-facing work should involve appropriate legal, privacy, security, and domain review before external commitments.

If money, procurement, contracts, data rights, security review, patient data, or hospital operations access becomes real, engage CPA/legal and qualified healthcare operations/privacy expertise.

## Forbidden Claims

Do not claim:

- “SpecShift improves patient outcomes.”
- “SpecShift identifies the correct clinical decision.”
- “SpecShift triages patients.”
- “SpecShift replaces hospital staff.”
- “SpecShift guarantees throughput improvement.”
- “SpecShift is clinically validated.”
- “SpecShift is HIPAA-ready” unless formally established.
- “SpecShift detects all bottlenecks.”
- “SpecShift proves the root cause.”

## Preferred Claims

Use:

- “This is an operations-research lane.”
- “This reviews observable workflow trajectories.”
- “This may identify candidate operational discrepancies for human review.”
- “This does not make clinical decisions.”
- “This requires hospital-controlled validation.”
- “This is exploratory until tested with governed data and domain reviewers.”

## Relationship to Core SpecShift Documents

This lane should remain consistent with:

- `docs/specshift_core/claim_gauntlet_overclaim_prevention_checklist.md`
- `docs/specshift_core/ddf_public_explanation_layer.md`
- `docs/specshift_core/pilot_acceptance_criteria.md`
- `docs/specshift_core/wiki_to_repo_canon_cleanup.md`

## Global Release Gate

> This claim is allowed only if it preserves observable-only review, buyer-retained adjudication, bounded validation status, and no protected method disclosure.

## Release Status

Draft v0.1 is suitable for internal operations-research planning.

Do not treat as clinical, legal, privacy, procurement, or deployment-ready language.
