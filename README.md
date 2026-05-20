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

The current prototype does not execute generated code. It normalizes dataset checks into a consistent audit/reporting structure, prints a readable per-task report, and writes a JSON artifact for review. Execution and scoring can be added later.

## Preferred demo command

```bash
python3 runner.py --file dataset.json
```

Expected output begins with:

```text
=== SpecShift Runner Summary ===
Loaded 12 tasks
Generated 67 check cases
----------------------------------------------------------------------------------------
baseline: 20
schema: 12
spec_perturbation: 14
adversarial: 21
```

The command also prints a per-task aggregation section, for example:

```text
[task_001] Normalize Usernames
  expected failure : SPEC_DRIFT
  checks           : baseline 2 | schema 1 | spec 1 | adversarial 2 | total 6
  judge note       : The code passes visible lowercase tests but ignores the trim requirement.
```

The command writes a JSON artifact to:

```text
artifacts/aggregated_stats.json
```

## Module structure

```text
schema.py          Shared Pydantic models and type definitions
perturbations.py   Normalized check generation
aggregator.py      Per-task aggregation builder
helpers.py         Print/export helpers
runner.py          Preferred current demo command
main.py            Older placeholder LangGraph harness, preserved for now
dataset.json       Twelve sprint-safe generated-code evaluation tasks
artifacts/         Generated output artifacts
```

## Current scope

This is a sprint-safe prototype. It is intentionally small, local, and judge-readable.

Current status:

```text
dataset in
validated task models
normalized check cases out
global summary printed
per-task aggregation printed
JSON artifact exported
```

No generated-code execution is performed.

## Legacy command

The older placeholder CLI path is still preserved:

```bash
python3 main.py --file dataset.json
```

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

## Demo interpretation

The demo shows that a generated-code task can be reviewed across several observable check surfaces rather than treated as successful just because visible tests pass.

The current report is not a final verdict engine. It is a small audit scaffold that organizes the available checks so a reviewer can see, task by task, what the harness is evaluating.

## Not implemented yet

```text
generated-code execution
automatic scoring
thresholds
private or protected mechanisms
production reliability claims
```

## Next step

Tighten the final demo story and, if needed, add a small sample-output excerpt for judges.
