#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone

ACTIVE = Path("memory_layer/wiki/operator_memory/active_workplan.json")
WORKPLAN = Path("memory_layer/wiki/operator_memory/workstation_command_center/workstation_command_center_upgrade_workplan.json")
KIRA_STATE = Path("memory_layer/wiki/operator_memory/workstation_command_center/kira_recommendation_state.json")
OUT = Path("memory_layer/wiki/operator_memory/workstation_command_center/phil_morale_state.json")

def run(cmd: list[str], timeout: int = 15) -> tuple[int, str]:
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)
    return proc.returncode, (proc.stdout + proc.stderr).strip()

def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def git_dirty() -> bool:
    code, output = run(["git", "status", "--short"])
    return code != 0 or bool(output.strip())

def write_state(payload: dict) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def main() -> int:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    active = load_json(ACTIVE)
    workplan = load_json(WORKPLAN)
    kira = load_json(KIRA_STATE)

    active_phase = active.get("active_phase", "unknown")
    next_action = active.get("next_action", "unknown")
    dirty = git_dirty()

    print("Phil Morale Layer")
    print("=" * 64)

    base = {
        "generated_at_utc": now,
        "engine": "phil_morale_layer_v1",
        "active_phase": active_phase,
        "next_serious_action": next_action,
        "claim_boundary": "Phil morale feedback is local human-friendly pacing only. It does not execute commands, override Kira, route externally, monitor production, validate truth, or authorize autonomous action."
    }

    if dirty:
        message = "No confetti while the tools are still on the floor."
        write_state({
            **base,
            "status": "held",
            "hold_reason": "git_dirty",
            "message": message,
        })
        print("Status: HELD")
        print(f"Phil says: {message}")
        print("Reason: Git is dirty. Serious checks come first.")
        print()
        print("Boundary: morale feedback only. No command execution or workflow authority.")
        return 0

    if not workplan:
        message = "I cannot riff on a missing workplan. That is how folders become weather."
        write_state({
            **base,
            "status": "held",
            "hold_reason": "missing_workplan",
            "message": message,
        })
        print("Status: HELD")
        print(f"Phil says: {message}")
        print("Reason: command-center workplan registry missing.")
        print()
        print("Boundary: morale feedback only. No command execution or workflow authority.")
        return 0

    completed = sum(1 for item in workplan.get("upgrade_phases", []) if item.get("status") == "complete")
    total = len(workplan.get("upgrade_phases", []))
    progress = round((completed / total) * 100, 1) if total else 0.0

    if kira and kira.get("severity") == "high":
        message = "Kira has the clipboard face. We listen to clipboard face."
        write_state({
            **base,
            "status": "held",
            "hold_reason": "kira_high_severity",
            "command_center_progress": progress,
            "message": message,
        })
        print("Status: HELD")
        print(f"Phil says: {message}")
        print(f"Reason: {kira.get('reason', 'Kira reported elevated severity.')}")
        print()
        print("Boundary: morale feedback only. No command execution or workflow authority.")
        return 0

    message = "Bridge crew update: the dashboard works, Kira has a clipboard, and the folder problem is losing structural integrity."

    write_state({
        **base,
        "status": "pass",
        "command_center_progress": progress,
        "message": message,
    })

    print("Status: PASS")
    print(f"generated_at_utc: {now}")
    print(f"active_phase: {active_phase}")
    print(f"command_center_progress: {progress:.1f}%")
    print()
    print(f"Phil says: {message}")
    print("Phil adds: Proceed, but do not romance the terminal. The terminal is a tool. A very dramatic tool.")
    print()
    print(f"Next serious action: {next_action}")
    print()
    print("Boundary: morale feedback only. No command execution, no workflow authority, no autonomous action, no truth resolution.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
