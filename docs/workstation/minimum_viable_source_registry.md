# Minimum Viable Source Registry

Date created: 2026-06-27
Status: Draft v0.1
Scope: Initial public-source registry for workstation MVP.

## Registry Rules

Each source must define:

- source_id
- source name
- source tier
- category
- access type
- API key requirement
- expected format
- update cadence
- guardrails
- current status

## MVP Sources

### cisa_kev

Name:
CISA Known Exploited Vulnerabilities

Tier:
tier_1_authoritative

Category:
cybersecurity

Access:
public JSON

Key required:
no

Format:
JSON

Cadence:
every 4 hours or daily during MVP

Guardrails:
defensive only; no exploit generation; no target-specific reconnaissance

Status:
ready for build

### usgs_earthquake

Name:
USGS Earthquake Feed

Tier:
tier_1_authoritative

Category:
earth hazard

Access:
public GeoJSON

Key required:
no

Format:
GeoJSON

Cadence:
15 minutes or daily during MVP

Guardrails:
preserve preliminary/revised status; no causal inference

Status:
ready for build

### federal_register

Name:
Federal Register API

Tier:
tier_1_authoritative

Category:
policy

Access:
public API

Key required:
no

Format:
JSON

Cadence:
daily

Guardrails:
summary is not legal advice; proposed is not final

Status:
ready for build

### arxiv

Name:
arXiv API

Tier:
tier_3_preprint

Category:
research

Access:
public API

Key required:
no

Format:
Atom/XML

Cadence:
daily

Guardrails:
preprint tag required; not peer-reviewed

Status:
ready for build

### noaa_alerts

Name:
NOAA/NWS or NOAA SWPC Alerts

Tier:
tier_1_authoritative

Category:
earth/space weather

Access:
public API/JSON

Key required:
usually no, verify before build

Format:
JSON

Cadence:
15-30 minutes or daily during MVP

Guardrails:
preserve agency severity/confidence language

Status:
verify endpoint then build

### huggingface_metadata

Name:
Hugging Face Hub Metadata

Tier:
tier_3_self_reported_metadata

Category:
AI model monitoring

Access:
public API

Key required:
not for basic public metadata, verify rate limits

Format:
JSON

Cadence:
daily

Guardrails:
metadata only; no model downloads; benchmarks are claims

Status:
ready after schema

### sec_edgar

Name:
SEC EDGAR

Tier:
tier_1_authoritative

Category:
financial/corporate filings

Access:
public API

Key required:
no, but descriptive User-Agent required

Format:
JSON/HTML filings

Cadence:
daily

Guardrails:
no investment advice; no trading signals

Status:
ready after User-Agent config

### bbc_world_rss

Name:
BBC World RSS

Tier:
tier_2_wire_or_reputable_news

Category:
world news

Access:
public RSS

Key required:
no

Format:
RSS/XML

Cadence:
hourly

Guardrails:
single-source breaking news is preliminary

Status:
verify live feed before build

### reuters_ap_rss

Name:
Reuters/AP RSS

Tier:
tier_2_wire

Category:
world news

Access:
RSS/API depending on current availability

Key required:
verify

Format:
RSS/XML or API

Cadence:
hourly

Guardrails:
live-verify feeds before building; do not assume URL stability

Status:
verify before build

## Later Sources

Add later:
- NIST NVD
- PubMed
- Semantic Scholar
- Crossref
- GitHub Advisories
- OSV.dev
- GDELT
- NASA EONET
- NASA DONKI
- Cloudflare Radar
- IODA
- WHO/CDC
- PyPI
- npm
- OpenAlex

## Source Health Fields

Each source should track:

- last_successful_fetch
- last_failure
- failure_count
- format_valid
- rate_limited
- status: healthy | degraded | failing | disabled
