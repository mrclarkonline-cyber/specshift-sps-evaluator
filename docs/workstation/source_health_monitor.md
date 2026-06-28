# Source Health Monitor

Date created: 2026-06-27
Status: Draft v0.1
Scope: Local source-health readiness layer for public-source workstation pipelines.

## Purpose

The source health monitor prevents silent pipeline failure.

It does not harvest remote data yet.

It checks whether the minimum viable source registry is present and whether each MVP source has a planned readiness status.

## Current Tool

Path:

tools/pipelines/source_health_check.py

Current behavior:

- reads docs/workstation/minimum_viable_source_registry.md
- checks required MVP source sections
- reports planned registry status
- reserves future live health fields
- performs no network calls
- requires no credentials
- mutates no files

## Required MVP Sources

- cisa_kev
- usgs_earthquake
- federal_register
- arxiv
- noaa_alerts
- huggingface_metadata
- sec_edgar
- bbc_world_rss
- reuters_ap_rss

## Future Health Fields

Each live source should eventually track:

- last_successful_fetch
- last_failure
- failure_count
- format_valid
- rate_limited
- status: healthy | degraded | failing | disabled

## Safety Boundary

The source health monitor is not a harvester.

It should not:

- fetch remote data
- require credentials
- store payloads
- trigger alerts
- infer truth
- start automated actions

## Next Build

After source health baseline passes, build the first safe raw intake module:

tools/pipelines/cisa_kev_fetch.py

CISA KEV is the safest first live source because it is public, authoritative, structured JSON, and defensive-only.
