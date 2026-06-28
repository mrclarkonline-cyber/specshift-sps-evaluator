# Pipeline Tools

Date created: 2026-06-27
Status: Early implementation
Scope: Local validation and status tools for the workstation pipeline plan.

## Current Tools

### pipeline_registry_check.py

Validates the minimum viable source registry document before any source harvesting is built.

This is intentionally local-only.

It does not fetch remote data.

It does not require credentials.

It does not mutate source files.

## Design Rule

No harvesting before:

1. source registry exists
2. registry passes validation
3. unified schema exists
4. safety guardrails exist
5. workstation status command exists

## Next Tools

Planned:

- source_health_check.py
- claim_safety_gate.py
- daily_digest.py
- cisa_kev_fetch.py
- usgs_earthquake_fetch.py
- federal_register_fetch.py
