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
from schema import EvaluatorInput, NormalisedCheck


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
        raise ValueError("Dataset must be a JSON list or an object with a 'tasks' list.")

    return [EvaluatorInput.model_validate(task) for task in raw_tasks]


def build_check_cases(tasks: list[EvaluatorInput]) -> list[NormalisedCheck]:
    """Normalize all task checks into one flat list."""
    checks: list[NormalisedCheck] = []

    for task in tasks:
        checks.extend(normalise_task_checks(task))

    return checks


def summarize_checks(checks: list[NormalisedCheck]) -> Counter:
    """Count normalized checks by check type."""
    return Counter(check.check_type for check in checks)


def print_summary(tasks: list[EvaluatorInput], checks: list[NormalisedCheck]) -> None:
    """Print a judge-readable summary."""
    counts = summarize_checks(checks)

    print("=== SpecShift Runner Summary ===")
    print(f"Loaded {len(tasks)} tasks")
    print(f"Generated {len(checks)} check cases")
    print()

    for check_type in ["baseline", "schema", "spec_perturbation", "adversarial"]:
        print(f"{check_type}: {counts.get(check_type, 0)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize SpecShift dataset checks and print summary counts."
    )
    parser.add_argument("--file", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        tasks = load_dataset(args.file)
        checks = build_check_cases(tasks)
    except FileNotFoundError:
        raise SystemExit(f"Dataset file not found: {args.file}") from None
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {args.file}: {exc}") from None
    except (ValidationError, ValueError) as exc:
        raise SystemExit(f"Dataset validation failed: {exc}") from None

    print_summary(tasks, checks)


if __name__ == "__main__":
    main()
