# Fast Relevance Pipelines

Date updated: 2026-06-27
Status: Draft v0.3
Scope: Lawful, public-source or user-approved information pipelines for fast relevance detection.

## Core Principle

Raw intake first.

Interpretation second.

Contradiction and anomaly engines last.

No pipeline is allowed to convert an observation into a conclusion without source support and human-review rules.

## Top Pipeline Families

### 1. World News and Major Events

Purpose:
Track geopolitical shifts, conflicts, disasters, policy events, and major institutional announcements.

Candidate sources:
- Reuters RSS/API, verify current feed before use
- Associated Press RSS/API, verify current feed before use
- BBC World RSS
- Al Jazeera RSS
- GDELT Project API
- UN News

Frequency:
15-60 minutes depending on source stability.

Output:
Timestamped event log with source URLs, publication time, retrieval time, geographic entities, source tier, and uncertainty label.

Guardrails:
- Flag single-source breaking news as preliminary.
- Separate news from opinion.
- Do not declare consensus when sources diverge.
- Treat GDELT as broad but noisier than human-edited wire sources.

### 2. AI Model Releases and Technical Developments

Purpose:
Track model releases, benchmark claims, agentic tooling, and technical shifts.

Candidate sources:
- arXiv cs.AI / cs.LG / cs.CL / cs.CR
- Hugging Face Hub metadata API
- Papers with Code
- GitHub releases for selected repos
- major AI lab blogs
- DeepLearning.AI / The Batch

Output:
AI release digest with model, organization, source link, claimed benchmarks, license, verification state, and caution notes.

Guardrails:
- Self-reported benchmarks are claims.
- Do not download or execute model artifacts.
- Do not treat model existence as capability proof.
- Track licenses and unsafe serialization risk.

### 3. Cybersecurity Advisories and Vulnerabilities

Purpose:
Track known exploited vulnerabilities and defensive advisories.

Candidate sources:
- CISA Known Exploited Vulnerabilities JSON
- NIST NVD API
- MITRE CVE
- CERT/CC
- GitHub Security Advisories
- OSV.dev

Output:
Vulnerability digest with CVE, CVSS, affected product, KEV flag, mitigation source link, and local relevance note.

Guardrails:
- Defensive use only.
- No exploit code.
- No attack chains.
- No target-specific reconnaissance.
- No active probing.

### 4. Science and Research Literature

Purpose:
Track preprints, peer-reviewed publications, corrections, retractions, and citation context.

Candidate sources:
- arXiv API
- PubMed / NCBI E-utilities
- Semantic Scholar
- Crossref
- OpenAlex
- bioRxiv / medRxiv
- Retraction Watch where available

Output:
Research digest with title, authors, abstract, DOI/arXiv ID, peer-review status, source link, and confidence tier.

Guardrails:
- Preprints are not peer-reviewed.
- Citations do not equal correctness.
- Do not extract restricted dual-use operational details.
- Keep abstracts distinct from machine-generated summaries.

### 5. Government Policy and Regulatory Updates

Purpose:
Track rules, proposed rules, notices, legislation, agency mandates, and compliance-relevant changes.

Candidate sources:
- Federal Register API
- Congress.gov API
- regulations.gov
- EUR-Lex / EU Official Journal
- GOV.UK alerts
- White House RSS
- standards bodies where applicable

Output:
Policy change log with action type, proposed/final status, effective date, jurisdiction, source link, and human-review note.

Guardrails:
- Summary is not legal advice.
- Proposed is not enacted.
- Jurisdiction matters.
- Link primary text.

### 6. Public Financial and Macroeconomic Indicators

Purpose:
Track public filings, macro indicators, and corporate event disclosures for context.

Candidate sources:
- SEC EDGAR
- FRED
- World Bank Open Data
- IMF Data
- EIA
- BLS / BEA

Output:
Finance/macro digest with filing type, indicator, timestamp, source, units, and relevance note.

Guardrails:
- No investment advice.
- No trading signals.
- No automated trading.
- Distinguish official data from private estimates.
- Treat market sentiment as observation only.

### 7. Earth Observation and Natural Hazards

Purpose:
Track earthquakes, fires, weather alerts, disasters, and environmental hazard signals.

