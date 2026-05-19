"""Core data schemas for the SpecShift evaluator pipeline."""

from __future__ import annotations

from pydantic import BaseModel, ValidationError
from typing import Any, Literal, TypedDict, Optional

FailureType = Literal[
    "SCHEMA_INVALID",
    "BASELINE_FAIL",
    "SPEC_DRIFT",
    "PERTURBATION_BRITTLE",
    "EDGE_CASE_FAIL",
    "TRAJECTORY_INCONSISTENT",
    "OVERFIT_TO_TESTS",
    "ROBUST",
    "INCONCLUSIVE",
]


class EvaluatorInput(BaseModel):
    task_id: str
    title: str
    original_spec: str
    generated_code: str
    baseline_tests: list[dict[str, Any]]
    schema_expectation: str
    spec_perturbations: list[dict[str, Any]]
    adversarial_tests: list[dict[str, Any]]
    expected_failure_type: FailureType
    judge_note: str


class EvaluatorOutput(BaseModel):
    baseline_passed: bool = False
    schema_passed: bool = False
    perturbation_passed: bool = False
    adversarial_passed: bool = False
    failure_type: FailureType = "INCONCLUSIVE"
    short_explanation: str = ""
    overall_verdict: str = "inconclusive"


class GraphState(TypedDict):
    input_data: EvaluatorInput
    output_data: EvaluatorOutput


class NormalisedCheck(BaseModel):
    task_id: str
    title: str
    check_type: Literal["baseline", "spec_perturbation", "adversarial", "schema"]
    schema_expectation: Optional[str] = None
    input: Optional[list] = None
    expected: Optional[Any] = None
    expected_contains: Optional[str] = None
    variation: Optional[str] = None
    expected_failure_type: str
    judge_note: str
    source_field: Literal[
        "baseline_tests",
        "spec_perturbations",
        "adversarial_tests",
        "schema_expectation",
    ]
