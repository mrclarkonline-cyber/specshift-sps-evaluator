"""Perturbation module for SpecShift.

This file is reserved for generating and applying simple spec perturbations and
adversarial variants for sprint-safe evaluation tasks.
"""

from typing import Literal, Any, Optional
from pydantic import BaseModel
from main import EvaluatorInput

class NormalisedCheck(BaseModel):
    task_id: str
    title: str
    check_type: Literal['baseline', 'spec_perturbation', 'adversarial', 'schema']
    schema_expectation: Optional[str] = None
    input: Optional[list] = None
    expected: Optional[Any] = None
    expected_contains: Optional[str] = None
    variation: Optional[str] = None
    expected_failure_type: str
    judge_note: str
    source_field: Literal['baseline_tests', 'spec_perturbations', 'adversarial_tests', 'schema_expectation']

def normalise_task_checks(task: EvaluatorInput) -> list[NormalisedCheck]:
    checks = []

    shared_fields = {
        "task_id": task.task_id,
        "title": task.title,
        "expected_failure_type": task.expected_failure_type,
        "judge_note": task.judge_note,
    }

    for entry in task.baseline_tests:
        checks.append(NormalisedCheck(
            **shared_fields,
            check_type = 'baseline',
            input = entry.get('input'),
            expected_contains = entry.get('expected_contains'),
            expected = entry.get('expected'),
            source_field = 'baseline_tests'
        ))

    for entry in task.spec_perturbations:
        checks.append(NormalisedCheck(
            **shared_fields,
            check_type = 'spec_perturbation',
            variation = entry.get('variation'),
            source_field = 'spec_perturbations'
        ))

    for entry in task.adversarial_tests:
        checks.append(NormalisedCheck(
            **shared_fields,
            check_type = 'adversarial',
            input = entry.get('input'),
            expected = entry.get('expected'),
            source_field = 'adversarial_tests'
        ))

    if task.schema_expectation:
        checks.append(NormalisedCheck(
            **shared_fields,
            check_type = 'schema',
            schema_expectation = task.schema_expectation,
            source_field = 'schema_expectation'
        ))

    return checks