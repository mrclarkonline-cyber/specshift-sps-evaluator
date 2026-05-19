# SpecShift SPS Evaluator

A small Secure Program Synthesis sprint prototype for turning generated-code tasks into normalized audit checks across baseline tests, schema expectations, spec perturbations, and adversarial cases.

Core claim:

Visible test success is not the same as robust spec satisfaction.

## What it demonstrates

Many generated-code workflows treat passing visible tests as the main success signal. SpecShift separates that signal into several check types:

1. baseline tests
2. schema expectations
3. spec perturbations
4. adversarial cases

The current prototype does not execute generated code yet. It normalizes dataset checks into a consistent audit/reporting structure. Execution and scoring can be added later.

## Preferred demo command

`python3 runner.py --file dataset.json`

Expected output:

```text
=== SpecShift Runner Summary ===
Loaded 12 tasks
Generated 67 check cases

baseline: 20
schema: 12
spec_perturbation: 14
adversarial: 21
```

## Module structure

```text
schema.py          Shared Pydantic models and type definitions
perturbations.py   Normalizes baseline, schema, spec perturbation, and adversarial checks
runner.py          Preferred current demo path
aggregator.py      Reserved for readable summary table/report generation
main.py            Older placeholder LangGraph harness, preserved for now
dataset.json       Twelve sprint-safe generated-code evaluation tasks
```

## Current scope

This is a sprint-safe prototype. It is intentionally small, local, and judge-readable.

Current status:

```text
dataset in
validated task models
normalized check cases out
summary counts printed
```

No generated-code execution is performed yet.

## Legacy command

The older placeholder CLI path is still preserved:

`python3 main.py --file dataset.json`

This path remains available for stability while the preferred runner path is developed.

## Failure categories

```text
SCHEMA_INVALID
BASELINE_FAIL
SPEC_DRIFT
PERTURBATION_BRITTLE
EDGE_CASE_FAIL
TRAJECTORY_INCONSISTENT
OVERFIT_TO_TESTS
ROBUST
INCONCLUSIVE
```

## Next step

Build `aggregator.py` so normalized checks can be rendered as a readable summary table/report.
