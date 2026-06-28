#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from datetime import datetime, timezone

ACTIVE = Path("memory_layer/wiki/operator_memory/active_workplan.json")
WORKPLAN = Path("memory_layer/wiki/operator_memory/workstation_command_center/workstation_command_center_upgrade_workplan.json")

def run(cmd: list[str], timeout: int = 15) -> tuple[int, str]:
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)
    return proc.returncode, (proc.stdout + proc.stderr).strip()

def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def tracker_percent(tracker: str) -> float | None:
    if not tracker or not Path(tracker).exists():
        return None
    code, output = run(["python3", tracker], timeout=20)
    if code != 0:
        return None
    match = re.search(r"Overall .*?progress score:\s+([0-9.]+)%", output)
    if not match:
        return None
    return float(match.group(1))

def git_dirty() -> bool:
    code, output = run(["git", "status", "--short"])
    return code != 0 or bool(output.strip())

def main() -> int:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    active = load_json(ACTIVE)
    workplan = load_json(WORKPLAN)

    active_workplan = active.get("active_workplan", "unknown")
    active_phase = active.get("active_phase", "unknown")
    tracker = active.get("active_tracker", "")
    next_action = active.get("next_action", "")
    blockers = active.get("blockers", [])
    risk_state = active.get("risk_state", {})
    percent = tracker_percent(tracker)
    dirty = git_dirty()

    recommendation = ""
    reason = ""
    severity = "normal"

    if dirty:
        recommendation = "Git is dirty. Finish the current file changes, then commit, park, or restore before claiming a clean landing."
        reason = "Dirty Git blocks fireworks and makes state ambiguous."
        severity = "high"
    elif blockers:
        recommendation = "Resolve or park the listed blockers before continuing the active phase."
        reason = "The active workplan brain lists blockers."
        severity = "high"
    elif risk_state.get("claim_risk") in {"medium", "high"} or risk_state.get("boundary_risk") in {"medium", "high"}:
        recommendation = "Run the claim-overstatement detector before continuing."
        reason = "The active workplan brain reports elevated claim or boundary risk."
        severity = "high"
    elif percent is not None and percent >= 100.0:
        recommendation = "This workplan is complete. Close or park this work block before starting the next named phase."
        reason = "The active tracker reports 100 percent completion."
        severity = "normal"
    elif active_phase == "phase_19_kira_recommendation_engine":
        recommendation = "Complete Phase 19 by wiring Kira recommendations to active_workplan.json, Git state, progress score, blockers, and claim-risk state."
        reason = "Phase 19 is the active command-center upgrade."
        severity = "normal"
    elif next_action:
        recommendation = f"Next action: {next_action}"
        reason = "The active workplan brain provided a next action."
        severity = "normal"
    else:
        recommendation = "No next action is registered. Update active_workplan.json before proceeding."
        reason = "Missing next_action creates guessing."
        severity = "medium"

    output = {
        "generated_at_utc": now,
        "engine": "kira_recommendation_engine_v1",
        "active_workplan": active_workplan,
        "active_phase": active_phase,
        "active_tracker": tracker,
        "progress_percent": percent,
        "git_dirty": dirty,
        "blockers": blockers,
        "risk_state": risk_state,
        "severity": severity,
        "recommendation": recommendation,
        "reason": reason,
        "claim_boundary": "Kira recommendations are local workflow guidance only. They do not execute commands, route externally, monitor production, validate truth, or authorize autonomous action."
    }

    print("Kira Recommendation Engine")
    print("=" * 64)
    print(f"active_workplan: {active_workplan}")
    print(f"active_phase:    {active_phase}")
    print(f"progress:        {percent if percent is not None else 'unknown'}")
    print(f"git_dirty:       {dirty}")
    print(f"severity:        {severity}")
    print()
    print(f"Kira recommends: {recommendation}")
    print(f"Reason: {reason}")
    print()
    print("Boundary: local workflow guidance only. No autonomous action or truth resolution.")

    out_dir = Path("memory_layer/wiki/operator_memory/workstation_command_center")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "kira_recommendation_state.json"
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
