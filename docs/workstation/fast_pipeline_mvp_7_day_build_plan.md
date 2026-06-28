# Fast Pipeline MVP 7-Day Build Plan

Date created: 2026-06-27
Status: Draft v0.1
Scope: Conservative seven-day build path for public-source workstation pipelines.

## Day 1: Infrastructure and Schema

Tasks:
- create unified schema
- create source registry
- create append-only local output folders
- create source health fields
- create basic JSON/Markdown output pattern
- create registry validation script

Goal:
No source fetching without schema and registry validation.

## Day 2: CISA KEV and USGS

Tasks:
- integrate CISA KEV JSON
- integrate USGS Earthquake GeoJSON
- store raw payload hash
- produce first two markdown summaries
- add source health check

Goal:
Two Tier 1 sources working with provenance.

## Day 3: Federal Register and arXiv

Tasks:
- integrate Federal Register API
- integrate arXiv API
- tag proposed/final rule
- tag preprint status
- generate policy and research digest sections

Goal:
Policy and research pipelines working.

## Day 4: NOAA and Hugging Face

Tasks:
- integrate NOAA/NWS or NOAA SWPC feed
- integrate Hugging Face model metadata only
- block any model download/execution behavior
- mark benchmark/model-card claims as unverified

Goal:
Earth/space/weather and AI model metadata working safely.

## Day 5: SEC EDGAR and News RSS Verification

Tasks:
- integrate SEC EDGAR basic filing search
- verify current BBC/Reuters/AP RSS options
- add only live, permitted feeds
- label wire reports as observation/preliminary until corroborated

Goal:
Corporate filings and verified news intake.

## Day 6: Digest Generator

Tasks:
- build markdown daily digest
- sections by category
- include top items only
- include pipeline health
- include uncertainty labels
- include source links

Goal:
Useful terminal-readable daily report.

## Day 7: Claim Safety Gate and Alert Rules

Tasks:
- add claim safety gate middleware
- enforce source_url and retrieved_at
- block unverified claims from validated language
- add Tier 1-only breaking alert rules
- test end-to-end with one 24-hour sample

Goal:
Safe first operational loop.

## Week-One Breaking Alerts Only

Allow:
- new CISA KEV item
- USGS earthquake above threshold
- NOAA/NWS severe alert
- NOAA SWPC severe alert
- official agency emergency notice

Delay:
- wire-service breaking alerts
- GDELT alerts
- social spikes
- anomaly flags

## Week-One Minimum Schema

Required:
- item_id
- pipeline
- source_name
- source_url
- retrieved_at
- published_at
- title
- summary
- confidence
- uncertainty_label
- claim_safety_notes

## Week-One Output Folder

Use:

reports/fast_relevance/YYYY-MM-DD/

Files:
- source_health.md
- cybersecurity.md
- earth_hazards.md
- policy.md
- research.md
- ai_models.md
- finance_filings.md
- news.md
- daily_digest.md
