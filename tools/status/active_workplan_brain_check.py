#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ACTIVE = Path("memory_layer/wiki/operator_memory/active_workplan.json")
SCHEMA = Path("memory_layer/wiki/operator_memory/workstation_command_center/active_workplan_brain_schema_v1.json")

def main() -> int:
    print("Active Workplan Brain check")
    print("=" * 56)
    print()

    if not ACTIVE.exists():
        print("Status: HELD")
        print(f"Missing active workplan: {ACTIVE}")
        print()
        print("Overall Active Workplan Brain score: 0.0%")
        return 1

    active = json.loads(ACTIVE.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8")) if SCHEMA.exists() else {}

    required = schema.get("required_fields", [
        "active_workplan",
        "active_phase",
        "active_tracker",
        "next_action",
        "blockers",
        "closure_rule",
        "risk_state",
        "parked_state",
    ])

    problems = []

    for field in required:
        if field not in active:
            problems.append(f"missing_field:{field}")

    tracker = active.get("active_tracker", "")
    if not tracker or not Path(tracker).exists():
        problems.append("active_tracker_missing_or_not_found")

    if active.get("canonical_landing_command") != "wiki_landing":
        problems.append("canonical_landing_command_not_wiki_landing")

    blockers = active.get("blockers", [])
    if not isinstance(blockers, list):
        problems.append("blockers_not_list")

    risk_state = active.get("risk_state", {})
    if not isinstance(risk_state, dict):
        problems.append("risk_state_not_object")

    parked_state = active.get("parked_state", {})
    if not isinstance(parked_state, dict):
        problems.append("parked_state_not_object")

    forbidden = active.get("forbidden_actions", [])
    if not any("custom fireworks" in str(item).lower() for item in forbidden):
        problems.append("missing_custom_fireworks_forbidden_rule")

    if not any("hardcoded phase" in str(item).lower() for item in forbidden):
        problems.append("missing_hardcoded_phase_forbidden_rule")

    status = "PASS" if not problems else "HELD"
    score = 100.0 if not problems else 60.0

    print(f"Status: {status}")
    print(f"active_workplan: {active.get('active_workplan', 'unknown')}")
    print(f"active_phase:    {active.get('active_phase', 'unknown')}")
    print(f"active_tracker:  {tracker}")
    print(f"next_action:     {active.get('next_action', 'unknown')}")
    print(f"blockers:        {', '.join(blockers) if blockers else 'none'}")
    print()

    if problems:
        print("Problems:")
        for problem in problems:
            print(f"  - {problem}")
    else:
        print("Problems: none")

    print()
    print(f"Overall Active Workplan Brain score: {score:.1f}%")
    print()
    print("Boundary: active_workplan.json is local workflow state only.")
    print("No autonomous action, production monitoring, external routing, surveillance, targeting, or truth resolution claimed.")

    return 0 if not problems else 1

if __name__ == "__main__":
    raise SystemExit(main())
