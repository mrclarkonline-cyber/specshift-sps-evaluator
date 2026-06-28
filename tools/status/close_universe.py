#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ACTIVE = Path("memory_layer/wiki/operator_memory/active_workplan.json")
WORKPLAN = Path("memory_layer/wiki/operator_memory/workstation_command_center/workstation_command_center_upgrade_workplan.json")
OUT_DIR = Path("memory_layer/wiki/operator_memory/workstation_command_center")
SHUTDOWN_STATE = OUT_DIR / "close_universe_state.json"
SHUTDOWN_LOG = OUT_DIR / "close_universe_log.jsonl"

def run(cmd: list[str], timeout: int = 20) -> tuple[int, str]:
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)
    return proc.returncode, (proc.stdout + proc.stderr).strip()

def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def git_status() -> tuple[bool, str]:
    code, output = run(["git", "status", "--short"])
    return code != 0 or bool(output.strip()), output

def latest_commit() -> str:
    code, output = run(["git", "log", "-1", "--pretty=%h %s"])
    return output if code == 0 and output else "unknown"

def main() -> int:
    now = datetime.now(timezone.utc).isoformat()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    active = load_json(ACTIVE)
    workplan = load_json(WORKPLAN)
    dirty, dirty_text = git_status()

    phases = workplan.get("upgrade_phases", [])
    completed = [p for p in phases if p.get("status") == "complete"]
    parked = [p for p in phases if p.get("status") == "parked"]
    active_phase = active.get("active_phase", "unknown")
    next_action = active.get("next_action", "unknown")
    tomorrow_first_task = next_action

    status = "held_dirty_git" if dirty else "shutdown_summary_created"

    state = {
        "engine": "close_universe_v1",
        "status": status,
        "created_at_utc": now,
        "active_workplan": active.get("active_workplan", "unknown"),
        "active_phase": active_phase,
        "latest_commit": latest_commit(),
        "git_dirty": dirty,
        "git_status": dirty_text,
        "completed_phase_count": len(completed),
        "total_phase_count": len(phases),
        "completed_phases": [p.get("phase") for p in completed],
        "parked_phases": [p.get("phase") for p in parked],
        "tomorrow_first_task": tomorrow_first_task,
        "shutdown_rule": "Stop work after this summary unless the user explicitly resumes. Completed repo/wiki work still ends with wiki_landing.",
        "claim_boundary": "close_universe is a local shutdown summary only. It does not lock the OS, execute autonomous actions, route externally, monitor production, or resolve truth."
    }

    SHUTDOWN_STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with SHUTDOWN_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(state, ensure_ascii=False, sort_keys=True) + "\n")

    print("Close Universe")
    print("=" * 64)
    print(f"Status: {status}")
    print(f"Active workplan: {state['active_workplan']}")
    print(f"Active phase: {active_phase}")
    print(f"Latest commit: {state['latest_commit']}")
    print(f"Git dirty: {dirty}")
    print()
    print("Landed today / completed in this workplan:")
    for phase in state["completed_phases"][-8:]:
        print(f"  - {phase}")
    print()
    print("Parked work:")
    if state["parked_phases"]:
        for phase in state["parked_phases"]:
            print(f"  - {phase}")
    else:
        print("  - none")
    print()
    print(f"Tomorrow's first task: {tomorrow_first_task}")
    print()
    if dirty:
        print("Kira: Git is dirty. No shutdown fireworks until the floor is clean.")
        print("Phil: The universe is ajar. Not closed. Ajar.")
    else:
        print("Kira: Work block summarized. Stop cleanly or proceed only by explicit choice.")
        print("Phil: Universe lid placed gently on top. No tools left in Eleanor's driveway.")
    print()
    print(f"State: {SHUTDOWN_STATE}")
    print(f"Log:   {SHUTDOWN_LOG}")
    print()
    print("Boundary: local shutdown summary only. wiki_landing owns fireworks.")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
