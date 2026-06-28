# arXiv Research Intake Pipeline

Date created: 2026-06-27
Status: Draft v0.1
Scope: Public research-awareness intake.

## Purpose

This pipeline fetches arXiv records for research awareness.

It is the fourth live-capable intake module because the source is:

- public
- structured
- widely used for early research discovery
- relevant to AI, machine learning, cryptography, statistics, and SpecShift research lanes

## Tool

Path:

tools/pipelines/arxiv_fetch.py

## Modes

Dry-run:

python3 tools/pipelines/arxiv_fetch.py --dry-run

Live fetch:

python3 tools/pipelines/arxiv_fetch.py --limit 10

Focused search:

python3 tools/pipelines/arxiv_fetch.py --limit 10 --search-term "agent reliability"

Custom categories:

python3 tools/pipelines/arxiv_fetch.py --limit 10 --categories "cs.AI,cs.LG,stat.ML"

## Output

Live fetch writes to:

reports/fast_relevance/YYYY-MM-DD/raw/arxiv_TIMESTAMP.xml

reports/fast_relevance/YYYY-MM-DD/raw/arxiv_TIMESTAMP.json

and:

reports/fast_relevance/YYYY-MM-DD/research_arxiv.md

## Safety Boundary

Allowed:

- research awareness
- preprint discovery
- metadata extraction
- abstract summaries
- source-linked citation
- preprint vs peer-reviewed flagging

Not allowed:

- treating preprints as peer-reviewed
- claiming scientific consensus from one record
- claiming production readiness
- restricted dual-use operational extraction
- medical advice
- legal advice
- commercial validation claims

## Claim Safety

An arXiv item confirms that an author-submitted research record exists in arXiv.

It does not by itself establish:

- correctness
- peer review
- replication
- scientific consensus
- production readiness
- safety
- commercial validity

## Required Label

Every arXiv output must include:

preprint_not_peer_reviewed

## Next Step

After this tool is committed, the next safe source is:

tools/pipelines/noaa_alerts_fetch.py

Reason:

NOAA/NWS or NOAA SWPC alerts are official public telemetry/alert sources with clear severity language.
