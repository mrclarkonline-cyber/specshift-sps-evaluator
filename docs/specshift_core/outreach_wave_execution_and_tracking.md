# SpecShift Outreach Wave Execution and Tracking

Date created: 2026-06-27
Status: Draft v0.1
Audience: Internal / outreach-ops-safe
Scope: Outreach execution rules, tracker fields, wave discipline, and follow-up categories.

## Purpose

This document keeps SpecShift outreach disciplined, buyer-safe, and traceable.

The goal is to prevent scattered outreach, inconsistent claims, untracked follow-ups, free-pilot leakage, protected method disclosure, or attachment mistakes.

## Core Outreach Rule

Do not send protected method materials in first-contact outreach.

First sends should be plain-text or approved buyer-safe material only.

No ZIPs, source files, internal scoring details, private implementation notes, or protected packet paths should be sent unless legal and commercial terms justify disclosure.

## Current Outreach Status

Use this as the default outreach status posture:

> SpecShift is an early-stage observable-only reliability review layer demonstrated in synthetic environments. It presents plausible buyer value, but it has not been validated as live production failure-prediction.

## Approved One-Sentence Summary

> SpecShift is a buyer-controlled, observable-only trajectory review layer that examines exported workflow traces and returns structured candidate-discrepancy memos for buyer-retained human review.

## Approved First-Send Summary

> I am reaching out about SpecShift, a buyer-controlled observable-only trajectory review layer for reviewing exported workflow traces. It returns structured candidate-discrepancy memos for human review and does not require model weights, source code, private prompts, hidden activations, private chain-of-thought, or internal architecture. The current status is early-stage and pilot-ready: demonstrated in synthetic environments, with production value to be tested through a bounded blind pilot using buyer-retained labels and pre-registered success criteria.

## Scope-Control Sentence

Use this sentence where appropriate:

> This packet evaluates the review layer as a standalone applied diagnostic; broader theoretical context is intentionally outside scope and is not required for the proposed blind audit.

## Outreach Wave Tracker Fields

Track each outreach row with these fields:

- Wave
- Company
- Contact name
- Contact role
- Contact email or channel
- Source of contact
- Target category
- Workflow hypothesis
- Pain hypothesis
- Date prepared
- Date sent
- Material sent
- Attachment sent
- Claim language version
- Status
- Reply date
- Reply category
- Follow-up due date
- Next action
- Buyer fit rating
- Protected method risk
- Legal/accounting trigger
- Notes

## Status Values

Use these status values:

- Not prepared
- Prepared
- Sent
- Replied
- Follow-up needed
- Follow-up sent
- Meeting scheduled
- Parked
- No fit
- Declined
- Converted to scoping call
- Converted to paid pilot discussion
- Do not contact

## Reply Categories

Classify replies as:

- Positive interest
- Needs clarification
- Referral
- Procurement path
- Technical review request
- Security review request
- Price / budget question
- Request for materials
- Request for protected method
- Free pilot request
- Exclusivity request
- No fit
- No response
- Unsubscribe / do not contact

## Wave Discipline

### Wave 0 — Hygiene

Purpose:

- Verify contacts.
- Remove duplicates.
- Remove bad-fit companies.
- Remove risky recipients.
- Confirm role relevance.

Do not send broad claims from this wave.

### Wave 1 — Precision Pilot Seekers

Purpose:

- Contact highest-fit companies where observable workflow trace review may solve an urgent problem.

Typical fit:

- AI agent companies.
- Workflow automation companies.
- Financial operations platforms.
- Incident response or support workflow platforms.
- Teams with recurring multi-step workflow risk.

### Wave 2 — Finance / Devtools Expansion

Purpose:

- Expand to finance integrity, reconciliation, devtools, infrastructure, and workflow review targets.

Typical fit:

- Payments.
- Reconciliation.
- Ledger operations.
- Agent infrastructure.
- Developer tools.
- Observability-adjacent buyers with buyer-side audit needs.

### Wave 3 — Support / Procurement / Incident

Purpose:

- Test support escalation, procurement workflow, incident response, and approval-flow use cases.

Typical fit:

- Multi-step visible workflows.
- Known completion gaps.
- Human review burden.
- Existing trace data.

### Wave 4 — Validators / Category Shapers

Purpose:

- Approach expert reviewers, category validators, or strategically relevant advisors.

Do not give away protected method.

Use category language and bounded pilot framing.

## Attachment Discipline

First send:

- Prefer no attachment.
- If attachment is necessary, use only approved buyer-safe PDF or plain-text material.
- Do not attach ZIPs.
- Do not attach source code.
- Do not attach protected method documents.
- Do not attach internal workplans.
- Do not attach hash/path/provenance bundles unless specifically appropriate and approved.

Approved first-send materials should be derived from:

- `docs/specshift_core/what_specshift_is_and_is_not.md`
- `docs/specshift_core/buyer_safe_viability_packet_refresh.md`
- `docs/specshift_core/pilot_acceptance_criteria.md`

## No-Free-Pilot Rule

Do not offer a free pilot.

Use:

> The appropriate next step would be a paid, scoped pilot with buyer-retained labels, pre-registered success criteria, no code transfer, no training rights, and no protected method disclosure.

If asked for free evaluation:

> I am not offering free pilots. A small paid pilot is the right structure because the work requires scoped data handling, success criteria, review time, and commercial boundary discipline.

## Protected Method Request Response

If a buyer asks for method details too early:

> I can describe the review structure, pilot boundary, input/output expectations, and validation design. Protected implementation details are not part of first-contact materials and would require appropriate commercial and legal terms before disclosure.

## Exclusivity Request Response

If a buyer asks for exclusivity too early:

> The default posture is non-exclusive. Any exclusivity would need to be narrow, time-bounded, commercially justified, and reviewed with counsel.

## Code Transfer Request Response

If a buyer asks for code:

> Code transfer is not part of the pilot structure. The proposed pilot evaluates the review layer through exported observable traces and returned candidate-discrepancy memos.

## Training Rights Request Response

If a buyer asks to use materials for model training:

> Training rights are not included. Pilot materials and outputs should be limited to the agreed evaluation purpose.

## Follow-Up Timing

Default follow-up cadence:

- First follow-up: 3-5 business days after first send.
- Second follow-up: 7-10 business days after first follow-up.
- Park after second follow-up unless there is clear signal.

Do not spam.

Do not chase after unsubscribe or do-not-contact signals.

## Follow-Up Template

Subject:

> Re: observable-only trajectory review pilot

Body:

> Following up briefly on SpecShift. The narrow question is whether one of your workflows has exported observable traces where a bounded review could test candidate-discrepancy memos against your retained labels and pre-registered success criteria.

> SpecShift does not require model weights, source code, private prompts, hidden activations, private chain-of-thought, or internal architecture.

> If there is a suitable workflow, the next step would be a short scoping call to determine pilot fit.

Close:

> Best,  
> Benjamin J. Clark  
> Founder, SpecShift Labs LLC

## Meeting Conversion Rule

Convert a reply into a scoping call only when there is evidence of:

- A real workflow.
- Observable traces.
- Review pain.
- Label ownership or path to labels.
- Human reviewer or business owner.
- Possible budget or sponsor.
- Buyer willingness to define success criteria.

If those are missing, ask one narrowing question before scheduling.

## Legal / Accounting Trigger

If a contact raises contracts, procurement, paid pilots, budget, pricing, exclusivity, data rights, code access, security terms, or money movement, pause before committing terms and engage CPA/legal support.

## Claim Gauntlet Requirement

Before sending any outreach copy, check it against:

`docs/specshift_core/claim_gauntlet_overclaim_prevention_checklist.md`

Global release gate:

> This claim is allowed only if it preserves observable-only review, buyer-retained adjudication, bounded validation status, and no protected method disclosure.

## Release Status

Draft v0.1 is suitable for internal outreach operations.

Do not treat as final legal, procurement, or contract language.
