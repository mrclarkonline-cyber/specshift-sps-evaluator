# SpecShift Wiki-to-Repo Canon Cleanup

Date created: 2026-06-27
Status: Draft v0.1
Audience: Internal / canon-control-safe
Scope: Prevent memory drift, stale claims, conflicting packet language, and public/private boundary confusion.

## Purpose

This document defines how SpecShift should keep wiki notes, memory scrapes, repo documents, outreach materials, and buyer-facing language aligned.

The goal is to make the repo the current operational canon while preserving the wiki as historical and exploratory memory.

## Core Rule

The repo controls release-ready language.

The wiki may contain exploration, old drafts, broader theory, jokes, speculative material, and deprecated framing.

Do not treat a wiki scrape as buyer-facing canon unless it has been promoted into the repo and passed the Claim Gauntlet.

## Current Canon Sources

The current SpecShift core canon is:

- `workplans/specshift_core_completion_stack_2026-06-27.md`
- `docs/specshift_core/claim_gauntlet_overclaim_prevention_checklist.md`
- `docs/specshift_core/what_specshift_is_and_is_not.md`
- `docs/specshift_core/ddf_public_explanation_layer.md`
- `docs/specshift_core/pilot_acceptance_criteria.md`
- `docs/specshift_core/buyer_safe_viability_packet_refresh.md`
- `docs/specshift_core/scoping_call_companion_workflow.md`
- `docs/specshift_core/outreach_wave_execution_and_tracking.md`
- `docs/specshift_core/wiki_to_repo_canon_cleanup.md`

## Current Default Commercial Status

Use this status language as the default:

> SpecShift is an early-stage observable-only reliability review layer demonstrated in synthetic environments. It presents plausible buyer value, but it has not been validated as live production failure-prediction.

Do not use stronger language unless external validation supports it.

## Current Default One-Sentence Summary

Use this as the default buyer-safe summary:

> SpecShift is a buyer-controlled, observable-only trajectory review layer that examines exported workflow traces and returns structured candidate-discrepancy memos for buyer-retained human review.

## Current Default Scope-Control Sentence

Use this sentence where appropriate:

> This packet evaluates the review layer as a standalone applied diagnostic; broader theoretical context is intentionally outside scope and is not required for the proposed blind audit.

## Current Global Release Gate

Every buyer-facing or public-facing claim should pass this gate:

> This claim is allowed only if it preserves observable-only review, buyer-retained adjudication, bounded validation status, and no protected method disclosure.

## Repo vs Wiki Authority

### Repo

Use the repo for:

- Release-ready language.
- Buyer-safe language.
- Pilot criteria.
- Outreach operations.
- Call scripts.
- Current commercial posture.
- Protected/public boundary statements.
- Canonical claim constraints.

### Wiki

Use the wiki for:

- Conversation memory.
- Exploratory notes.
- Broader theory.
- Historical drafts.
- Humor and scene scaffolding.
- Deprecated language.
- Raw idea capture.
- Non-release material.

## Promotion Rule

A wiki note becomes canon only after it is:

1. Reviewed.
2. Reduced to buyer-safe or internal-safe language.
3. Checked against the Claim Gauntlet.
4. Added to the repo.
5. Committed.
6. Optionally pushed to remote.

Until then, it is memory, not canon.

## Deprecated Language List

Mark these as deprecated unless future evidence supports them:

- “SpecShift proves...”
- “SpecShift guarantees...”
- “SpecShift validates production systems...”
- “SpecShift predicts failures...”
- “SpecShift replaces auditors...”
- “SpecShift certifies correctness...”
- “SpecShift has live production validation...”
- “SpecShift detects every discrepancy...”
- “SpecShift eliminates audit risk...”
- “ΔΔF proves hidden structure...”
- “ΔΔF validates SpecShift...”
- “The method is proven commercially...”

## Preferred Replacement Language

Use:

- “SpecShift reviews observable workflow trajectories...”
- “SpecShift flags candidate discrepancies...”
- “SpecShift returns structured candidate-discrepancy memos for buyer-retained human review...”
- “SpecShift is ready for bounded blind pilot testing...”
- “Production value remains subject to external validation...”
- “The buyer retains labels, ground truth, criteria, and final decision authority...”
- “ΔΔF highlights second-order change in observable trajectories...”
- “ΔΔF is explanatory intuition, not commercial proof...”

## Public / Private Boundary

### Public-Safe

Public-safe materials may include:

- Observable-only category framing.
- Buyer-controlled review framing.
- Candidate-discrepancy memo outputs.
- Corrected commercial status.
- Pilot acceptance criteria.
- Non-requirement of hidden internals.
- Scope-control sentence.
- General ΔΔF explanation.

### Private / Protected

Do not place in public or first-send materials:

- Protected scoring method.
- Source code.
- Sensitive algorithms.
- Reproducible implementation details.
- Internal heuristics.
- Private method notes.
- Protected data-room material.
- Broad provenance bundles unless specifically appropriate.

## Cleanup Workflow

When a new wiki scrape appears:

1. Leave it untracked until reviewed.
2. Inspect for useful canon updates.
3. Extract only stable, buyer-safe or internal-operational items.
4. Add extracted material to appropriate repo files.
5. Mark speculative or deprecated material as non-canon.
6. Commit only the cleaned repo artifact.
7. Do not commit raw wiki scrape unless intentionally archiving memory.

## Current Untracked Wiki Scrape Handling

The current untracked scrape:

`memory_layer/wiki/operator_memory/current-conversation-strategic-scrape-2026-06-27.md`

should remain untracked unless there is a deliberate decision to archive raw memory.

Preferred action:

- Do not add it casually.
- Review it only when extracting canon.
- Promote cleaned items into repo docs.
- Leave raw scrape local unless archiving is explicitly desired.

## Canon Review Checklist

Before release, check:

- Does this claim match the corrected commercial status?
- Does it preserve buyer-retained adjudication?
- Does it preserve observable-only review?
- Does it avoid protected method disclosure?
- Does it avoid production validation overclaiming?
- Does it avoid automatic final judgment language?
- Does it distinguish SpecShift from ordinary evals, monitoring, and observability?
- Does it keep broader theory outside buyer proof?
- Does it preserve no code transfer, no training rights, no free pilot, and non-exclusive default?

## Legal / Accounting Trigger

If canon updates affect contracts, procurement, paid pilots, budget, pricing, exclusivity, data rights, code access, security terms, or money movement, pause before committing external terms and engage CPA/legal support.

## Release Status

Draft v0.1 is suitable for internal canon management.

The repo should be treated as the active source of current operational truth.
