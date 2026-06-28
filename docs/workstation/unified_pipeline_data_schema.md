# Unified Pipeline Data Schema

Date updated: 2026-06-27
Status: Draft v0.2
Scope: Shared record format for public-source fast relevance pipelines.

## Purpose

Every ingested item should preserve provenance, uncertainty, and raw/interpreted separation.

No record should enter the knowledge base without:

- source name
- source URL
- retrieval timestamp
- publication timestamp when available
- source type
- source tier
- raw payload hash or excerpt hash
- uncertainty label
- claim safety notes

## Minimal 7-Day Schema

Use this first:

Required fields:
- item_id
- pipeline
- source_name
- source_url
- retrieved_at
- published_at
- title
- summary
- raw_excerpt
- confidence
- uncertainty_label
- claim_safety_notes

## Full Schema Fields

Schema metadata:
- format_version
- record_id
- ingestion_id
- pipeline_name

Provenance:
- source_name
- source_url
- source_type
- source_reliability_tier
- retrieved_at_utc
- published_at_utc
- author_or_agency
- retrieval_method

Payload:
- title
- summary
- raw_text_or_excerpt
- entities
- locations
- topic_tags
- numerical_metrics

Epistemic state:
- classification
- confidence_score
- uncertainty_label
- verification_state

Cross reference:
- cross_source_matches
- contradicted_by
- related_ids
- claim_safety_notes

Integrity:
- raw_payload_sha256
- raw_excerpt_sha256
- deduplication_key
- human_review_required

## Source Confidence Tiers

Tier 1:
Official agency data, direct instrument telemetry, primary legal/regulatory source, SEC EDGAR, CISA, NIST, USGS, NOAA, NASA.

Tier 2:
Peer-reviewed literature, reputable wire services, PubMed-indexed publications, Reuters/AP/BBC after feed verification.

Tier 3:
Preprints, corporate release notes, vendor model cards, GDELT automated extraction, academic press releases.

Tier 4:
Crowdsourced reports, social media, forums, unverified blogs.

## Uncertainty Labels

Use:

- confirmed
- multiple_sources
- single_source
- preliminary
- preprint
- marketing_claim
- needs_verification
- conflicting
- low_confidence
- unknown

## Epistemic Ladder

1. Observation: directly reported by a source.
2. Correlation: co-occurrence noted, no causal claim.
3. Anomaly: deviation from baseline.
4. Hypothesis: proposed explanation.
5. Validated conclusion: independently corroborated or confirmed by authoritative body.

## Deduplication Strategy

Use layered deduplication:

1. exact URL match
2. SHA-256 hash of normalized title + source + published date
3. entity overlap and 24-hour temporal clustering
4. fuzzy title similarity
5. cross-stream event matching by location/time/entity

Duplicates should become additional provenance links, not inflated new events.

## Claim Safety Gate

No record advances from hypothesis to validated conclusion without:

- confirmation from originating authoritative source, or
- independent corroboration from a second Tier 1/Tier 2 source, and
- logged transition reason.

The transition must never be silent.
