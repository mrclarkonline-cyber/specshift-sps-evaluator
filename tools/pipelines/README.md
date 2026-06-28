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

### arxiv_fetch.py

Fetches arXiv research records for public research awareness.

Dry-run:

python3 tools/pipelines/arxiv_fetch.py --dry-run

Live fetch:

python3 tools/pipelines/arxiv_fetch.py --limit 10

Focused search:

python3 tools/pipelines/arxiv_fetch.py --limit 10 --search-term "agent reliability"

Safety boundary:

- research awareness only
- arXiv records are preprints / author-submitted records
- not peer-reviewed by default
- no validated conclusion from one record
- no medical/legal/commercial validation claims

### noaa_alerts_fetch.py

Fetches NOAA/NWS active alerts for official public alert awareness.

Dry-run:

python3 tools/pipelines/noaa_alerts_fetch.py --dry-run

Live fetch:

python3 tools/pipelines/noaa_alerts_fetch.py --limit 10

### huggingface_metadata_fetch.py

Fetches Hugging Face public model metadata only.

Dry-run:

python3 tools/pipelines/huggingface_metadata_fetch.py --dry-run

Live fetch:

python3 tools/pipelines/huggingface_metadata_fetch.py --limit 10

### sec_edgar_fetch.py

Fetches SEC public company ticker metadata.

Dry-run:

python3 tools/pipelines/sec_edgar_fetch.py --dry-run

Live fetch:

python3 tools/pipelines/sec_edgar_fetch.py --limit 10

### world_news_rss_fetch.py

Verifies and fetches initial public world-news RSS sources.

Dry-run:

python3 tools/pipelines/world_news_rss_fetch.py --dry-run

Verify-only:

python3 tools/pipelines/world_news_rss_fetch.py --verify-only

Live fetch:

python3 tools/pipelines/world_news_rss_fetch.py --limit 10

### daily_digest.py

Generates a local daily digest from generated source summaries.

Dry-run:

python3 tools/pipelines/daily_digest.py --dry-run

Generate:

python3 tools/pipelines/daily_digest.py

### claim_safety_gate.py

Runs a lightweight claim-safety scan on generated markdown digests.

Dry-run:

python3 tools/pipelines/claim_safety_gate.py --dry-run

Scan:

python3 tools/pipelines/claim_safety_gate.py --path reports/fast_relevance

### specshift_buyer_trigger_watch.py

Generates cautious SpecShift buyer-trigger triage from local source digests.

Dry-run:

python3 tools/pipelines/specshift_buyer_trigger_watch.py --dry-run

Generate:

python3 tools/pipelines/specshift_buyer_trigger_watch.py

### finance_integrity_watch.py

Generates finance-workflow relevance triage from local source digests.

Dry-run:

python3 tools/pipelines/finance_integrity_watch.py --dry-run

Generate:

python3 tools/pipelines/finance_integrity_watch.py

### contradiction_detector.py

Generates a local multi-source contradiction/friction report from generated source digests.

Dry-run:

python3 tools/pipelines/contradiction_detector.py --dry-run

Generate:

python3 tools/pipelines/contradiction_detector.py

Safety boundary:

- flags unresolved variance only
- does not pick a winner
- does not infer intent or cause
- requires human review

### claim_overstatement_detector.py

Generates a local claim-overstatement watch from generated source digests.

Dry-run:

python3 tools/pipelines/claim_overstatement_detector.py --dry-run

Generate:

python3 tools/pipelines/claim_overstatement_detector.py

Safety boundary:

- language-control guardrail only
- does not adjudicate truth
- does not infer cause or intent
- recommends bounded wording downgrades
- human review required