Candidate sources:
- USGS Earthquake GeoJSON
- NOAA/NWS API
- NASA EONET
- NASA FIRMS
- GDACS RSS
- Copernicus Emergency Management
- Smithsonian Global Volcanism Program

Output:
Hazard log with event type, severity, coordinates/region, official alert level, source, and uncertainty note.

Guardrails:
- Preserve agency certainty language.
- Do not infer causation.
- Distinguish automatic detection from reviewed alert.
- Avoid tactical mapping or targeting uses.

### 8. Space Weather and Astronomy Transients

Purpose:
Track solar flares, geomagnetic storms, CMEs, NEOs, and transient astronomy reports.

Candidate sources:
- NOAA SWPC alerts JSON
- NASA DONKI
- NASA CNEOS Scout / Sentry
- Minor Planet Center
- GCN / TAN
- Transient Name Server

Output:
Space weather / transient log with detection status, confirmation status, severity scale, and source.

Guardrails:
- Detected does not mean confirmed.
- Avoid alarmist language.
- Use official severity scales.
- No SETI/ET conclusion from anomaly data.

### 9. Open-Source Supply Chain and Dependency Integrity

Purpose:
Track package releases, dependency advisories, suspicious update patterns, and supply-chain risk.

Candidate sources:
- GitHub Security Advisories
- GitHub Releases API
- PyPI RSS / JSON
- npm registry
- Libraries.io
- OpenSSF
- OSV.dev

Output:
Dependency delta report with package, version, advisory link, CVE, risk note, and review status.

Guardrails:
- Never execute newly downloaded packages.
- No auto-update without review.
- Harvesting isolated from build/runtime environments.
- Flag typosquatting risk.

### 10. Infrastructure Outage and Internet Health

Purpose:
Track cloud outages, DNS/CDN issues, routing anomalies, and large-scale internet health.

Candidate sources:
- Cloudflare Radar
- RIPE Atlas / RIS
- IODA
- official AWS/Azure/GCP/Cloudflare status feeds
- ThousandEyes public reports where permitted

Output:
Outage event log with service, region, scope, start time, source, and confidence tier.

Guardrails:
- Passive consumption only.
- No active probes.
- No pings, sweeps, floods, or distressed-service tests.
- Crowdsourced data is only an indicator.

### 11. Public Health Surveillance

Purpose:
Track official outbreak notices and public-health advisories.

Candidate sources:
- WHO Disease Outbreak News
- CDC outbreak RSS
- ECDC
- Our World in Data
- Global.health
- ProMED with caution

Output:
Public-health brief with disease/event, location, official source, case count if provided, and uncertainty label.

Guardrails:
- No personal health data.
- Early outbreak data is uncertain.
- No medical advice.
- Separate case counts from modeled transmission.

### 12. Aviation and Maritime Aggregate Safety

Purpose:
Track aggregate logistics friction, major flight groundings, maritime chokepoint issues, and official safety notices.

Candidate sources:
- FAA NAS status
- FAA NOTAM access only if current public terms permit
- NTSB reports
- IMO / maritime official notices
- aggregate ADS-B/AIS sources only where terms allow

Output:
Aggregate logistics disruption log.

Guardrails:
- No individual private flight tracking.
- No private vessel tracking.
- Aggregate/system level only.
- Respect terms of service.

### 13. Patent and Standards Tracker

Purpose:
Track slow-moving technology horizon signals.

Candidate sources:
- USPTO / PatentsView
- EPO OPS
- WIPO Patentscope
- IETF Datatracker
- W3C
- ISO/IEC public updates

Output:
Monthly technology horizon report.

Guardrails:
- Patent filings are claims, not working products.
- Draft standards are not final standards.

### 14. SpecShift Buyer Trigger Watch

Purpose:
Find events that create urgency for observable-only workflow review.

Sources:
- agent incident reports
- finance workflow incidents
- public postmortems
- reliability failures
- AI product launches
- procurement and governance language
- SEC cyber/operations disclosures

Output:
Target company, event, workflow hypothesis, buyer role hypothesis, and claim-safe outreach note.

Guardrails:
- No exploitative incident framing.
- No overclaiming production fit.
- No protected method disclosure.

### 15. Finance Integrity Watch

Purpose:
Surface finance workflow relevance for SpecShift.

Sources:
- payments news
- SEC EDGAR
- finance automation announcements
- reconciliation platform updates
- ledger infrastructure releases
- fintech outages

