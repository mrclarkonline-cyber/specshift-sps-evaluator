from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from schema import EvaluatorInput, NormalisedCheck, TaskAggregation


def summarize_stats(stats: list[TaskAggregation]) -> Counter:
    """Count aggregated checks from per-task stats."""
    totals = Counter()

    for stat in stats:
        totals["baseline"] += stat.baseline_count
        totals["schema"] += stat.schema_count
        totals["spec_perturbation"] += stat.spec_perturbation_count
        totals["adversarial"] += stat.adversarial_count

    return totals


def save_aggregated_stats(stats: list[TaskAggregation], output_path: Path) -> None:
    """Persist per-task aggregated stats to a JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = [stat.model_dump() for stat in stats]
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def print_summary(
    tasks: list[EvaluatorInput],
    checks: list[NormalisedCheck],
    stats: list[TaskAggregation],
) -> None:
    """Print a judge-readable summary."""
    counts = summarize_stats(stats)
    divider = "-" * 88

    print("=== SpecShift Runner Summary ===")
    print(f"Loaded {len(tasks)} tasks")
    print(f"Generated {len(checks)} check cases")
    print(divider)

    for check_type in ["baseline", "schema", "spec_perturbation", "adversarial"]:
        print(f"{check_type}: {counts.get(check_type, 0)}")

    print("\n=== Per-Task Aggregation ===")
    print(divider)
    for stat in stats:
        print(f"[{stat.task_id}] {stat.title}")
        print(f"  expected failure : {stat.expected_failure_type}")
        print(
            "  checks           : "
            f"baseline {stat.baseline_count} | "
            f"schema {stat.schema_count} | "
            f"spec {stat.spec_perturbation_count} | "
            f"adversarial {stat.adversarial_count} | "
            f"total {stat.total_checks}"
        )
        print(f"  judge note       : {stat.judge_note}")
        print(divider)
