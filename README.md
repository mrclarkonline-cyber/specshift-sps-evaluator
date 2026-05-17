# SpecShift: Sprint-Safe Evaluator Harness

SpecShift is a small local evaluator harness for the Secure Program Synthesis sprint.

Core claim:

Passing visible tests is not enough for secure program synthesis. Perturbation-aware spec validation can catch brittle apparent success.

## What it does

The harness reads dataset.json, validates each task with Pydantic, runs each task through a placeholder LangGraph workflow, and prints one readable report per task.

Current workflow:

1. Ingest task and baseline tests
2. Validate schema expectation
3. Run spec perturbation checks
4. Run adversarial cases
5. Generate readable report

## Current scope

This is a sprint-safe prototype. It does not execute generated code yet. The first milestone is a clean end-to-end path:

- dataset in
- schema validation
- routed placeholder verdict
- readable report out

## Run

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py --file dataset.json

## Failure categories

- SCHEMA_INVALID
- BASELINE_FAIL
- SPEC_DRIFT
- PERTURBATION_BRITTLE
- EDGE_CASE_FAIL
- TRAJECTORY_INCONSISTENT
- OVERFIT_TO_TESTS
- ROBUST
- INCONCLUSIVE

## Notes

This project is intentionally small and judge-readable. It is a public-safe sprint prototype, not a full evaluator product.
