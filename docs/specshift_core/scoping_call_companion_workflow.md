# SpecShift Scoping-Call Companion Workflow

Date created: 2026-06-27
Status: Draft v0.1
Audience: Internal / live-call-safe
Scope: 20-minute buyer scoping call script, fit/no-fit criteria, and follow-up capture discipline.

## Purpose

This workflow keeps early SpecShift buyer calls focused, bounded, and commercially safe.

The call goal is not to sell the full method.

The call goal is to determine whether the buyer has a workflow suitable for a paid, bounded, observable-only trajectory review pilot.

## Core Call Rule

Do not disclose protected implementation details.

Keep the conversation centered on:

- Buyer workflow.
- Observable trace availability.
- Review pain.
- Existing baseline process.
- Pilot fit.
- Buyer-retained labels.
- Pre-registered success criteria.
- Paid, bounded next step.

## 20-Minute Call Structure

### 0:00-2:00 — Opening Boundary

Suggested opening:

> SpecShift is an observable-only trajectory review layer. We do not need model weights, source code, private prompts, hidden activations, private chain-of-thought, or internal architecture. The purpose of this call is to see whether one of your workflows is suitable for a bounded pilot using exported traces, buyer-retained labels, and pre-registered success criteria.

### 2:00-6:00 — Buyer Workflow Selection

Ask:

- Which workflow creates the highest review pain right now?
- Is the issue agent task completion, reconciliation, approval flow, support escalation, incident response, or another multi-step process?
- What final state does the system claim?
- What visible steps lead to that final state?
- Where do errors usually hide?
- What happens when a workflow appears complete but is not actually complete?

### 6:00-10:00 — Observable Trace Check

Ask:

- Do you have exported observable traces for this workflow?
- Are events timestamped?
- Are tool calls, approvals, retries, exceptions, or handoffs visible?
- Is the claimed final state visible?
- Can traces be anonymized or redacted for pilot review?
- Can labels be retained by your team until after SpecShift outputs are submitted?

Fit signal:

- The workflow has visible sequence data.
- The final state or claimed completion marker is visible.
- There are known or suspected discrepancies.
- Buyer can preserve labels separately.

No-fit signal:

- No observable trace exists.
- The only evidence is hidden model state.
- Buyer cannot define the final state.
- Buyer cannot retain or produce labels.
- Buyer wants immediate production certification.

### 10:00-14:00 — Validation Design

Ask:

- How would your team know whether a flagged candidate discrepancy was useful?
- Do you already have known-good and known-bad examples?
- Can you define confirmed discrepancy, confirmed non-discrepancy, ambiguous, out-of-scope, and excluded cases?
- What baseline review process should SpecShift be compared against?
- What would count as useful enough to justify a next step?

Suggested framing:

> A valid pilot should use buyer-retained labels, pre-registered success criteria, false-positive and false-negative accounting, ambiguous-case handling, and buyer-retained human adjudication.

### 14:00-17:00 — Commercial and Scope Boundary

Say:

> If there is a fit, the next step would be a paid, scoped pilot. The default posture is no code transfer, no training rights, no broad exclusivity, no protected method disclosure, and no open-ended free trial.

Ask:

- Who would sponsor a paid pilot?
- Who owns the workflow?
- Who owns the labels?
- Who reviews procurement or vendor approval?
- Is there a security review path?
- What decision would the pilot need to support?

### 17:00-20:00 — Close and Next Step

If fit:

> This sounds potentially pilot-suitable. The next step would be to define the workflow, dataset boundary, label categories, success criteria, baseline, commercial scope, and review timeline.

If no fit:

> This may not be the right first workflow for SpecShift. A better candidate would have exported observable traces, visible claimed final states, buyer-retained labels, and known review pain.

If unclear:

> This may be worth a short follow-up focused only on trace availability, label control, and success criteria.

## Fit / No-Fit Decision

### Strong Fit

A strong pilot candidate has:

