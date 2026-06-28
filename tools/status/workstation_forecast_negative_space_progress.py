#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("memory_layer/wiki/operator_memory/workstation_next_workplans")
REG = ROOT / "workstation_forecast_negative_space_engine_workplan.json"
QUEUE = ROOT / "next_workplan_queue.json"
ACTIVE = Path("memory_layer/wiki/operator_memory/active_workplan.json")

print("Workstation Forecast + Negative-Space Engine status")
print("=" * 72)
print()

active = json.loads(ACTIVE.read_text(encoding="utf-8")) if ACTIVE.exists() else {}
active_phase = active.get("active_phase", "")
next_action = active.get("next_action", "")

if not REG.exists():
    print("Registration: MISSING")
    progress = 0.0
else:
    data = json.loads(REG.read_text(encoding="utf-8"))
    phases = data.get("candidate_phases", [])
    completed = sum(1 for p in phases if p.get("status") == "complete")
    total = len(phases)

    print("Registration: FOUND")
    print(f"    status: {data.get('status')}")
    print(f"    purpose: {data.get('purpose')}")
    print()

    print("Forecast workplan phases:")
    for item in phases:
        phase = item.get("phase", "unknown")
        goal = item.get("goal", "")
        status = item.get("status", "registered")
        if phase == active_phase:
            icon = "🎯"
        elif status == "complete":
            icon = "✅"
        else:
            icon = "🟡"
        print(f"    {icon} {phase}: {goal}")

    progress = round((completed / total) * 100, 1) if total else 0.0

print()
print(f"Current active phase: {active_phase or 'unknown'}")
print(f"Next action: {next_action or 'unknown'}")

if QUEUE.exists():
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    print(f"Queued after this: {', '.join(queue.get('queued_after_next', [])) or 'none'}")

print()
print(f"Overall Forecast Engine progress score: {progress:.1f}%")
print()
print("Boundary: Forecast + Negative-Space Engine creates review candidates only.")
print("No prediction, alerting, production monitoring, causal certainty, autonomous action, or truth resolution claimed.")
