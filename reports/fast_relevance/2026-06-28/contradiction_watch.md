# Multi-Source Contradiction Watch

Generated at UTC: 2026-06-28T01:41:27.413351Z
Report folder: reports/fast_relevance/2026-06-28

## Safety Boundary

This output flags unresolved variance or anomaly for review; it does not establish cause, intent, origin, or validated conclusion.

The contradiction detector does not pick a winner. It only surfaces possible divergence, overlap, or uncertainty differences for human review.

## Method

- Scans local generated markdown digests only.
- Extracts rough entity and numeric overlaps.
- Flags numeric variance, source-tier differences, and uncertainty-label differences.
- Does not fetch network data.
- Does not mutate source digests.

## Candidate Divergence / Friction Items

### 1. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/ai_models_huggingface_metadata.md
- Left title: Hugging Face Model Metadata Digest
- Left source: https://huggingface.co/api/models?limit=3&sort=lastModified&direction=-1
- Left tier: tier_3
- Left uncertainty: - Uncertainty label: self_reported_platform_metadata
- Right source digest: reports/fast_relevance/2026-06-28/cybersecurity_cisa_kev.md
- Right title: CISA KEV Defensive Advisory Digest
- Right source: https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
- Right tier: tier_1_authoritative
- Right uncertainty: - Uncertainty label: institutional_directive
- Shared entities: Raw, SHA256, Safety Boundary

This, UTC, Uncertainty
- Shared numbers: 06, 1, 2, 2026, 26, 28, 3, 41
- Left-only numbers: 0, 18, 22, 87
- Right-only numbers: 03, 04, 12569, 1629, 20230, 2025, 2026.06, 21, 23, 25, 67038
- Divergence notes: numeric_variance, source_tier_difference, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 2. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/ai_models_huggingface_metadata.md
- Left title: Hugging Face Model Metadata Digest
- Left source: https://huggingface.co/api/models?limit=3&sort=lastModified&direction=-1
- Left tier: tier_3
- Left uncertainty: - Uncertainty label: self_reported_platform_metadata
- Right source digest: reports/fast_relevance/2026-06-28/earth_hazards_usgs_earthquake.md
- Right title: USGS Earthquake GeoJSON Digest
- Right source: https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson
- Right tier: tier_1_authoritative
- Right uncertainty: - Uncertainty label: official_telemetry_preliminary_possible
- Shared entities: Claim Safety Note, Raw, SHA256, Safety Boundary

This, UTC, Uncertainty
- Shared numbers: 0, 06, 1, 2, 2026, 26, 28, 3, 41
- Left-only numbers: 18, 22, 87
- Right-only numbers: 09, 10, 104.6082, 112, 12, 127.2767, 13, 14, 142.4136, 19, 200, 21, 24, 29, 32
- Divergence notes: numeric_variance, source_tier_difference, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 3. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/ai_models_huggingface_metadata.md
- Left title: Hugging Face Model Metadata Digest
- Left source: https://huggingface.co/api/models?limit=3&sort=lastModified&direction=-1
- Left tier: tier_3
- Left uncertainty: - Uncertainty label: self_reported_platform_metadata
- Right source digest: reports/fast_relevance/2026-06-28/earth_weather_noaa_alerts.md
- Right title: NOAA/NWS Active Alert Digest
- Right source: https://api.weather.gov/alerts/active
- Right tier: tier_1_authoritative
- Right uncertainty: - Uncertainty label: official_alert_preserve_agency_language
- Shared entities: Claim Safety Note, Raw, SHA256, Safety Boundary

This, UTC, Uncertainty
- Shared numbers: 06, 1, 2, 2026, 28, 3, 41
- Left-only numbers: 0, 18, 22, 26, 87
- Right-only numbers: 0.1, 00, 001.1, 05, 11, 1100, 2.49, 25, 27, 30, 38, 405, 45, 47, 7
- Divergence notes: numeric_variance, source_tier_difference, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 4. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/ai_models_huggingface_metadata.md
- Left title: Hugging Face Model Metadata Digest
- Left source: https://huggingface.co/api/models?limit=3&sort=lastModified&direction=-1
- Left tier: tier_3
- Left uncertainty: - Uncertainty label: self_reported_platform_metadata
- Right source digest: reports/fast_relevance/2026-06-28/finance_sec_edgar_basic.md
- Right title: SEC EDGAR Basic Company Ticker Digest
- Right source: https://www.sec.gov/files/company_tickers.json
- Right tier: tier_1_authoritative
- Right uncertainty: - Uncertainty label: official_sec_company_metadata
- Shared entities: Raw, SHA256, Safety Boundary