- A recurring multi-step workflow.
- Exported observable traces.
- Visible claimed final states.
- Known or suspected review gaps.
- Buyer-controlled labels.
- A human review team or owner.
- A baseline process.
- Willingness to pre-register criteria.
- Budget or path to paid evaluation.

### Medium Fit

A medium pilot candidate has:

- Some trace data.
- Some known review pain.
- Partial labels.
- A plausible workflow owner.
- Unclear baseline or success criteria.

Action:

- Do not overpromise.
- Ask for a narrower workflow.
- Request label/process clarification before proposing pilot terms.

### Poor Fit

A poor pilot candidate has:

- No observable traces.
- No defined workflow.
- No labels.
- No final state.
- No buyer-side reviewer.
- Desire for free consulting.
- Demand for code, protected method, or broad exclusivity.
- Request for production validation claims before pilot evidence.

Action:

- Decline or park.
- Do not disclose more.
- Offer only a safer future-fit description.

## Forbidden Live-Call Moves

Do not:

- Offer a free pilot.
- Send ZIPs on the first call.
- Transfer code.
- Grant training rights.
- Agree to broad exclusivity.
- Claim live production validation.
- Claim guaranteed failure prediction.
- Let the buyer define success after seeing outputs.
- Disclose protected scoring or implementation details.
- Present SpecShift as replacing human reviewers.
- Present the memo as an automated final verdict.

## Required Safe Language

Use:

> SpecShift returns structured candidate-discrepancy memos for buyer-retained human review.

Use:

> Production value should be tested through a bounded blind pilot with buyer-retained labels and pre-registered success criteria.

Use:

> This packet evaluates the review layer as a standalone applied diagnostic; broader theoretical context is intentionally outside scope and is not required for the proposed blind audit.

## Post-Call Capture Template

After the call, capture:

- Company:
- Contact names:
- Contact roles:
- Workflow discussed:
- Buyer pain:
- Observable trace availability:
- Claimed final state:
- Label owner:
- Existing baseline:
- Success criteria candidate:
- False-positive concern:
- False-negative concern:
- Ambiguous-case handling:
- Security/procurement path:
- Budget signal:
- Timeline signal:
- Fit classification:
- Next action:
- Follow-up materials approved:
- Protected method risk:
- Legal/accounting threshold triggered:

## Follow-Up Email Structure

Subject:

> Follow-up: bounded observable-only trajectory review pilot

Body:

> Thank you for the conversation. Based on what we discussed, the potentially suitable pilot area appears to be [workflow]. SpecShift would evaluate exported observable workflow traces and return structured candidate-discrepancy memos for buyer-retained human review.

> A safe pilot would keep labels, ground truth, success criteria, and final adjudication under your control. It would not require model weights, source code, private prompts, hidden activations, private chain-of-thought, or internal architecture.

> The next step would be to confirm the dataset boundary, label categories, pre-registered success criteria, baseline comparison, security requirements, and commercial scope.

> This packet evaluates the review layer as a standalone applied diagnostic; broader theoretical context is intentionally outside scope and is not required for the proposed blind audit.

Close with:

> Best,  
> Benjamin J. Clark  
> Founder, SpecShift Labs LLC

## Legal / Accounting Trigger

If the call includes contracts, procurement, paid pilots, budget, pricing, exclusivity, data rights, code access, security terms, or money movement, pause before committing terms and engage CPA/legal support.

## Repo Companion Script Note

After a live call, run the local call companion workflow if available:

`python3 v0_5/call_companion/specshift_call_companion.py`

Use it to capture notes and generate follow-up drafts.

## Release Gate

Before using this workflow externally, verify it against:

`docs/specshift_core/claim_gauntlet_overclaim_prevention_checklist.md`

Global release gate:

> This claim is allowed only if it preserves observable-only review, buyer-retained adjudication, bounded validation status, and no protected method disclosure.

## Release Status

Draft v0.1 is suitable for internal call preparation.

Do not treat as final legal, procurement, or contract language.
