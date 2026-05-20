# SpecShift SPS Evaluator



## Why this matters

Modern code-generation systems can pass visible example tests while still violating the intended specification. SpecShift demonstrates this gap using small synthetic tasks that expose schema violations, edge-case failures, perturbation brittleness, and trajectory inconsistencies.

This repository is intentionally designed as a lightweight, judge-readable evaluation scaffold rather than a production verifier. The goal is to make specification robustness failures observable, reproducible, and easy to inspect locally.

## What this is not

SpecShift is not a finished verifier, theorem prover, sandbox, or production security tool. It does not execute generated code, prove correctness, or claim that any implementation is safe. It is a public-safe scaffold for showing how visible-test success can miss important specification failures.

## Expected demo output

Run:

    python3 runner.py --file dataset.json

Expected summary:

- Loaded 12 synthetic tasks
- Generated 67 check cases
- baseline: 20
- schema: 12
- spec_perturbation: 14
- adversarial: 21

## Public-scope boundary

This repository is intentionally limited to public, synthetic examples. It does not include private scoring logic, protected methods, bidder materials, valuation language, or commercial negotiation strategy.


A Secure Program Synthesis sprint prototype for turning generated-code tasks into normalized audit checks across baseline tests, schema expectations, spec perturbations, and adversarial cases.

Core claim:

Visible test success is not the same as robust spec satisfaction.

## What it demonstrates

Many generated-code workflows treat passing visible tests as the main success signal. SpecShift separates that signal into several check types:

1. baseline tests
2. schema expectations
3. spec perturbations
4. adversarial cases

The current prototype takes a small synthetic dataset of generated-code tasks and normalizes each task’s baseline tests, schema expectations, spec perturbations, and adversarial cases into a consistent audit/reporting structure.

## Setup

Install the sprint dependencies first:

```bash
python3 -m pip install -r requirements.txt
```

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

## Dataset field description

Each item in dataset.json is one evaluation task with the following fields:

| Field | Type | Description |
|---|---|---|
| task_id | string | Unique identifier for the task (for example, task_001). |
| title | string | Human-readable task title shown in summaries. |
| original_spec | string | Natural-language requirement the generated code is supposed to satisfy. |
| generated_code | string | Code implementation being reviewed (stored as code text). |
| baseline_tests | list[object] | Basic visible checks used as initial behavior signal. |
| schema_expectation | string | Structural/shape expectation for function signature or output format. |
| spec_perturbations | list[object] | Requirement variations that stress robustness to spec shifts. |
| adversarial_tests | list[object] | Edge or stress checks designed to reveal brittle behavior. |
| expected_failure_type | Literal | Intended label for expected outcome category (for example, SPEC_DRIFT). |
| judge_note | string | Brief human explanation of why the expected label was chosen. |


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

## Two-minute demo

1. Run `python3 runner.py --file dataset.json`.
2. Confirm the runner loads 12 tasks and generates 67 check cases.
3. Read the global check counts.
4. Read the per-task aggregation blocks.
5. Notice that the report separates visible baseline tests from schema expectations, spec perturbations, and adversarial cases.

The point of the demo is not to prove final correctness. The point is to show a small, runnable scaffold for reviewing generated-code tasks beyond visible test success.

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

## Demo status

The current demo is ready for review as a small sprint prototype. Future work would add generated-code execution, automatic scoring, and richer discrepancy reporting.