This, UTC, Uncertainty
- Shared numbers: 06, 1, 2, 2026, 26, 28, 3, 41
- Left-only numbers: 0, 18, 22, 87
- Right-only numbers: 0000320193, 0001045810, 0001652044, 10433
- Divergence notes: numeric_variance, source_tier_difference, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 5. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/ai_models_huggingface_metadata.md
- Left title: Hugging Face Model Metadata Digest
- Left source: https://huggingface.co/api/models?limit=3&sort=lastModified&direction=-1
- Left tier: tier_3
- Left uncertainty: - Uncertainty label: self_reported_platform_metadata
- Right source digest: reports/fast_relevance/2026-06-28/policy_federal_register.md
- Right title: Federal Register Policy Intake Digest
- Right source: https://www.federalregister.gov/api/v1/documents.json?per_page=10&order=newest&conditions%5Bpublication_date%5D%5Bgte%5D=2026-06-20&conditions%5Btype%5D%5B%5D=RULE&conditions%5Btype%5D%5B%5D=PRORULE&conditions%5Btype%5D%5B%5D=NOTICE
- Right tier: tier_1_authoritative
- Right uncertainty: - Uncertainty label: institutional_source_policy_record
- Shared entities: Claim Safety Note, Raw, SHA256, Safety Boundary

This, UTC, Uncertainty
- Shared numbers: 06, 1, 2, 2026, 28, 3, 41
- Left-only numbers: 0, 18, 22, 26, 87
- Right-only numbers: 10, 10036, 11094, 13116, 20, 24, 29, 50, 719
- Divergence notes: numeric_variance, source_tier_difference, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 6. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/ai_models_huggingface_metadata.md
- Left title: Hugging Face Model Metadata Digest
- Left source: https://huggingface.co/api/models?limit=3&sort=lastModified&direction=-1
- Left tier: tier_3
- Left uncertainty: - Uncertainty label: self_reported_platform_metadata
- Right source digest: reports/fast_relevance/2026-06-28/research_arxiv.md
- Right title: arXiv Research Intake Digest
- Right source: https://export.arxiv.org/api/query?search_query=cat%3Acs.AI%2BOR%2Bcat%3Acs.LG%2BOR%2Bcat%3Acs.CL%2BOR%2Bcat%3Acs.CR%2BOR%2Bcat%3Astat.ML&start=0&max_results=3&sortBy=submittedDate&sortOrder=descending
- Right tier: unknown
- Right uncertainty: uncertainty label: unknown
- Shared entities: Latest, Raw, SHA256, Safety Boundary

This, UTC
- Shared numbers: 0, 06, 2026, 28, 3, 41
- Left-only numbers: 1, 18, 2, 22, 26, 87
- Right-only numbers: 24
- Divergence notes: numeric_variance, source_tier_difference, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 7. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/ai_models_huggingface_metadata.md
- Left title: Hugging Face Model Metadata Digest
- Left source: https://huggingface.co/api/models?limit=3&sort=lastModified&direction=-1
- Left tier: tier_3
- Left uncertainty: - Uncertainty label: self_reported_platform_metadata
- Right source digest: reports/fast_relevance/2026-06-28/world_news_rss.md
- Right title: World News RSS Verification and Intake Digest
- Right source: bbc_world
- Right tier: tier_2
- Right uncertainty: - Uncertainty label: single_source_preliminary
- Shared entities: Claim Safety Note, Raw, SHA256, Safety Boundary

