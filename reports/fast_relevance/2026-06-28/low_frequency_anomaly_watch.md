# Low-Frequency High-Impact Anomaly Watch

Generated at UTC: 2026-06-28T01:41:27.517664Z
Report root: reports/fast_relevance
Current report day: reports/fast_relevance/2026-06-28

## Safety Boundary

This output flags candidate statistical outliers for review only. It does not establish cause, intent, origin, prediction, emergency status, risk level, or validated conclusion.

The anomaly detector is deliberately conservative. It requires baseline context and keeps all findings at observation or hypothesis level unless independently validated elsewhere.

## Null Hypothesis

The default assumption is that observed variation in daily pipeline outputs is ordinary source-volume fluctuation, reporting cadence variation, or local ingestion artifact unless independently corroborated.

## Baseline Requirements

- Minimum recommended historical days: 14
- Available historical days: 1
- Z-score threshold: 3.0
- Any candidate anomaly requires human review.
- Any candidate anomaly requires source-level inspection before interpretation.
- No automated action is permitted.

## Baseline Status

INSUFFICIENT BASELINE.

The system does not yet have enough historical daily reports to make meaningful low-frequency anomaly claims. This is expected for a new pipeline stack.

## Current Day Metrics

- Markdown source digest count: 8
- Heading count: 53
- Numeric token count: 339

## Candidate Metric Deviations

No z-score analysis performed because fewer than three report days are available.

## Event Hint Counts

- earthquake: 18
- alert: 18
- warning: 6
- watch: 1
- vulnerability: 7
- cve: 3
- kev: 4
- rule: 5
- notice: 6
- preprint: 1
- model: 10
- filing: 1
- workflow: 1

## Candidate Hint Deviations

No hint-level z-score analysis performed because fewer than three report days are available.

## Required Review Steps Before Any Interpretation

1. Inspect the source digests directly.
2. Confirm the relevant raw source records exist.
3. Check whether the spike is caused by duplicate records or source format changes.
4. Check contradiction and overstatement reports.
5. Seek independent corroboration before upgrading any item beyond hypothesis.

## Forbidden Conclusions

- Do not infer cause.
- Do not infer intent.
- Do not infer coordinated manipulation.
- Do not infer emergency status.
- Do not infer buyer urgency.
- Do not trigger automated operational action.
- Do not promote anomaly to validated conclusion.

## Output Classification

classification: anomaly_hypothesis_scaffold

confidence ceiling: hypothesis

human_review_required: true

## Kira Recommendation

Treat this as a smoke alarm for the data room, not as a diagnosis. First check whether the smoke is toast, wiring, weather, or a real fire.
