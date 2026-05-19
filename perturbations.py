"""Perturbation module for SpecShift.

This file is reserved for generating and applying simple spec perturbations and
adversarial variants for sprint-safe evaluation tasks.
"""

from typing import Literal, Any
from pydantic import BaseModel
from main import EvaluatorInput

class NormalisedCheck(BaseModel):
    task_id: str
    title: str
    original_spec: str
    generated_code: str
    check_type: Literal['baseline', 'spec_perturbation', 'adversarial']
    schema_expectation: str
    input: Any | None
    expected: Any | None
    variation: str | None
    expected_failure_type: str | None # not check level but still adds context, keep?
    judge_note: str | None
    source_field: Literal['baseline_tests', 'spec_perturbations', 'adversarial_tests']

def normalise_task_checks(task: EvaluatorInput) -> list[NormalisedCheck]:
    checks = []

    shared_fields = {
        "task_id": task.task_id,
        "title": task.title,
        "original_spec": task.original_spec,
        "generated_code": task.generated_code,
        "schema_expectation": task.schema_expectation,
        "expected_failure_type": task.expected_failure_type,
        "judge_note": task.judge_note,
    }

    for entry in task.baseline_tests:
        checks.append(NormalisedCheck(
            **shared_fields,
            check_type = 'baseline',
            input = entry.get('input'),
            expected = entry.get('expected'),
            variation = None,
            source_field = 'baseline_tests'
        ))

    for entry in task.spec_perturbations:
        checks.append(NormalisedCheck(
            **shared_fields,
            check_type = 'spec_perturbation',
            input = None,
            expected = None,
            variation = entry.get('variation'),
            source_field = 'spec_perturbations'
        ))

    for entry in task.adversarial_tests:
        checks.append(NormalisedCheck(
            **shared_fields,
            check_type = 'adversarial',
            input = entry.get('input'),
            expected = entry.get('expected'),
            variation = None,
            source_field = 'adversarial_tests'
        ))

    return checks