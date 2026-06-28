# Phase 2 Worldwide Group 1 Configured

Status: configured, not live-ingested  
Date: 2026-06-28

## What changed

The first worldwide expansion build group now has a source registry and a health-check scaffold.

Configured sources:

1. WHO Disease Outbreak News
2. ReliefWeb / OCHA
3. GDACS
4. World Bank Open Data
5. IMF Data
6. EU Open Data Portal
7. ECDC

## Boundary

This is not yet live ingestion.

The scaffold checks whether candidate public endpoints are reachable and records a small health report. It does not claim:

- validated parsing
- durable ingestion
- contradiction detection
- production alerting
- legal, medical, financial, or emergency advice

## Guardrails

All sources remain public and provenance-preserving. The system must store source URL, retrieval timestamp, source region/country, language, uncertainty label, and original text/excerpt. Translation is derived and must not replace the original source text.

## Next implementation step

Turn each reachable source into a normalized record writer using the worldwide schema, starting with the lowest-risk structured sources:

1. GDACS
2. ReliefWeb / OCHA
3. World Bank
4. EU Open Data Portal
5. WHO DON
6. ECDC
7. IMF
