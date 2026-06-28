# Federal Register Policy Intake Pipeline

Date created: 2026-06-27
Status: Draft v0.1
Scope: Official public policy/regulatory awareness.

## Purpose

This pipeline fetches Federal Register records for public policy and regulatory awareness.

It is the third live-capable Tier 1 intake module because the source is:

- public
- authoritative
- structured JSON
- primary-source federal publication data
- useful for AI, technology, procurement, standards, and compliance monitoring

## Tool

Path:

tools/pipelines/federal_register_fetch.py

## Modes

Dry-run:

python3 tools/pipelines/federal_register_fetch.py --dry-run

Live fetch:

python3 tools/pipelines/federal_register_fetch.py --limit 10 --days 7

Optional focused search:

python3 tools/pipelines/federal_register_fetch.py --limit 10 --days 30 --search-term "artificial intelligence"

## Output

Live fetch writes to:

reports/fast_relevance/YYYY-MM-DD/raw/federal_register_TIMESTAMP.json

and:

reports/fast_relevance/YYYY-MM-DD/policy_federal_register.md

## Safety Boundary

Allowed:

- official public policy awareness
- proposed/final rule tracking
- publication date tracking
- agency/source linking
- human-review triage

Not allowed:

- legal advice
- compliance determination
- jurisdiction-specific advice without human legal review
- claiming a proposed rule is final
- treating a summary as a substitute for primary text
- automated operational changes based only on feed output

## Claim Safety

A Federal Register item confirms a public federal document record.

It does not by itself establish:

- how the rule applies to a specific person
- how the rule applies to a specific company
- legal obligations in a specific situation
- final legal effect if the document is proposed or a notice
- commercial strategy without human review

## Next Step

After this tool is committed, the next safe source is:

tools/pipelines/arxiv_fetch.py

Reason:

arXiv is public, structured, and valuable for early research awareness, but all records must be tagged as preprints / not peer-reviewed.
