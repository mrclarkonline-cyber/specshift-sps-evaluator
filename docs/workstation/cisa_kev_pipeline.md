# CISA KEV Pipeline

Date created: 2026-06-27
Status: Draft v0.1
Scope: Defensive public-source cybersecurity advisory intake.

## Purpose

This pipeline fetches the CISA Known Exploited Vulnerabilities catalog for defensive awareness.

It is the first live-capable Tier 1 intake module because the source is:

- public
- authoritative
- structured JSON
- defensive in purpose
- useful for workstation security posture

## Tool

Path:

tools/pipelines/cisa_kev_fetch.py

## Modes

Dry-run:

python3 tools/pipelines/cisa_kev_fetch.py --dry-run

Live fetch:

python3 tools/pipelines/cisa_kev_fetch.py --limit 10

## Output

Live fetch writes to:

reports/fast_relevance/YYYY-MM-DD/raw/cisa_kev_TIMESTAMP.json

and:

reports/fast_relevance/YYYY-MM-DD/cybersecurity_cisa_kev.md

## Safety Boundary

Allowed:

- defensive advisory monitoring
- CVE awareness
- patch-status awareness
- workstation risk review
- source-linked summary generation

Not allowed:

- exploit generation
- attack chains
- target-specific reconnaissance
- active probing
- evasion guidance
- weaponization
- automated system changes based only on feed output

## Claim Safety

A CISA KEV entry means the vulnerability appears in the CISA Known Exploited Vulnerabilities catalog.

It does not by itself prove:

- local exposure
- local compromise
- local exploitability
- required local action without human review

## Next Step

After this tool is committed, the next safe source is:

tools/pipelines/usgs_earthquake_fetch.py

Reason:

USGS Earthquake GeoJSON is also public, structured, and authoritative.