This, UTC, Uncertainty
- Shared numbers: 06, 1, 2, 2026, 26, 28, 3, 41
- Left-only numbers: 0, 18, 22, 87
- Right-only numbers: 08, 12, 21, 27, 30, 35, 40, 51, 56, 920
- Divergence notes: numeric_variance, source_tier_difference, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 8. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/cybersecurity_cisa_kev.md
- Left title: CISA KEV Defensive Advisory Digest
- Left source: https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
- Left tier: tier_1_authoritative
- Left uncertainty: - Uncertainty label: institutional_directive
- Right source digest: reports/fast_relevance/2026-06-28/earth_hazards_usgs_earthquake.md
- Right title: USGS Earthquake GeoJSON Digest
- Right source: https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson
- Right tier: tier_1_authoritative
- Right uncertainty: - Uncertainty label: official_telemetry_preliminary_possible
- Shared entities: Raw, SHA256, Safety Boundary

This, URL, UTC, Uncertainty
- Shared numbers: 06, 1, 2, 2026, 21, 26, 28, 3, 41
- Left-only numbers: 03, 04, 12569, 1629, 20230, 2025, 2026.06, 23, 25, 67038
- Right-only numbers: 0, 09, 10, 104.6082, 112, 12, 127.2767, 13, 14, 142.4136, 19, 200, 24, 29, 32
- Divergence notes: numeric_variance, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 9. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/cybersecurity_cisa_kev.md
- Left title: CISA KEV Defensive Advisory Digest
- Left source: https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
- Left tier: tier_1_authoritative
- Left uncertainty: - Uncertainty label: institutional_directive
- Right source digest: reports/fast_relevance/2026-06-28/earth_weather_noaa_alerts.md
- Right title: NOAA/NWS Active Alert Digest
- Right source: https://api.weather.gov/alerts/active
- Right tier: tier_1_authoritative
- Right uncertainty: - Uncertainty label: official_alert_preserve_agency_language
- Shared entities: Raw, SHA256, Safety Boundary

This, UTC, Uncertainty
- Shared numbers: 06, 1, 2, 2026, 25, 28, 3, 41
- Left-only numbers: 03, 04, 12569, 1629, 20230, 2025, 2026.06, 21, 23, 26, 67038
- Right-only numbers: 0.1, 00, 001.1, 05, 11, 1100, 2.49, 27, 30, 38, 405, 45, 47, 7, 8
- Divergence notes: numeric_variance, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 10. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/cybersecurity_cisa_kev.md
- Left title: CISA KEV Defensive Advisory Digest
- Left source: https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
- Left tier: tier_1_authoritative
- Left uncertainty: - Uncertainty label: institutional_directive
- Right source digest: reports/fast_relevance/2026-06-28/finance_sec_edgar_basic.md
- Right title: SEC EDGAR Basic Company Ticker Digest
- Right source: https://www.sec.gov/files/company_tickers.json
- Right tier: tier_1_authoritative
- Right uncertainty: - Uncertainty label: official_sec_company_metadata
- Shared entities: Raw, SHA256, Safety Boundary

This, UTC, Uncertainty
- Shared numbers: 06, 1, 2, 2026, 26, 28, 3, 41
- Left-only numbers: 03, 04, 12569, 1629, 20230, 2025, 2026.06, 21, 23, 25, 67038
- Right-only numbers: 0000320193, 0001045810, 0001652044, 10433
- Divergence notes: numeric_variance, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 11. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/cybersecurity_cisa_kev.md
- Left title: CISA KEV Defensive Advisory Digest
- Left source: https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
- Left tier: tier_1_authoritative
- Left uncertainty: - Uncertainty label: institutional_directive
- Right source digest: reports/fast_relevance/2026-06-28/policy_federal_register.md
- Right title: Federal Register Policy Intake Digest
- Right source: https://www.federalregister.gov/api/v1/documents.json?per_page=10&order=newest&conditions%5Bpublication_date%5D%5Bgte%5D=2026-06-20&conditions%5Btype%5D%5B%5D=RULE&conditions%5Btype%5D%5B%5D=PRORULE&conditions%5Btype%5D%5B%5D=NOTICE
- Right tier: tier_1_authoritative
- Right uncertainty: - Uncertainty label: institutional_source_policy_record
- Shared entities: Raw, SHA256, Safety Boundary