Output:
Company, workflow implicated, possible SpecShift fit, buyer role hypothesis, and risk note.

Guardrails:
- No trading advice.
- No compliance certification claims.
- No severity score unless buyer-controlled.

### 16. AI-for-Science Watch

Purpose:
Find simulation trajectory review opportunities.

Sources:
- arXiv
- Semantic Scholar
- OpenAlex
- materials / physics / biology simulation papers
- AI-for-science lab updates

Output:
Paper/project, simulation trajectory relevance, discrepancy-review angle, label/baseline possibility.

Guardrails:
- No scientific proof claims.
- Human expert adjudication required.

### 17. Materials Stability / Shielding / Composites Watch

Purpose:
Track materials research relevant to stability, shielding, degradation, and functional composites.

Sources:
- arXiv
- Crossref
- OpenAlex
- NASA / DOE / NIST public pages
- journal feeds
- university lab releases

Output:
Material domain, trajectory type, data availability, claim ladder level, next research action.

Guardrails:
- No material safety claims.
- No weapons or battlefield use.
- Separate hypothesis, simulation, experiment, replication, and readiness.

### 18. Multi-Source Contradiction Detector

Purpose:
Flag where high-quality sources disagree on the same event, number, or claim.

Sources:
- internal outputs from raw pipelines.

Output:
Contradiction log with source A, source B, divergence type, timestamps, and unresolved flag.

Guardrails:
- Do not pick a winner automatically.
- Disagreement is not misinformation.
- Human review required.
- Build only after stable raw pipelines exist.

### 19. Claim-Overstatement Detector

Purpose:
Flag headlines, summaries, or internal interpretations that assert more than the primary source supports.

Sources:
- internal outputs plus source documents.

Output:
Overstatement log with headline/summary language and primary-source basis.

Guardrails:
- Checks language only.
- Does not adjudicate truth.
- Does not replace human review.

### 20. Low-Frequency High-Impact Anomaly Detector

Purpose:
Detect rare statistical outliers across quantitative feeds.

Sources:
- internal time-series records after sufficient baseline exists.

Output:
Anomaly report with stream, anomaly score, baseline, time range, and source links.

Guardrails:
- Build last.
- Requires explicit null hypothesis and historical baseline.
- Anomaly is not cause.
- No automated action.
- Confidence capped at hypothesis unless validated externally.

## Priority Implementation Order

1. unified schema and source registry
2. CISA KEV
3. USGS Earthquake GeoJSON
4. Federal Register
5. arXiv
6. NOAA/NWS or NOAA SWPC
7. Hugging Face metadata
8. SEC EDGAR basic
9. BBC/Reuters/AP RSS after live feed verification
10. daily digest generator
11. source health monitor
12. claim safety gate
13. SpecShift Buyer Trigger Watch
14. Finance Integrity Watch
15. contradiction detector
16. claim-overstatement detector
17. low-frequency anomaly detector

## Minimum Viable Source List

Start with:

- CISA KEV JSON
- USGS Earthquake GeoJSON
- Federal Register API
- arXiv API
- NOAA SWPC alerts JSON or NOAA/NWS alerts API
- Hugging Face metadata API
- SEC EDGAR
- BBC World RSS
- Reuters/AP RSS only after confirming current live feeds

## Breaking Alert Policy

Week-one breaking alerts should be restricted to Tier 1 or official telemetry sources:

- new CISA KEV entry
- high-severity CVE with active exploitation
- USGS earthquake above configured threshold
- NOAA/NWS warning
- NOAA SWPC severe space weather alert
- official Federal Register / agency emergency action if relevant

Wire-service breaking alerts come later, after source verification and contradiction checks are stable.

## Daily Digest Sections

1. Executive Summary
2. Critical Security
3. AI / Technical Releases
4. Research Literature
5. Policy and Regulatory
6. Financial / Corporate Filings
7. Earth / Space / Infrastructure
8. SpecShift Buyer Triggers
9. Epistemic Friction
10. Pipeline Health

## What Not To Build Yet

- social media truth monitoring
- real-time video/audio analysis
- individual aircraft or vessel tracking
- active external scanning
- automated trading
- forecasting engines
- anomaly detector without baseline
- contradiction detector before stable source diversity exists
