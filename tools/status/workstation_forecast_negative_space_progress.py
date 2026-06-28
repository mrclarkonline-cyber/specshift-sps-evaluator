#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("memory_layer/wiki/operator_memory/workstation_next_workplans")
REG = ROOT / "workstation_forecast_negative_space_engine_workplan.json"
QUEUE = ROOT / "next_workplan_queue.json"

print("Workstation Forecast + Negative-Space Engine status")
print("=" * 72)
print()

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
        icon = "✅" if status == "complete" else "🎯" if phase == "forecast_phase_1_scope_registration" else "🟡"
        print(f"    {icon} {phase}: {goal}")

    progress = 10.0 if total else 0.0
    if completed:
        progress = round((completed / total) * 100, 1)

print()
if QUEUE.exists():
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    print(f"Queued after this: {', '.join(queue.get('queued_after_next', [])) or 'none'}")

print()
print(f"Overall Forecast Engine progress score: {progress:.1f}%")
print()
print("Boundary: Forecast + Negative-Space Engine creates review candidates only.")
print("No prediction, alerting, production monitoring, causal certainty, autonomous action, or truth resolution claimed.")