This, UTC, Uncertainty
- Shared numbers: 06, 1, 2, 2026, 28, 3, 41
- Left-only numbers: 03, 04, 12569, 1629, 20230, 2025, 2026.06, 21, 23, 25, 26, 67038
- Right-only numbers: 10, 10036, 11094, 13116, 20, 24, 29, 50, 719
- Divergence notes: numeric_variance, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 12. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/cybersecurity_cisa_kev.md
- Left title: CISA KEV Defensive Advisory Digest
- Left source: https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
- Left tier: tier_1_authoritative
- Left uncertainty: - Uncertainty label: institutional_directive
- Right source digest: reports/fast_relevance/2026-06-28/research_arxiv.md
- Right title: arXiv Research Intake Digest
- Right source: https://export.arxiv.org/api/query?search_query=cat%3Acs.AI%2BOR%2Bcat%3Acs.LG%2BOR%2Bcat%3Acs.CL%2BOR%2Bcat%3Acs.CR%2BOR%2Bcat%3Astat.ML&start=0&max_results=3&sortBy=submittedDate&sortOrder=descending
- Right tier: unknown
- Right uncertainty: uncertainty label: unknown
- Shared entities: Raw, SHA256, Safety Boundary

This, UTC
- Shared numbers: 06, 2026, 28, 3, 41
- Left-only numbers: 03, 04, 1, 12569, 1629, 2, 20230, 2025, 2026.06, 21, 23, 25, 26, 67038
- Right-only numbers: 0, 24
- Divergence notes: numeric_variance, source_tier_difference, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 13. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/cybersecurity_cisa_kev.md
- Left title: CISA KEV Defensive Advisory Digest
- Left source: https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
- Left tier: tier_1_authoritative
- Left uncertainty: - Uncertainty label: institutional_directive
- Right source digest: reports/fast_relevance/2026-06-28/world_news_rss.md
- Right title: World News RSS Verification and Intake Digest
- Right source: bbc_world
- Right tier: tier_2
- Right uncertainty: - Uncertainty label: single_source_preliminary
- Shared entities: Raw, SHA256, Safety Boundary

This, URL, UTC, Uncertainty
- Shared numbers: 06, 1, 2, 2026, 21, 26, 28, 3, 41
- Left-only numbers: 03, 04, 12569, 1629, 20230, 2025, 2026.06, 23, 25, 67038
- Right-only numbers: 08, 12, 27, 30, 35, 40, 51, 56, 920
- Divergence notes: numeric_variance, source_tier_difference, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 14. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/earth_hazards_usgs_earthquake.md
- Left title: USGS Earthquake GeoJSON Digest
- Left source: https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson
- Left tier: tier_1_authoritative
- Left uncertainty: - Uncertainty label: official_telemetry_preliminary_possible
- Right source digest: reports/fast_relevance/2026-06-28/earth_weather_noaa_alerts.md
- Right title: NOAA/NWS Active Alert Digest
- Right source: https://api.weather.gov/alerts/active
- Right tier: tier_1_authoritative
- Right uncertainty: - Uncertainty label: official_alert_preserve_agency_language
- Shared entities: Claim Safety Note, Raw, SHA256, Safety Boundary

This, UTC, Uncertainty
- Shared numbers: 06, 1, 2, 2026, 28, 3, 41
- Left-only numbers: 0, 09, 10, 104.6082, 112, 12, 127.2767, 13, 14, 142.4136, 19, 200, 21, 24, 26
- Right-only numbers: 0.1, 00, 001.1, 05, 11, 1100, 2.49, 25, 27, 30, 38, 405, 45, 47, 7
- Divergence notes: numeric_variance, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 15. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/earth_hazards_usgs_earthquake.md
- Left title: USGS Earthquake GeoJSON Digest
- Left source: https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson
- Left tier: tier_1_authoritative
- Left uncertainty: - Uncertainty label: official_telemetry_preliminary_possible
- Right source digest: reports/fast_relevance/2026-06-28/finance_sec_edgar_basic.md
- Right title: SEC EDGAR Basic Company Ticker Digest
- Right source: https://www.sec.gov/files/company_tickers.json
- Right tier: tier_1_authoritative
- Right uncertainty: - Uncertainty label: official_sec_company_metadata
- Shared entities: Raw, SHA256, Safety Boundary

