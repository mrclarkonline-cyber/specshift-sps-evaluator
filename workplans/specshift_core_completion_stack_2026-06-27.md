# SpecShift Core Completion Stack Workplan

Date registered: 2026-06-27

## Purpose

Register the unfinished SpecShift core artifacts that must be completed before revisiting broader lanes.

This workplan prioritizes protection, buyer clarity, pilot readiness, outreach execution, and canon cleanup.

## Completion Stack

### Tier 1: Protection and clarity

#### 12. Claim Gauntlet / Overclaim-Prevention Checklist

Status: Not started  
Priority: Highest  
Reason: Every other artifact should pass through this before release.

Deliverables:
- Internal checklist
- Pass/fail language
- Forbidden claim patterns
- Safer replacement language
- Release gate for outreach, packet, and public-facing docs

Acceptance criteria:
- Prevents claims of live production validation
- Preserves buyer-controlled adjudication
- Preserves observable-only boundary
- Prevents protected method disclosure
- Distinguishes candidate-discrepancy detection from automated judgment

---

#### 15. Buyer-Facing “What SpecShift Is / Is Not” Page

Status: Not started  
Priority: High  
Reason: Buyer clarity before outreach or scoping calls.

Deliverables:
- One-page plain-English explanation
- “SpecShift is” section
- “SpecShift is not” section
- Buyer-safe boundary language
- Procurement-category distinction

Acceptance criteria:
- Explains observable-only trajectory review
- Avoids overclaiming
- Makes buyer control explicit
- Does not disclose protected implementation
- Distinguishes SpecShift from evals, monitoring, observability, and ordinary trace tooling

---

#### 11. ΔΔF Public Explanation Layer

Status: Not started  
Priority: High  
Reason: Needed for public explanation without exposing protected method or drifting into unsupported theory.

Deliverables:
- Plain-English explanation
- Technical but bounded explanation
- Safe analogy set
- “What this does not prove” section
- Relationship to SpecShift stated cautiously

Acceptance criteria:
- Communicates second-order change/stress tracking clearly
- Avoids claiming scientific validation beyond current evidence
- Does not imply production prediction
- Keeps broader theory separate from applied diagnostic claims

---

### Tier 2: Buyer readiness

#### 14. Pilot Acceptance Criteria Finalization

Status: Not started  
Priority: High  
Reason: Paid pilot conversations need clear success criteria.

Deliverables:
- Pre-registered acceptance criteria
- Dataset requirements
- Label requirements
- False-positive / false-negative accounting
- Ambiguous-category handling
- Buyer-retained adjudication statement

Acceptance criteria:
- Works for a bounded blind trajectory review pilot
- Does not require internals, source code, weights, private prompts, or hidden reasoning
- Defines success without implying guaranteed detection
- Supports paid pilot pricing and scope control

---

#### 1. SpecShift Buyer-Safe Viability Packet Refresh

Status: Not started  
Priority: High  
Reason: Main buyer packet must reflect corrected commercial status.

Deliverables:
- Refreshed buyer packet
- Corrected commercial status language
- Claim Gauntlet pass
- Pilot framing
- Boundary page integration
- Scope-control sentence integration

Acceptance criteria:
- States early-stage observable-only reliability review demonstrated in synthetic environments
- States plausible buyer value
- States live production failure-prediction is not validated
- Keeps broader theory outside scope
- Does not disclose protected method

---

#### 9. Scoping-Call Companion Workflow Polish

Status: Not started  
Priority: Medium-high  
Reason: Needed for live buyer calls and follow-up discipline.

Deliverables:
- 20-minute scoping call script
- Opening boundary statement
- Workflow selection prompts
- Fit / no-fit decision criteria
- Follow-up note capture
- Follow-up draft generator check

Acceptance criteria:
- Keeps call focused on buyer workflow and pilot fit
- Avoids free consulting and protected method disclosure
- Routes serious money/procurement moments to CPA/legal threshold
- Produces clean follow-up artifacts

---

### Tier 3: Execution machinery

#### 10. Outreach Wave Execution and Tracking

Status: Not started  
Priority: Medium  
Reason: Outreach needs disciplined tracking after core artifacts are protected.

Deliverables:
- Outreach tracker
- Wave status dashboard
- Contact status fields
- Sent / replied / no-fit / follow-up categories
- No-free-pilot language
- Attachment/path discipline

Acceptance criteria:
- Preserves Proton copy-ready workflow
- Tracks company, contact, role, wave, date, status, and next action
- Uses only approved packet language
- No ZIPs or protected files in first send

---

#### 13. Wiki-to-Repo Canon Cleanup

Status: Not started  
Priority: Medium  
Reason: Prevents memory drift and artifact contradiction.

Deliverables:
- Canon index
- Current claims page
- Deprecated language list
- Protected/private method boundary note
- Repo/wiki reconciliation checklist

Acceptance criteria:
- Current buyer-safe language is easy to find
- Old overclaims are marked deprecated
- Public/private boundaries are explicit
- Workplan artifacts point to canonical sources

---

## Recommended Execution Order

1. Claim Gauntlet / Overclaim-Prevention Checklist
2. Buyer-Facing “What SpecShift Is / Is Not” Page
3. ΔΔF Public Explanation Layer
4. Pilot Acceptance Criteria Finalization
5. SpecShift Buyer-Safe Viability Packet Refresh
6. Scoping-Call Companion Workflow Polish
7. Outreach Wave Execution and Tracking
8. Wiki-to-Repo Canon Cleanup

## Global Release Gate

No buyer-facing or public-facing artifact should be treated as ready unless it passes this sentence:

> This claim is allowed only if it preserves observable-only review, buyer-retained adjudication, bounded validation status, and no protected method disclosure.

## Notes

- Do not offer free pilots.
- Do not transfer code.
- Do not grant training rights.
- Do not imply production validation.
- Do not imply automated final judgment.
- Do not disclose protected method.
- Do not collapse SpecShift into ordinary evals, monitoring, observability, or trace tooling.
- At the stage where contracts, procurement, paid pilots, budget, or money movement becomes real, engage CPA/legal support.

