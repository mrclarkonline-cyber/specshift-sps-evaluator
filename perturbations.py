"""Perturbation module for SpecShift.

This file is reserved for generating and applying simple spec perturbations and
adversarial variants for sprint-safe evaluation tasks.
"""

from schema import EvaluatorInput, NormalisedCheck


def normalise_task_checks(task: EvaluatorInput) -> list[NormalisedCheck]:
    checks = []

    shared_fields = {
        "task_id": task.task_id,
        "title": task.title,
        "expected_failure_type": task.expected_failure_type,
        "judge_note": task.judge_note,
    }

    for entry in task.baseline_tests:
        checks.append(
            NormalisedCheck(
                **shared_fields,
                check_type="baseline",
                input=entry.get("input"),
                expected_contains=entry.get("expected_contains"),
                expected=entry.get("expected"),
                source_field="baseline_tests",
            )
        )

    for entry in task.spec_perturbations:
        checks.append(
            NormalisedCheck(
                **shared_fields,
                check_type="spec_perturbation",
                variation=entry.get("variation"),
                source_field="spec_perturbations",
            )
        )

    for entry in task.adversarial_tests:
        checks.append(
            NormalisedCheck(
                **shared_fields,
                check_type="adversarial",
                input=entry.get("input"),
                expected=entry.get("expected"),
                source_field="adversarial_tests",
            )
        )

    if task.schema_expectation:
        checks.append(
            NormalisedCheck(
                **shared_fields,
                check_type="schema",
                schema_expectation=task.schema_expectation,
                source_field="schema_expectation",
            )
        )

    return checks