This, UTC, Uncertainty
- Shared numbers: 06, 1, 2, 2026, 26, 28, 3, 41
- Left-only numbers: 0, 09, 10, 104.6082, 112, 12, 127.2767, 13, 14, 142.4136, 19, 200, 21, 24, 29
- Right-only numbers: 0000320193, 0001045810, 0001652044, 10433
- Divergence notes: numeric_variance, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 16. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/earth_hazards_usgs_earthquake.md
- Left title: USGS Earthquake GeoJSON Digest
- Left source: https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson
- Left tier: tier_1_authoritative
- Left uncertainty: - Uncertainty label: official_telemetry_preliminary_possible
- Right source digest: reports/fast_relevance/2026-06-28/policy_federal_register.md
- Right title: Federal Register Policy Intake Digest
- Right source: https://www.federalregister.gov/api/v1/documents.json?per_page=10&order=newest&conditions%5Bpublication_date%5D%5Bgte%5D=2026-06-20&conditions%5Btype%5D%5B%5D=RULE&conditions%5Btype%5D%5B%5D=PRORULE&conditions%5Btype%5D%5B%5D=NOTICE
- Right tier: tier_1_authoritative
- Right uncertainty: - Uncertainty label: institutional_source_policy_record
- Shared entities: Claim Safety Note, Raw, SHA256, Safety Boundary

This, Type, UTC, Uncertainty
- Shared numbers: 06, 1, 10, 2, 2026, 24, 28, 29, 3, 41, 50
- Left-only numbers: 0, 09, 104.6082, 112, 12, 127.2767, 13, 14, 142.4136, 19, 200, 21, 26, 32, 33
- Right-only numbers: 10036, 11094, 13116, 20, 719
- Divergence notes: numeric_variance, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 17. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/earth_hazards_usgs_earthquake.md
- Left title: USGS Earthquake GeoJSON Digest
- Left source: https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson
- Left tier: tier_1_authoritative
- Left uncertainty: - Uncertainty label: official_telemetry_preliminary_possible
- Right source digest: reports/fast_relevance/2026-06-28/research_arxiv.md
- Right title: arXiv Research Intake Digest
- Right source: https://export.arxiv.org/api/query?search_query=cat%3Acs.AI%2BOR%2Bcat%3Acs.LG%2BOR%2Bcat%3Acs.CL%2BOR%2Bcat%3Acs.CR%2BOR%2Bcat%3Astat.ML&start=0&max_results=3&sortBy=submittedDate&sortOrder=descending
- Right tier: unknown
- Right uncertainty: uncertainty label: unknown
- Shared entities: Raw, SHA256, Safety Boundary

This, UTC
- Shared numbers: 0, 06, 2026, 24, 28, 3, 41
- Left-only numbers: 09, 1, 10, 104.6082, 112, 12, 127.2767, 13, 14, 142.4136, 19, 2, 200, 21, 26
- Right-only numbers: none
- Divergence notes: numeric_variance, source_tier_difference, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 18. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/earth_hazards_usgs_earthquake.md
- Left title: USGS Earthquake GeoJSON Digest
- Left source: https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson
- Left tier: tier_1_authoritative
- Left uncertainty: - Uncertainty label: official_telemetry_preliminary_possible
- Right source digest: reports/fast_relevance/2026-06-28/world_news_rss.md
- Right title: World News RSS Verification and Intake Digest
- Right source: bbc_world
- Right tier: tier_2
- Right uncertainty: - Uncertainty label: single_source_preliminary
- Shared entities: Claim Safety Note, Raw, SHA256, Safety Boundary

