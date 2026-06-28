# SpecShift Buyer Trigger Watch

Date created: 2026-06-27
Status: Draft v0.1
Scope: Buyer-relevance synthesis from local public-source digests.

## Tool

tools/pipelines/specshift_buyer_trigger_watch.py

## Dry-run

python3 tools/pipelines/specshift_buyer_trigger_watch.py --dry-run

## Generate

python3 tools/pipelines/specshift_buyer_trigger_watch.py

## Purpose

This tool scans local generated digests for buyer-trigger terms related to agent reliability, workflow automation, audit, governance, handoff, reconciliation, settlement, and observable trace review.

## Safety Boundary

Allowed:

- buyer-trigger triage
- role hypothesis
- workflow-fit hypothesis
- cautious outreach preparation
- source-linked review

Not allowed:

- claiming buyer has a problem
- claiming production validation
- claiming causation
- claiming hidden internals
- using incidents exploitatively
- protected method disclosure

## Safe Sentence

SpecShift can review observable workflow traces and return candidate-discrepancy memos for human adjudication without requiring model internals, private prompts, weights, or hidden chain-of-thought.
