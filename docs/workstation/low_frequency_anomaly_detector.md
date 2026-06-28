# Low-Frequency High-Impact Anomaly Detector

Date created: 2026-06-27
Status: Draft v0.1
Scope: Conservative local anomaly-hypothesis scaffold for generated report history.

## Tool

tools/pipelines/low_frequency_anomaly_detector.py

## Dry-run

python3 tools/pipelines/low_frequency_anomaly_detector.py --dry-run

## Generate

python3 tools/pipelines/low_frequency_anomaly_detector.py

## Purpose

This detector is the final workplan item because it is the highest interpretive-risk layer.

It looks only at local report-history signals and generates a conservative anomaly watch.

It is not a prediction engine.

It is not a causation engine.

It is not an emergency-alert engine.

It is not a truth engine.

## Null Hypothesis

The default assumption is that observed variation in daily pipeline outputs is ordinary source-volume fluctuation, reporting cadence variation, or local ingestion artifact unless independently corroborated.

## What It Checks

- daily markdown digest count
- heading count
- numeric token count
- configured event-hint keyword counts
- coarse z-score deviations when enough history exists

## Safety Boundary

Allowed:

- flag candidate statistical outliers
- record baseline limitations
- require human review
- preserve source-inspection steps
- keep confidence capped at hypothesis

Not allowed:

- infer cause
- infer intent
- infer coordinated manipulation
- infer emergency status
- infer buyer urgency
- trigger automated operational action
- promote anomaly to validated conclusion

## Baseline Requirement

The default minimum baseline is 14 report days.

If fewer than 14 report days exist, the output must clearly say:

INSUFFICIENT BASELINE.

## Required Interpretive Warning

This output flags candidate statistical outliers for review only. It does not establish cause, intent, origin, prediction, emergency status, risk level, or validated conclusion.

## Required Review Steps

Before any interpretation:

1. Inspect source digests directly.
2. Confirm raw source records exist.
3. Check for duplicates or source-format changes.
4. Check contradiction and overstatement reports.
5. Seek independent corroboration.

## Workplan Status

This completes the initial 18-item workstation pipeline implementation list.
