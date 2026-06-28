# Worldwide Pipeline Schema Extension

Status: Required before Phase 2 live integrations
Scope: Translation, cross-country comparison, and bias/censorship fields

## Purpose

The completed 18-pipeline stack uses a provenance-first schema.

Worldwide expansion requires added fields so international, multilingual, and cross-country material does not collapse into false certainty.

## Required Added Fields

- source_country_or_region
- source_language
- title_original_language
- title_translated
- summary_original_language
- summary_translated
- translation_method: none | machine | human | source_provided
- translation_confidence: high | medium | low | unknown
- translation_notes
- bias_or_censorship_risk: low | medium | high | unknown
- bias_or_censorship_notes
- source_governance_type: intergovernmental | national_government | public_broadcaster | independent_wire | state_media | academic | ngo | commercial | unknown
- official_claim_status: not_official_claim | official_claim | state_media_claim | agency_observation
- cross_country_comparisons
- divergence_type: none | factual_conflict | timing_mismatch | methodology_difference | translation_uncertainty | framing_difference | omission_asymmetry | state_claim_vs_independent_report
- cross_source_matches
- claim_safety_notes

## Cross-Country Comparison Object

Each comparison object should include:

- comparison_indicator
- country
- value
- unit
- as_of_date
- methodology_note
- comparison_warning: none | methodology_mismatch | reporting_gap | translation_risk | revision_risk

## Translation Rules

- Preserve original language text as the authoritative stored text.
- Store translated text separately.
- Do not overwrite original text with translation.
- Mark machine translation clearly.
- High-stakes translated claims require human review or independent corroboration.
- Politically loaded terms should preserve original wording in notes where possible.

## Bias / Censorship Rules

Bias and censorship risk is scored per source, not per country.

A country can have official gazettes, public broadcasters, independent outlets, state-controlled outlets, academic repositories, and citizen/NGO reports. These must not be collapsed into one national risk score.

## State-Media Rule

State-media or single-country official claims can be recorded as official claims.

They cannot become validated conclusions without independent corroboration.

Default cap:

- state_media_claim + no corroboration = hypothesis or official_claim only

## Cross-Country Comparison Rule

Importance is not confidence.

A discrepancy is not automatically a contradiction.

Before flagging contradiction, check:

- unit differences
- fiscal year differences
- reporting lag
- definition mismatch
- methodology difference
- exchange-rate basis
- per-capita vs aggregate
- provisional vs final data
- translation error

## Claim Safety Gate Extension

No worldwide record advances to validated_conclusion unless:

1. source URL exists
2. retrieval timestamp exists
3. source country/region exists
4. original language field exists when applicable
5. uncertainty label exists
6. bias/censorship field exists
7. translation field exists when applicable
8. high-stakes claim has corroboration or authoritative primary source support
9. state-media claims are not promoted without independent confirmation
10. cross-country comparisons include methodology notes

## Digest Rule

Daily global digests must separate:

- direct instrument/agency observations
- official claims
- independent news reports
- translated summaries
- cross-country comparisons
- contradiction/friction items
- unverified/state-media-only items
