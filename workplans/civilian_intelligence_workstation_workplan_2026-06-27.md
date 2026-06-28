# Civilian Intelligence Workstation Workplan

Date registered: 2026-06-27
Status: Draft v0.3
Scope: Defensive, lawful, public-source research and audit workstation.

## Naming Boundary

Do not describe this system as literal NSA, CIA, military, covert, classified, or offensive capability.

Preferred name:

Civilian intelligence-grade research and audit workstation.

Purpose:

A hardened research, provenance, and decision-support workstation for fast lawful information intake, source discipline, repo hygiene, evidence review, and SpecShift execution.

## Current Architecture

### Terminal

Role:
- audit gate
- status gate
- commit/push control
- workplan registration
- wiki update pathway
- artifact promotion

Pattern:

pre-audit -> write artifact -> verify -> stage intended files -> diff -> commit -> pull/rebase -> push -> landing check

### Repo

Role:
- operational canon
- buyer-safe language
- claim gates
- workplans
- outreach materials
- research-lane documents

### Wiki

Role:
- memory
- historical notes
- workplan closure
- optional backlog
- non-release context unless promoted into repo

### Orchestra / Fetch_ET

Role:
- evidence and data acquisition
- structured research probes
- global observation reports
- source inventory
- anomaly triage

Known commands:
- orchestra_probe
- orchestra_conduct
- orchestra_signals
- orchestra_board
- radar_run
- radar_status
- radar_open
- orchestra_sources
- orchestra_fetch
- orchestra_global_observation
- fetch_et

### Codex

Role:
- bounded mechanic for code edits
- tests
- repo cleanup
- script writing
- guardrail implementation

Boundary:
Use Codex only where code edits are complex enough to need it. Terminal remains the promotion gate.

## Stage Plan

### Stage 1: Workstation Status

Deliver:
- tools/status/specshift_status.sh
- repo clean/dirty check
- remote sync check
- current workplan check
- artifact count
- wiki update check
- pipeline registry presence check

### Stage 2: Source Registry and Schema

Deliver:
- docs/workstation/minimum_viable_source_registry.md
- docs/workstation/unified_pipeline_data_schema.md
- strict required fields
- source tier definitions
- uncertainty labels
- claim safety gate

### Stage 3: MVP Public Pipelines

Build the minimum viable public-source pipeline set:

1. CISA KEV JSON
2. USGS Earthquake GeoJSON
3. Federal Register API
4. arXiv API
5. NOAA/NWS or NOAA SWPC alerts
6. Hugging Face metadata API
7. SEC EDGAR basic filings
8. World news RSS after live feed verification

### Stage 4: Daily Digest

Deliver:
- terminal markdown digest
- source links
- uncertainty labels
- source health section
- epistemic friction section
- claim safety violations section

### Stage 5: Contradiction and Anomaly Layers

Build last.

Reason:
These are interpretive layers and can manufacture false certainty if built before stable raw intake exists.

## Fastest Useful Build Order

1. specshift_status.sh
2. unified schema and append-only local storage
3. CISA KEV
4. USGS Earthquake feed
5. Federal Register
6. arXiv
7. NOAA/NWS or NOAA SWPC
8. Hugging Face metadata
9. SEC EDGAR
10. World news RSS after feed verification
11. daily digest
12. claim safety gate
13. contradiction detector
14. anomaly detector

## Highest-Value Integrations

1. CISA KEV and NIST NVD
2. AI model and benchmark tracker
3. arXiv / PubMed / Semantic Scholar research tracker
4. Federal Register and SEC EDGAR
5. USGS / NOAA / NASA physical telemetry
6. World news wires and GDELT
7. open-source dependency and advisory feeds
8. infrastructure outage monitor
9. contradiction detector
10. claim-overstatement detector

## Do Not Build Yet

Do not build these until raw-source intake is stable:

- real-time social media sentiment analysis
- individual flight or vessel tracking
- active security scanning
- automated trading or financial advice
- complex predictive forecasting
- low-frequency anomaly detector
- contradiction detector without at least three live source categories
- automated actions based on feed output

## Safety Boundary

Allowed:
- lawful public-source research
- defensive cybersecurity awareness
- source monitoring
- repo audit
- provenance tracking
- buyer-safe outreach support
- uncertainty-preserving reports

Not allowed:
- hacking
- credential theft
- covert surveillance
- targeting individuals
- evading detection
- offensive cyber
- exploit generation
- active probing of distressed infrastructure
- individual aircraft/vessel/person tracking
- weapons support
- classified-claim cosplay
- implying government-grade authorization or access

## Immediate Next Best Action

Build:

tools/status/specshift_status.sh

Then build:

tools/pipelines/pipeline_registry_check.py

No harvesting should begin until source registry and schema validation are in place.
