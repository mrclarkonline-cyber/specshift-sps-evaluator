"""SpecShift: sprint-safe evaluator harness."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Literal, TypedDict

from langgraph.graph import END, StateGraph
from pydantic import BaseModel, ValidationError


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


def node_ingest_and_baseline(state: GraphState) -> GraphState:
    task = state["input_data"]
    print(f"[{task.task_id}] Ingesting task and checking baseline tests...")
    return state


def node_validate_schema(state: GraphState) -> GraphState:
    task = state["input_data"]
    print(f"[{task.task_id}] Validating schema expectations...")
    return state


def node_run_perturbations(state: GraphState) -> GraphState:
    task = state["input_data"]
    print(f"[{task.task_id}] Running spec perturbation checks...")
    return state


def node_run_adversarial(state: GraphState) -> GraphState:
    task = state["input_data"]
    print(f"[{task.task_id}] Running adversarial cases...")
    return state


def node_generate_report(state: GraphState) -> GraphState:
    task = state["input_data"]
    print(f"[{task.task_id}] Compiling final evaluation report...")

    state["output_data"].failure_type = task.expected_failure_type
    state["output_data"].short_explanation = (
        "Placeholder evaluator completed all workflow nodes. "
        "Expected failure type and judge note are carried through for the first readable CLI pass. "
        "No executable checks have been implemented yet."
    )

    if task.expected_failure_type == "ROBUST":
        state["output_data"].overall_verdict = "robust"
    elif task.expected_failure_type == "INCONCLUSIVE":
        state["output_data"].overall_verdict = "inconclusive"
    else:
        state["output_data"].overall_verdict = "flagged"

    return state


def build_graph():
    workflow = StateGraph(GraphState)
    workflow.add_node("ingest_and_baseline", node_ingest_and_baseline)
    workflow.add_node("validate_schema", node_validate_schema)
    workflow.add_node("run_perturbations", node_run_perturbations)
    workflow.add_node("run_adversarial", node_run_adversarial)
    workflow.add_node("generate_report", node_generate_report)

    workflow.set_entry_point("ingest_and_baseline")
    workflow.add_edge("ingest_and_baseline", "validate_schema")
    workflow.add_edge("validate_schema", "run_perturbations")
    workflow.add_edge("run_perturbations", "run_adversarial")
    workflow.add_edge("run_adversarial", "generate_report")
    workflow.add_edge("generate_report", END)

    return workflow.compile()


def load_dataset(file_path: Path) -> list[EvaluatorInput]:
    with file_path.open("r", encoding="utf-8") as handle:
        raw_data = json.load(handle)

    raw_tasks = raw_data["tasks"] if isinstance(raw_data, dict) and "tasks" in raw_data else raw_data

    if not isinstance(raw_tasks, list):
        raise ValueError("Dataset must be a JSON list or an object with a 'tasks' list.")

    return [EvaluatorInput.model_validate(task) for task in raw_tasks]


def output_to_json(output: EvaluatorOutput) -> str:
    return output.model_dump_json(indent=2)


def evaluate_tasks(tasks: list[EvaluatorInput]) -> list[EvaluatorOutput]:
    app = build_graph()
    results = []

    for task in tasks:
        initial_state: GraphState = {
            "input_data": task,
            "output_data": EvaluatorOutput(),
        }
        final_state = app.invoke(initial_state)
        results.append(final_state["output_data"])

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the SpecShift evaluator harness on a JSON dataset."
    )
    parser.add_argument("--file", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        tasks = load_dataset(args.file)
    except FileNotFoundError:
        raise SystemExit(f"Dataset file not found: {args.file}") from None
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {args.file}: {exc}") from None
    except (ValidationError, ValueError) as exc:
        raise SystemExit(f"Dataset validation failed: {exc}") from None

    reports = evaluate_tasks(tasks)

    print("\n=== Final Evaluation Reports ===")
    for task, report in zip(tasks, reports):
        print(f"\nTask: {task.task_id} - {task.title}")
        print(f"Expected failure type: {task.expected_failure_type}")
        print(f"Judge note: {task.judge_note}")
        print(output_to_json(report))


if __name__ == "__main__":
    main()
