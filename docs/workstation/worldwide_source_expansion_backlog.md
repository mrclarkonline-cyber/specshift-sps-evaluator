# Worldwide Source Expansion Backlog

Status: Registered
Scope: Future source expansion after initial 18/18 workstation stack

## Immediate Next Build Group

1. WHO Disease Outbreak News
2. ReliefWeb / OCHA
3. GDACS
4. World Bank
5. IMF
6. EU Open Data Portal
7. ECDC
8. BBC World Service RSS verification
9. Deutsche Welle RSS verification
10. Canada Open Government

## Why These First

They are:

- relatively accessible
- high provenance
- broad international value
- low interpretive risk
- useful for global digest expansion
- strong complements to the existing US-centered stack

## Build Pattern For Each Source

For every worldwide source:

1. Add source metadata to registry.
2. Add guarded fetch script.
3. Support dry-run.
4. Support low-limit live fetch.
5. Preserve source URL and retrieval timestamp.
6. Preserve original language.
7. Add translation fields if needed.
8. Add bias/censorship risk field.
9. Add source governance type.
10. Run claim safety gate.
11. Generate validation report.
12. Commit, push, and land with wiki_landing.

## Do Not Build Yet

Do not build these until the schema extension and first worldwide sources are stable:

- Xinhua
- TASS
- national gazette family
- national statistical office cross-check family
- Global Fishing Watch
- individual vessel/flight tracking
- global anomaly flagger
- automated cross-country causal inference

## Explicit Prohibitions

No worldwide pipeline should support:

- surveillance of individuals
- tactical mapping
- military targeting
- active cyber probing
- exploit generation
- automated trading
- legal/medical/financial decisioning
- state-media claims promoted as facts
- anomaly claims promoted as conclusions
