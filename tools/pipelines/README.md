# Pipeline Tools

Date updated: 2026-06-27
Status: Early implementation
Scope: Local validation and status tools for the workstation pipeline plan.

## Current Tools

### pipeline_registry_check.py

Validates the minimum viable source registry document before any source harvesting is built.

This is intentionally local-only.

It does not fetch remote data.

It does not require credentials.

It does not mutate source files.

### source_health_check.py

Reports local source-health readiness from the registry.

This is also local-only.

It reserves future live health fields but does not fetch network sources yet.

## Design Rule

No harvesting before:

1. source registry exists
2. registry passes validation
3. unified schema exists
4. safety guardrails exist
5. workstation status command exists
6. source health baseline passes

## Next Tools

Planned:

- cisa_kev_fetch.py
- usgs_earthquake_fetch.py
- federal_register_fetch.py
- arxiv_fetch.py
- claim_safety_gate.py
- daily_digest.py

## Live-Capable Intake Tools

### cisa_kev_fetch.py

Fetches the CISA Known Exploited Vulnerabilities catalog for defensive awareness.

Dry-run:

python3 tools/pipelines/cisa_kev_fetch.py --dry-run

Live fetch:

python3 tools/pipelines/cisa_kev_fetch.py --limit 10

Safety boundary:

- defensive awareness only
- no exploit generation
- no attack chains
- no active probing
- no target-specific reconnaissance

### usgs_earthquake_fetch.py

Fetches the USGS Earthquake GeoJSON feed for public geophysical awareness.

Dry-run:

python3 tools/pipelines/usgs_earthquake_fetch.py --dry-run

Live fetch:

python3 tools/pipelines/usgs_earthquake_fetch.py --limit 10

Safety boundary:

- public geophysical awareness only
- no aftershock prediction
- no unsupported impact claims
- no tactical mapping
- no automated emergency action

### federal_register_fetch.py

Fetches Federal Register records for public policy/regulatory awareness.

Dry-run:

python3 tools/pipelines/federal_register_fetch.py --dry-run

Live fetch:

python3 tools/pipelines/federal_register_fetch.py --limit 10 --days 7

Focused search:

python3 tools/pipelines/federal_register_fetch.py --limit 10 --days 30 --search-term "artificial intelligence"

Safety boundary:

- policy awareness only
- not legal advice
- proposed is not final
- primary source link required
- no automated operational changes

