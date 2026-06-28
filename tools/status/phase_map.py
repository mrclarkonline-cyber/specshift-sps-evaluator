#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

WORKPLAN = Path("memory_layer/wiki/operator_memory/workstation_command_center/workstation_command_center_upgrade_workplan.json")
ACTIVE = Path("memory_layer/wiki/operator_memory/active_workplan.json")
OUT_DIR = Path("memory_layer/wiki/operator_memory/workstation_command_center")
STATE = OUT_DIR / "phase_map_state.json"

ICONS = {
    "complete": "✅",
    "partial": "🟡",
    "registered": "🟡",
    "in_progress": "🎯",
    "active": "🎯",
    "parked": "💤",
    "protected": "🔒",
    "caution": "⚠️",
    "held": "⚠️",
    "unknown": "❔",
}

def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def icon_for(phase: dict, active_phase: str) -> str:
    phase_name = phase.get("phase", "")
    status = phase.get("status", "registered")
    if phase_name == active_phase:
        return ICONS["active"]
    return ICONS.get(status, ICONS["unknown"])

def main() -> int:
    now = datetime.now(timezone.utc).isoformat()
    workplan = load_json(WORKPLAN)
    active = load_json(ACTIVE)

    phases = workplan.get("upgrade_phases", [])
    active_phase = active.get("active_phase", "")
    active_workplan = active.get("active_workplan", "")

    records = []
    completed = 0

    print("SpecShift Visual Phase Map")
    print("=" * 72)
    print(f"generated_at_utc: {now}")
    print(f"active_workplan: {active_workplan}")
    print()

    if not phases:
        print("No phases found.")
        progress = 0.0
    else:
        print("Command Center phases:")
        for item in phases:
            phase_name = item.get("phase", "unknown")
            upgrade = item.get("upgrade", "unknown")
            command = item.get("command_target", "")
            status = item.get("status", "registered")
            icon = icon_for(item, active_phase)

            if status == "complete":
                completed += 1

            print(f"  {icon} {phase_name}")
            print(f"      upgrade: {upgrade}")
            print(f"      command: {command}")
            print(f"      status:  {'active' if phase_name == active_phase else status}")

            if item.get("artifact"):
                print(f"      artifact: {item.get('artifact')}")
            print()

            records.append({
                "phase": phase_name,
                "upgrade": upgrade,
                "command_target": command,
                "status": "active" if phase_name == active_phase else status,
                "icon": icon,
                "artifact": item.get("artifact", ""),
                "boundary": item.get("boundary", ""),
            })

        progress = round((completed / len(phases)) * 100, 1)

    state = {
        "engine": "phase_map_v1",
        "created_at_utc": now,
        "active_workplan": active_workplan,
        "active_phase": active_phase,
        "completed_phases": completed,
        "total_phases": len(phases),
        "progress_percent": progress,
        "phase_records": records,
        "claim_boundary": "Phase Map is a read-only local visualization of registered workplan state. It does not execute commands, alter state, route externally, monitor production, or resolve truth."
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"Completed phases: {completed}/{len(phases)}")
    print(f"Overall Phase Map reflected progress: {progress:.1f}%")
    print()
    print("Legend: ✅ complete | 🟡 registered/partial | 🎯 active | 🔒 protected | ⚠️ caution/held | 💤 parked")
    print()
    print("Boundary: read-only local visualization. wiki_landing owns fireworks.")
    print(f"State: {STATE}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
