# Workstation Pipeline Execution Workplan

Date registered: 2026-06-27
Status: Draft v0.1
Scope: Execute the civilian intelligence workstation pipeline plan safely.

## Purpose

This workplan turns the AI-recommended pipeline registry into a practical execution sequence.

The goal is not to pull everything at once.

The goal is to build the workstation in a safe order:

1. status visibility
2. source registry validation
3. schema discipline
4. Tier 1 public-source intake
5. daily digest
6. claim safety gate
7. SpecShift-specific synthesis
8. contradiction and anomaly layers last

## Execution Principle

Raw intake first.

Interpretation second.

Contradiction and anomaly engines last.

No automated action from pipeline outputs.

No offensive cyber.

No individual tracking.

No trading signals.

No protected method disclosure.

## Stage 1: Workstation Status Command

Deliver:

tools/status/specshift_status.sh

Purpose:
One command reports repo, wiki, artifact, pipeline, and environment readiness.

Must show:

- git branch
- git clean/dirty state
- remote sync status
- latest commits
- workstation docs present/missing
- pipeline registry present/missing
- core artifact count
- finance outreach files present/missing
- Python version
- recommended command availability
- next recommended action

Acceptance criteria:

- runs without network dependency
- does not mutate repo
- exits 0
- readable in Terminal
- no secrets displayed

## Stage 2: Pipeline Registry Check

Deliver:

tools/pipelines/pipeline_registry_check.py

Purpose:
Validate that the minimum viable source registry exists and contains the required source sections before any source harvesting begins.

Must check:

- docs/workstation/minimum_viable_source_registry.md exists
- required MVP sources are present
- each source has tier/category/access/key/format/cadence/guardrails/status fields
- missing fields are reported clearly
- exits nonzero if required registry items are missing

Required MVP source IDs:

- cisa_kev
- usgs_earthquake
- federal_register
- arxiv
- noaa_alerts
- huggingface_metadata
- sec_edgar
- bbc_world_rss
- reuters_ap_rss

Acceptance criteria:

- registry check runs locally
- no network call
- no credentials required
- missing items are visible
- can be called by future status command

## Stage 3: Source Health Monitor

Deliver later:

tools/pipelines/source_health_check.py

Purpose:
Track source availability, last successful fetch, failure count, format validity, and status.

Fields:

- last_successful_fetch
- last_failure
- failure_count
- format_valid
- rate_limited
- status: healthy | degraded | failing | disabled

## Stage 4: First Tier 1 Intake

Build only after Stage 1 and Stage 2 pass.

First sources:

1. CISA KEV JSON
2. USGS Earthquake GeoJSON
3. Federal Register API
4. arXiv API
5. NOAA/NWS or NOAA SWPC alerts
6. Hugging Face metadata only
7. SEC EDGAR basic filings

Rules:

- no model downloads
- no package execution
- no active probing
- no private tracking
- no trading/investment advice
- no legal advice
- no medical advice

## Stage 5: Daily Digest

Deliver later:

tools/pipelines/daily_digest.py

Output folder:

reports/fast_relevance/YYYY-MM-DD/

Sections:

1. Executive Summary
2. Critical Security
3. AI / Technical Releases
4. Research Literature
5. Policy and Regulatory
6. Financial / Corporate Filings
7. Earth / Space / Infrastructure
8. SpecShift Buyer Triggers
9. Epistemic Friction
10. Pipeline Health

## Stage 6: Claim Safety Gate

Deliver later:

tools/pipelines/claim_safety_gate.py

Rules:

- every item must have source_url and retrieved_at
- unsupported claims remain observation/hypothesis
- preprints are labeled preprint
- model cards are labeled self-reported claims
- no validated conclusion without Tier 1/Tier 2 corroboration or authoritative confirmation
- transition to validated_conclusion must be logged

## Stage 7: SpecShift Synthesis

Deliver later:

- SpecShift Buyer Trigger Watch
- Finance Integrity Watch
- AI Agent Reliability Watch
- AI-for-Science Watch
- Materials Watch

Rules:

- synthesis uses raw records
- no protected method disclosure
- no production validation claims
- no buyer overclaiming

## Stage 8: Interpretive Layers, Build Last

Deliver last:

- Multi-Source Contradiction Detector
- Claim-Overstatement Detector
- Low-Frequency High-Impact Anomaly Detector

Rules:

- contradiction detector does not pick a winner
- overstatement detector checks language only
- anomaly detector requires explicit baseline and null hypothesis
- no automated actions
- human review required

## Immediate Execution

Proceed now with:

1. tools/status/specshift_status.sh
2. tools/pipelines/pipeline_registry_check.py
3. tools/pipelines/README.md

Then commit and push.