This, URL, UTC, Uncertainty
- Shared numbers: 06, 1, 12, 2, 2026, 21, 26, 28, 3, 40, 41, 51
- Left-only numbers: 0, 09, 10, 104.6082, 112, 127.2767, 13, 14, 142.4136, 19, 200, 24, 29, 32, 33
- Right-only numbers: 08, 27, 30, 35, 56, 920
- Divergence notes: numeric_variance, source_tier_difference, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 19. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/earth_weather_noaa_alerts.md
- Left title: NOAA/NWS Active Alert Digest
- Left source: https://api.weather.gov/alerts/active
- Left tier: tier_1_authoritative
- Left uncertainty: - Uncertainty label: official_alert_preserve_agency_language
- Right source digest: reports/fast_relevance/2026-06-28/finance_sec_edgar_basic.md
- Right title: SEC EDGAR Basic Company Ticker Digest
- Right source: https://www.sec.gov/files/company_tickers.json
- Right tier: tier_1_authoritative
- Right uncertainty: - Uncertainty label: official_sec_company_metadata
- Shared entities: Raw, SHA256, Safety Boundary

This, UTC, Uncertainty
- Shared numbers: 06, 1, 2, 2026, 28, 3, 41
- Left-only numbers: 0.1, 00, 001.1, 05, 11, 1100, 2.49, 25, 27, 30, 38, 405, 45, 47, 7
- Right-only numbers: 0000320193, 0001045810, 0001652044, 10433, 26
- Divergence notes: numeric_variance, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 20. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/earth_weather_noaa_alerts.md
- Left title: NOAA/NWS Active Alert Digest
- Left source: https://api.weather.gov/alerts/active
- Left tier: tier_1_authoritative
- Left uncertainty: - Uncertainty label: official_alert_preserve_agency_language
- Right source digest: reports/fast_relevance/2026-06-28/policy_federal_register.md
- Right title: Federal Register Policy Intake Digest
- Right source: https://www.federalregister.gov/api/v1/documents.json?per_page=10&order=newest&conditions%5Bpublication_date%5D%5Bgte%5D=2026-06-20&conditions%5Btype%5D%5B%5D=RULE&conditions%5Btype%5D%5B%5D=PRORULE&conditions%5Btype%5D%5B%5D=NOTICE
- Right tier: tier_1_authoritative
- Right uncertainty: - Uncertainty label: institutional_source_policy_record
- Shared entities: Claim Safety Note, Raw, SHA256, Safety Boundary

This, UTC, Uncertainty
- Shared numbers: 06, 1, 2, 2026, 28, 3, 41
- Left-only numbers: 0.1, 00, 001.1, 05, 11, 1100, 2.49, 25, 27, 30, 38, 405, 45, 47, 7
- Right-only numbers: 10, 10036, 11094, 13116, 20, 24, 29, 50, 719
- Divergence notes: numeric_variance, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 21. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/earth_weather_noaa_alerts.md
- Left title: NOAA/NWS Active Alert Digest
- Left source: https://api.weather.gov/alerts/active
- Left tier: tier_1_authoritative
- Left uncertainty: - Uncertainty label: official_alert_preserve_agency_language
- Right source digest: reports/fast_relevance/2026-06-28/research_arxiv.md
- Right title: arXiv Research Intake Digest
- Right source: https://export.arxiv.org/api/query?search_query=cat%3Acs.AI%2BOR%2Bcat%3Acs.LG%2BOR%2Bcat%3Acs.CL%2BOR%2Bcat%3Acs.CR%2BOR%2Bcat%3Astat.ML&start=0&max_results=3&sortBy=submittedDate&sortOrder=descending
- Right tier: unknown
- Right uncertainty: uncertainty label: unknown
- Shared entities: Raw, SHA256, Safety Boundary

This, UTC
- Shared numbers: 06, 2026, 28, 3, 41
- Left-only numbers: 0.1, 00, 001.1, 05, 1, 11, 1100, 2, 2.49, 25, 27, 30, 38, 405, 45
- Right-only numbers: 0, 24
- Divergence notes: numeric_variance, source_tier_difference, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 22. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/earth_weather_noaa_alerts.md
- Left title: NOAA/NWS Active Alert Digest
- Left source: https://api.weather.gov/alerts/active
- Left tier: tier_1_authoritative
- Left uncertainty: - Uncertainty label: official_alert_preserve_agency_language
- Right source digest: reports/fast_relevance/2026-06-28/world_news_rss.md
- Right title: World News RSS Verification and Intake Digest
- Right source: bbc_world
- Right tier: tier_2
- Right uncertainty: - Uncertainty label: single_source_preliminary
- Shared entities: Claim Safety Note, Raw, SHA256, Safety Boundary

