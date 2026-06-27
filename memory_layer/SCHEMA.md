# SpecShift Operational Memory Layer Schema

## Layers

1. raw/
Immutable source material. Do not rewrite.

2. wiki/
AI-maintained synthesis pages. May be updated when new evidence arrives.

3. wiki/core/
Protected-core index and claim-boundary references only. Do not disclose method internals.

4. logs/
Activity logs, update notes, ingestion records, contradiction checks, and promotion decisions.

## Required Page Fields

Each wiki page should include:

- Status:
- Source(s):
- Last updated:
- Public-safe:
- Private-safe:
- Counsel-only:
- Core-protected:
- Confidence:
- Contradictions:
- Promotion status:

## Non-Negotiable Rules

The AI may maintain synthesis.
The AI may not mutate protected claims, pricing posture, licensing boundaries, or core method without explicit promotion.
Raw evidence is never rewritten.
Public-facing claims must remain bounded and defensible.

## Claim Lifecycle

No claim should skip stages without explicit approval.

1. Inbox
   Raw candidate idea or incoming signal. Not yet operational knowledge.

2. Observed
   Source-backed observation captured from raw evidence.

3. Synthesized
   Integrated into wiki context with source links and confidence notes.

4. Operational
   Useful for outreach, buyer strategy, product framing, or workflow decisions.

5. Validated
   Supported by reproducible evidence, pilot result, external confirmation, or repeated trace.

6. Public-safe
   Approved for external language without exposing protected method internals.

## Promotion Rules

Inbox items may become wiki pages only through explicit promotion.

Each promotion record must include:
- source item
- promoted page
- reason for promotion
- claim lifecycle stage
- public-safety status
- protected-core risk
- date
- reviewer

## Archive Rules

Do not delete superseded claims, retired hypotheses, or old outreach logic.
Move them to archive with a short reason and replacement pointer when applicable.
