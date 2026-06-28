# NOAA/NWS Alert Intake Pipeline

Date created: 2026-06-27
Status: Draft v0.1
Scope: Official public weather alert awareness.

## Tool

tools/pipelines/noaa_alerts_fetch.py

## Dry-run

python3 tools/pipelines/noaa_alerts_fetch.py --dry-run

## Live fetch

python3 tools/pipelines/noaa_alerts_fetch.py --limit 10

## Boundary

Preserve NOAA/NWS agency language. Do not reinterpret severity, certainty, urgency, geography, risk, or action beyond official guidance.
