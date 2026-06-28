# Orchestra Full Implementation Workplan

Date registered: 2026-06-27
Status: Active audit/remediation workplan
Scope: Make Orchestra / Fetch_ET fully verifiable inside the workstation.

## Definition of Done

Orchestra is fully implemented when:

- all expected command wrappers are discoverable
- each wrapper has a safe help/status mode
- core paths exist
- source registry exists and parses
- global observation categories are represented
- source health can be audited
- live fetches remain explicit human-triggered actions
- no tool performs active probing or targeting by default
- status output clearly reports gaps
- wiki_landing shows clean status after repo-side integration

## Phase 1: Repo-Side Audit Integration

Deliver:

- tools/orchestra/orchestra_audit.py
- tools/status/orchestra_status.sh
- docs/workstation/orchestra_implementation_status.md
- docs/workstation/orchestra_implementation_audit_latest.md
- docs/workstation/orchestra_implementation_audit_latest.json

## Phase 2: Local Command Wrapper Verification

Check these commands:

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

Each should support a safe status/help/dry-run mode.

## Phase 3: Registry Verification

Check:

~/WORK/tools/orchestra/config/global_observation_pipelines.json

Required categories:

- astronomy
- earth_observation
- aviation
- space
- geophysical
- human
- underwater_acoustic_networks
- planetary_probes
- news
- cybersecurity
- research_literature
- policy
- finance
- infrastructure

## Phase 4: Output Verification

Expected report root:

~/WORK/research/global_observation/reports

Reports should preserve:

- source URL
- retrieval timestamp
- source tier
- uncertainty label
- raw/interpreted separation
- no unsupported conclusions

## Phase 5: Workstation Integration

SpecShift status should call Orchestra audit or reference its latest report.

Pipeline reports should be able to coexist with Orchestra outputs without mixing raw intake and interpretation.

## Safety Boundary

Do not build:

- offensive cyber
- active external scans
- surveillance tooling
- individual tracking
- exploit generation
- automated response systems
- classified/agency-claim framing

## Immediate Next Action

Run:

tools/status/orchestra_status.sh

Then inspect:

docs/workstation/orchestra_implementation_audit_latest.md

Fix any missing local wrappers or registry gaps reported there.