This, UTC, Uncertainty
- Shared numbers: 06, 1, 2, 2026, 27, 28, 3, 30, 41
- Left-only numbers: 0.1, 00, 001.1, 05, 11, 1100, 2.49, 25, 38, 405, 45, 47, 7, 8, 840.0
- Right-only numbers: 08, 12, 21, 26, 35, 40, 51, 56, 920
- Divergence notes: numeric_variance, source_tier_difference, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 23. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/finance_sec_edgar_basic.md
- Left title: SEC EDGAR Basic Company Ticker Digest
- Left source: https://www.sec.gov/files/company_tickers.json
- Left tier: tier_1_authoritative
- Left uncertainty: - Uncertainty label: official_sec_company_metadata
- Right source digest: reports/fast_relevance/2026-06-28/policy_federal_register.md
- Right title: Federal Register Policy Intake Digest
- Right source: https://www.federalregister.gov/api/v1/documents.json?per_page=10&order=newest&conditions%5Bpublication_date%5D%5Bgte%5D=2026-06-20&conditions%5Btype%5D%5B%5D=RULE&conditions%5Btype%5D%5B%5D=PRORULE&conditions%5Btype%5D%5B%5D=NOTICE
- Right tier: tier_1_authoritative
- Right uncertainty: - Uncertainty label: institutional_source_policy_record
- Shared entities: Raw, SHA256, Safety Boundary

This, UTC, Uncertainty
- Shared numbers: 06, 1, 2, 2026, 28, 3, 41
- Left-only numbers: 0000320193, 0001045810, 0001652044, 10433, 26
- Right-only numbers: 10, 10036, 11094, 13116, 20, 24, 29, 50, 719
- Divergence notes: numeric_variance, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 24. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/finance_sec_edgar_basic.md
- Left title: SEC EDGAR Basic Company Ticker Digest
- Left source: https://www.sec.gov/files/company_tickers.json
- Left tier: tier_1_authoritative
- Left uncertainty: - Uncertainty label: official_sec_company_metadata
- Right source digest: reports/fast_relevance/2026-06-28/research_arxiv.md
- Right title: arXiv Research Intake Digest
- Right source: https://export.arxiv.org/api/query?search_query=cat%3Acs.AI%2BOR%2Bcat%3Acs.LG%2BOR%2Bcat%3Acs.CL%2BOR%2Bcat%3Acs.CR%2BOR%2Bcat%3Astat.ML&start=0&max_results=3&sortBy=submittedDate&sortOrder=descending
- Right tier: unknown
- Right uncertainty: uncertainty label: unknown
- Shared entities: Raw, SHA256, Safety Boundary

This, UTC
- Shared numbers: 06, 2026, 28, 3, 41
- Left-only numbers: 0000320193, 0001045810, 0001652044, 1, 10433, 2, 26
- Right-only numbers: 0, 24
- Divergence notes: numeric_variance, source_tier_difference, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 25. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/finance_sec_edgar_basic.md
- Left title: SEC EDGAR Basic Company Ticker Digest
- Left source: https://www.sec.gov/files/company_tickers.json
- Left tier: tier_1_authoritative
- Left uncertainty: - Uncertainty label: official_sec_company_metadata
- Right source digest: reports/fast_relevance/2026-06-28/world_news_rss.md
- Right title: World News RSS Verification and Intake Digest
- Right source: bbc_world
- Right tier: tier_2
- Right uncertainty: - Uncertainty label: single_source_preliminary
- Shared entities: Raw, SHA256, Safety Boundary

