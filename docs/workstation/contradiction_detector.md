# Multi-Source Contradiction Detector

Date created: 2026-06-27
Status: Draft v0.1
Scope: Local epistemic-friction detection across generated source digests.

## Tool

tools/pipelines/contradiction_detector.py

## Dry-run

python3 tools/pipelines/contradiction_detector.py --dry-run

## Generate

python3 tools/pipelines/contradiction_detector.py

## Purpose

This tool scans local generated markdown digests and flags possible unresolved variance across sources.

It is not a truth engine.

It does not pick a winner.

It does not label disagreement as misinformation.

## Safety Boundary

Allowed:

- flag unresolved variance
- flag source-tier differences
- flag uncertainty-label differences
- flag numeric variance
- support human review

Not allowed:

- declaring one source true
- declaring one source false
- inferring intent
- inferring cause
- claiming concealment
- claiming fraud
- labeling disagreement as misinformation by default
- promoting unresolved variance to validated conclusion

## Required Interpretive Warning

This output flags unresolved variance or anomaly for review; it does not establish cause, intent, origin, or validated conclusion.

## Next Step

After this tool is committed, the next workplan item is:

tools/pipelines/claim_overstatement_detector.py

Reason:

Claim-overstatement detection checks whether generated summaries or headlines assert more certainty than their own source support allows.
