"""Runner module for SpecShift.

Loads evaluator tasks, normalizes all check cases, and prints a simple summary.
This does not execute generated code.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from pydantic import ValidationError

from perturbations import normalise_task_checks
from aggregator import build_aggregation
from schema import EvaluatorInput, NormalisedCheck, TaskAggregation


def load_dataset(file_path: Path) -> list[EvaluatorInput]:
    """Load dataset.json into validated EvaluatorInput objects."""
    with file_path.open("r", encoding="utf-8") as handle:
        raw_data = json.load(handle)

    raw_tasks = (
        raw_data["tasks"]
        if isinstance(raw_data, dict) and "tasks" in raw_data
        else raw_data
    )

    if not isinstance(raw_tasks, list):
        raise ValueError(
            "Dataset must be a JSON list or an object with a 'tasks' list."
        )

    return [EvaluatorInput.model_validate(task) for task in raw_tasks]


def build_check_cases(tasks: list[EvaluatorInput]) -> list[NormalisedCheck]:
    """Normalize all task checks into one flat list."""
    checks: list[NormalisedCheck] = []

    for task in tasks:
        checks.extend(normalise_task_checks(task))

    return checks


def aggregate_stats(tasks: list[EvaluatorInput]) -> list[TaskAggregation]:
    stats: list[TaskAggregation] = []

    for task in tasks:
        stats.append(build_aggregation(task))

    return stats


def summarize_checks(checks: list[NormalisedCheck]) -> Counter:
    """Count normalized checks by check type."""
    return Counter(check.check_type for check in checks)


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize SpecShift dataset checks and print summary counts."
    )
    parser.add_argument("--file", required=True, type=Path)
    parser.add_argument(
        "--stats-out",
        type=Path,
        default=Path("artifacts/aggregated_stats.json"),
        help="Path to write aggregated per-task stats as JSON.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        tasks = load_dataset(args.file)
        checks = build_check_cases(tasks)
        stats = aggregate_stats(tasks)
    except FileNotFoundError:
        raise SystemExit(f"Dataset file not found: {args.file}") from None
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {args.file}: {exc}") from None
    except (ValidationError, ValueError) as exc:
        raise SystemExit(f"Dataset validation failed: {exc}") from None

    print_summary(tasks, checks, stats)
    save_aggregated_stats(stats, args.stats_out)
    print(f"\nSaved aggregated stats to: {args.stats_out}")


if __name__ == "__main__":
    main()
