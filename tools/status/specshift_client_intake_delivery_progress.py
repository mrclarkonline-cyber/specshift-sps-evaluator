#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("memory_layer/wiki/operator_memory/workstation_next_workplans")
REG = ROOT / "specshift_client_intake_delivery_system_workplan.json"
ACTIVE = Path("memory_layer/wiki/operator_memory/active_workplan.json")

print("SpecShift Client Intake + Delivery System status")
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

    print("Client intake/delivery phases:")
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
    if completed == 0 and total:
        progress = 10.0

print()
print(f"Current active phase: {active_phase or 'unknown'}")
print(f"Next action: {next_action or 'unknown'}")
print()
print(f"Overall Client Intake progress score: {progress:.1f}%")
print()
print("Boundary: Client Intake + Delivery System is a workflow scaffold only.")
print("No legal advice, financial advice, binding contract terms, compliance certification, production monitoring, or truth validation claimed.")
