# USGS Earthquake GeoJSON Pipeline

Date created: 2026-06-27
Status: Draft v0.1
Scope: Public geophysical telemetry intake.

## Purpose

This pipeline fetches the USGS Earthquake Hazards Program GeoJSON feed for public geophysical awareness.

It is the second live-capable Tier 1 intake module because the source is:

- public
- authoritative
- structured GeoJSON
- non-commercial
- useful for physical-world situational awareness

## Tool

Path:

tools/pipelines/usgs_earthquake_fetch.py

## Modes

Dry-run:

python3 tools/pipelines/usgs_earthquake_fetch.py --dry-run

Live fetch:

python3 tools/pipelines/usgs_earthquake_fetch.py --limit 10

## Output

Live fetch writes to:

reports/fast_relevance/YYYY-MM-DD/raw/usgs_earthquake_TIMESTAMP.geojson

and:

reports/fast_relevance/YYYY-MM-DD/earth_hazards_usgs_earthquake.md

## Safety Boundary

Allowed:

- public geophysical awareness
- official earthquake feed monitoring
- event summaries with source links
- preliminary/revised status preservation

Not allowed:

- predicting aftershocks
- inferring cause or intent
- asserting impact without official support
- tactical mapping
- private-person tracking
- automated emergency actions
- panic language

## Claim Safety

A USGS feed item confirms that USGS reported an earthquake event record.

It does not by itself establish:

- final magnitude
- final casualty/damage impact
- aftershock prediction
- risk to a specific person or facility
- required action without official emergency guidance

## Next Step

After this tool is committed, the next safe source is:

tools/pipelines/federal_register_fetch.py

Reason:

Federal Register is public, authoritative, structured, and directly supports policy/regulatory awareness.
