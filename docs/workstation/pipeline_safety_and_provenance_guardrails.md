# Pipeline Safety and Provenance Guardrails

Date updated: 2026-06-27
Status: Draft v0.2
Scope: Safety rules for fast relevance pipelines.

## Core Doctrine

Observation is not conclusion.

Correlation is not cause.

Anomaly is not proof.

A preprint is not settled science.

A company benchmark is a claim until independently verified.

A contradiction is not misinformation by itself.

## Required Guardrails

### Provenance

Every item must include:
- source URL
- source name
- retrieval timestamp
- publication timestamp when available
- source type
- uncertainty label
- pipeline name
- claim safety notes

### Raw / Interpreted Separation

Raw source fields must remain separate from:
- machine-generated summaries
- importance scores
- anomaly scores
- contradiction labels
- SpecShift relevance notes

### Cybersecurity

Allowed:
- defensive advisory monitoring
- CVE awareness
- patch status awareness
- dependency risk awareness

Not allowed:
- exploit code
- attack chains
- target-specific reconnaissance
- active probing
- evasion guidance
- weaponization

### Finance

Allowed:
- public filings
- macro indicators
- finance workflow relevance
- SpecShift buyer-trigger awareness

Not allowed:
- investment advice
- trading signals
- automated trading
- compliance certification claims

### Health

Allowed:
- official outbreak notices
- aggregated public-health data
- uncertainty-labeled summaries

Not allowed:
- personal health data
- panic language
- medical advice
- treating early reports as validated epidemiology

### Science

Allowed:
- literature monitoring
- DOI/citation tracking
- preprint tagging
- retraction/correction watch

Not allowed:
- treating preprints as settled science
- claiming validation from one paper
- extracting restricted operational biosecurity details

### AI Models

Allowed:
- model metadata tracking
- license tracking
- benchmark claim logging
- paper/source linking

Not allowed:
- executing unverified model artifacts
- unsafe binary loading
- treating self-reported benchmarks as verified
- ignoring license restrictions

### Earth / Space / Hazard

Allowed:
- official hazard alerts
- official telemetry
- aggregate regional reporting

Not allowed:
- tactical mapping
- private-person tracking
- origin/intent claims from anomalies
- SETI/ET conclusions from transient data

### Aviation / Maritime

Allowed:
- aggregate logistics disruption monitoring
- official safety notices
- system-level status

Not allowed:
- individual private flight tracking
- individual private vessel tracking
- surveillance
- targeting
- terms-of-service violations

### Contradiction Detector

Allowed:
- flag unresolved variance
- list source A vs source B differences
- downgrade confidence
- send to human review

Not allowed:
- choosing the true source automatically
- labeling disagreement as misinformation by default
- hiding the underlying sources

### Anomaly Detector

Allowed:
- flag statistical outliers with baseline
- attach raw evidence
- require human review
- preserve alternatives

Not allowed:
- asserting cause
- generating urgency without support
- triggering automated action
- operating without null hypothesis and baseline

## Required Warning for Interpretive Reports

Use this sentence:

This output flags unresolved variance or anomaly for review; it does not establish cause, intent, origin, or validated conclusion.

## What Not To Build Yet

Do not build yet:
- low-frequency anomaly detection
- complex predictive modeling
- social media truth monitoring
- individual flight/vessel tracking
- active security scans
- video/audio analysis
- automated actions based on alerts
