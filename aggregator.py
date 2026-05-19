"""Aggregator module for SpecShift.

This file is reserved for collecting task results and producing readable summary
reports for judges.
"""

from schema import EvaluatorInput, TaskAggregation


def build_aggregation(task: EvaluatorInput) -> TaskAggregation:

    baseline_count = len(task.baseline_tests)
    schema_count = 1
    spec_perturbation_count = len(task.spec_perturbations)
    adversarial_count = len(task.adversarial_tests)
    total_checks = (
        baseline_count + schema_count + spec_perturbation_count + adversarial_count
    )

    fields = {
        "task_id": task.task_id,
        "title": task.title,
        "expected_failure_type": task.expected_failure_type,
        "judge_note": task.judge_note,
        "baseline_count": baseline_count,
        "schema_count": schema_count,
        "spec_perturbation_count": spec_perturbation_count,
        "adversarial_count": adversarial_count,
        "total_checks": total_checks,
    }

    return TaskAggregation(**fields)