This, UTC, Uncertainty
- Shared numbers: 06, 1, 2, 2026, 26, 28, 3, 41
- Left-only numbers: 0000320193, 0001045810, 0001652044, 10433
- Right-only numbers: 08, 12, 21, 27, 30, 35, 40, 51, 56, 920
- Divergence notes: numeric_variance, source_tier_difference, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 26. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/policy_federal_register.md
- Left title: Federal Register Policy Intake Digest
- Left source: https://www.federalregister.gov/api/v1/documents.json?per_page=10&order=newest&conditions%5Bpublication_date%5D%5Bgte%5D=2026-06-20&conditions%5Btype%5D%5B%5D=RULE&conditions%5Btype%5D%5B%5D=PRORULE&conditions%5Btype%5D%5B%5D=NOTICE
- Left tier: tier_1_authoritative
- Left uncertainty: - Uncertainty label: institutional_source_policy_record
- Right source digest: reports/fast_relevance/2026-06-28/research_arxiv.md
- Right title: arXiv Research Intake Digest
- Right source: https://export.arxiv.org/api/query?search_query=cat%3Acs.AI%2BOR%2Bcat%3Acs.LG%2BOR%2Bcat%3Acs.CL%2BOR%2Bcat%3Acs.CR%2BOR%2Bcat%3Astat.ML&start=0&max_results=3&sortBy=submittedDate&sortOrder=descending
- Right tier: unknown
- Right uncertainty: uncertainty label: unknown
- Shared entities: Raw, SHA256, Safety Boundary

This, UTC
- Shared numbers: 06, 2026, 24, 28, 3, 41
- Left-only numbers: 1, 10, 10036, 11094, 13116, 2, 20, 29, 50, 719
- Right-only numbers: 0
- Divergence notes: numeric_variance, source_tier_difference, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 27. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/policy_federal_register.md
- Left title: Federal Register Policy Intake Digest
- Left source: https://www.federalregister.gov/api/v1/documents.json?per_page=10&order=newest&conditions%5Bpublication_date%5D%5Bgte%5D=2026-06-20&conditions%5Btype%5D%5B%5D=RULE&conditions%5Btype%5D%5B%5D=PRORULE&conditions%5Btype%5D%5B%5D=NOTICE
- Left tier: tier_1_authoritative
- Left uncertainty: - Uncertainty label: institutional_source_policy_record
- Right source digest: reports/fast_relevance/2026-06-28/world_news_rss.md
- Right title: World News RSS Verification and Intake Digest
- Right source: bbc_world
- Right tier: tier_2
- Right uncertainty: - Uncertainty label: single_source_preliminary
- Shared entities: Claim Safety Note, Raw, SHA256, Safety Boundary

This, UTC, Uncertainty
- Shared numbers: 06, 1, 2, 2026, 28, 3, 41
- Left-only numbers: 10, 10036, 11094, 13116, 20, 24, 29, 50, 719
- Right-only numbers: 08, 12, 21, 26, 27, 30, 35, 40, 51, 56, 920
- Divergence notes: numeric_variance, source_tier_difference, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

### 28. Candidate source friction

- Left source digest: reports/fast_relevance/2026-06-28/research_arxiv.md
- Left title: arXiv Research Intake Digest
- Left source: https://export.arxiv.org/api/query?search_query=cat%3Acs.AI%2BOR%2Bcat%3Acs.LG%2BOR%2Bcat%3Acs.CL%2BOR%2Bcat%3Acs.CR%2BOR%2Bcat%3Astat.ML&start=0&max_results=3&sortBy=submittedDate&sortOrder=descending
- Left tier: unknown
- Left uncertainty: uncertainty label: unknown
- Right source digest: reports/fast_relevance/2026-06-28/world_news_rss.md
- Right title: World News RSS Verification and Intake Digest
- Right source: bbc_world
- Right tier: tier_2
- Right uncertainty: - Uncertainty label: single_source_preliminary
- Shared entities: Parsed JSON, Raw, SHA256, Safety Boundary

This, UTC
- Shared numbers: 06, 2026, 28, 3, 41
- Left-only numbers: 0, 24
- Right-only numbers: 08, 1, 12, 2, 21, 26, 27, 30, 35, 40, 51, 56, 920
- Divergence notes: numeric_variance, source_tier_difference, uncertainty_label_difference
- Claim safety note: unresolved variance only; human review required.

## Forbidden Conclusions

- Do not call a source false based only on this report.
- Do not call a source true based only on this report.
- Do not label disagreement as misinformation by default.
- Do not infer intent, cause, concealment, fraud, or manipulation.
- Do not promote unresolved variance to validated conclusion.

## Kira Recommendation

Use this report as an epistemic friction board. The correct next move is source review, not conclusion.
