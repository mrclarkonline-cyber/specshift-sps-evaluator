#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

REG = Path("memory_layer/wiki/operator_memory/workstation_command_center/workstation_command_center_upgrade_workplan.json")
ACTIVE = Path("memory_layer/wiki/operator_memory/active_workplan.json")

print("Workstation Command Center upgrade status")
print("=" * 64)
print()

if not REG.exists():
    print("Registration: MISSING")
    progress = 0.0
else:
    data = json.loads(REG.read_text(encoding="utf-8"))
    phases = data.get("upgrade_phases", [])
    print("Registration: FOUND")
    print(f"    status: {data.get('status')}")
    print(f"    purpose: {data.get('purpose')}")
    print()

    active_data = json.loads(ACTIVE.read_text(encoding="utf-8")) if ACTIVE.exists() else {}
    active_phase = active_data.get("active_phase", "")

    completed = 0
    total = len(phases)

    print("Upgrade map:")
    for item in phases:
        phase = item.get("phase", "")
        upgrade = item.get("upgrade", "")
        command = item.get("command_target", "")
        icon = "🎯" if phase == active_phase else "🟡"
        print(f"    {icon} {phase}: {upgrade} [{command}]")

    progress = 10.0 if total else 0.0
    print()
    print(f"Current active phase: {active_phase or 'unknown'}")
    print(f"Next action: {active_data.get('next_action', 'unknown')}")

print()
print(f"Overall Command Center progress score: {progress:.1f}%")
print()
print("Boundary: Command Center upgrades organize local workflow only.")
print("No autonomous action, production monitoring, external routing, surveillance, targeting, or truth resolution claimed.")
