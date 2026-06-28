# Worldwide Pipeline Expansion Registry

Status: Registered backlog
Scope: Phase 2 worldwide public-source expansion

## Tier 1: Fastest / highest-confidence additions

| Pipeline | Region | Category | Status |
|---|---|---|---|
| WHO Disease Outbreak News | Global | health_and_biosecurity | registered |
| ReliefWeb / OCHA | Global | earth_and_environment | registered |
| GDACS | Global | earth_and_environment | registered |
| World Bank Open Data | Global | infrastructure_and_economics | registered |
| IMF Data | Global | infrastructure_and_economics | registered |
| EU Open Data Portal | EU | government_and_policy | registered |
| ECDC | EU | health_and_biosecurity | registered |
| BBC World Service RSS | Global | global_news | verify-first |
| Deutsche Welle RSS | Global | global_news | verify-first |
| Canada Open Government | Canada | government_and_policy | registered |
| data.gov.uk | UK | government_and_policy | registered |
| data.gov.au | Australia | government_and_policy | registered |

## Tier 2: High-value technical and environmental additions

| Pipeline | Region | Category | Status |
|---|---|---|---|
| Copernicus EMS / Data Space | EU / Global | earth_and_environment | registered |
| ECMWF | EU / Global | earth_and_environment | registered |
| ESA / EUMETSAT | EU / Global | space_and_astronomy | registered |
| JMA | Japan | space_earth_and_anomaly_feeds | registered |
| JAXA | Japan | space_and_astronomy | registered |
| Geonet NZ | New Zealand | earth_and_environment | registered |
| Geoscience Australia | Australia | earth_and_environment | registered |
| Smithsonian Global Volcanism Program | Global | earth_and_environment | registered |
| FAO GIEWS | Global | infrastructure_and_economics | registered |
| IAEA IEC | Global | earth_and_environment | registered |

## Tier 3: Regional expansion additions

| Pipeline | Region | Category | Status |
|---|---|---|---|
| Africa CDC | Africa | health_and_biosecurity | registered |
| PAHO | Americas | health_and_biosecurity | registered |
| AHA Centre | Southeast Asia | earth_and_environment | registered |
| BMKG Indonesia | Southeast Asia | earth_and_environment | registered |
| Singapore NEA | Southeast Asia | earth_and_environment | registered |
| INEGI | Mexico | infrastructure_and_economics | registered |
| ECLAC | Latin America / Caribbean | infrastructure_and_economics | registered |
| SSN Mexico | Mexico | earth_and_environment | registered |
| INPE Brazil | Brazil | earth_and_environment | registered |
| SERNAGEOMIN Chile | Chile | earth_and_environment | registered |
| CDEMA | Caribbean | earth_and_environment | registered |
| SICA | Central America | earth_and_environment | registered |

## Tier 4: Guarded media/state-claim sources

| Pipeline | Region | Category | Status |
|---|---|---|---|
| Reuters verification | Global | global_news | verify-first |
| AFP verification | Global | global_news | verify-first |
| Al Jazeera | MENA / Global | global_news | bias-flag-required |
| NHK World | Japan / Global | global_news | registered |
| Kyodo | Japan | global_news | registered |
| Yonhap | South Korea | global_news | registered |
| PTI | India | global_news | bias-flag-required |
| PIB India | India | government_and_policy | official-claim-only |
| Xinhua | China | global_news | state-media-guarded |
| TASS | Russia | global_news | state-media-guarded |

## Tier 5: Slow, specialized, or build-last sources

| Pipeline | Region | Category | Status |
|---|---|---|---|
| OECD | Global / OECD | infrastructure_and_economics | registered |
| BIS | Global | infrastructure_and_economics | registered |
| IEA | Global | infrastructure_and_economics | registered |
| Global Fishing Watch | Global | infrastructure_and_economics | privacy-guard-required |
| IMO | Global | infrastructure_and_economics | registered |
| NSIDC | Arctic / Antarctic | earth_and_environment | registered |
| SCAR / COMNAP | Antarctic | earth_and_environment | registered |
| Arctic Council / AMAP | Arctic | earth_and_environment | registered |
| National Gazettes | Multi-country | government_and_policy | per-country-only |
| National Statistical Offices | Multi-country | infrastructure_and_economics | per-country-only |
| Global anomaly flagger | Global | contradiction_and_claim_checking | build-last |

## Status Meaning

- registered: known source family, not yet live
- verify-first: URL/API availability must be checked before integration
- official-claim-only: source can report what an institution says, not validate it
- state-media-guarded: strict state-media/provenance/censorship labels required
- per-country-only: must be implemented one country at a time
- build-last: requires stable historical baselines before output has meaning
