"""Runner module for SpecShift.

Loads evaluator tasks, normalizes all check cases, and prints a simple summary.
This does not execute generated code.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pydantic import ValidationError

from perturbations import normalise_task_checks
from aggregator import build_aggregation
from schema import EvaluatorInput, NormalisedCheck, TaskAggregation
from helpers import print_summary, save_aggregated_stats


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
