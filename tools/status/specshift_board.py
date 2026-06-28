#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone

REPO = Path.cwd()
ACTIVE = Path("memory_layer/wiki/operator_memory/active_workplan.json")
WORKPLAN = Path("memory_layer/wiki/operator_memory/workstation_command_center/workstation_command_center_upgrade_workplan.json")

def run(cmd: list[str], timeout: int = 10) -> tuple[int, str]:
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)
    return proc.returncode, (proc.stdout + proc.stderr).strip()

def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def section(title: str) -> None:
    print()
    print(f"=== {title} ===")

def main() -> None:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    active = load_json(ACTIVE)
    workplan = load_json(WORKPLAN)

    print("SpecShift Mission Control")
    print("=" * 64)
    print(f"generated_at_utc: {now}")

    section("Active workplan")
    print(f"workplan:      {active.get('active_workplan', 'unknown')}")
    print(f"active phase:  {active.get('active_phase', 'unknown')}")
    print(f"tracker:       {active.get('active_tracker', 'unknown')}")
    print(f"next action:   {active.get('next_action', 'unknown')}")
    blockers = active.get("blockers", [])
    print(f"blockers:      {', '.join(blockers) if blockers else 'none'}")
    print(f"closure rule:  {active.get('closure_rule', 'unknown')}")

    section("Git")
    code, status = run(["git", "status", "--short"])
    print("status: clean" if code == 0 and not status else "status: dirty or unavailable")
    if status:
        print(status)

    code, commit = run(["git", "log", "-1", "--pretty=%h %s"])
    print(f"last commit: {commit if code == 0 and commit else 'unknown'}")

    section("Progress")
    tracker = active.get("active_tracker", "")
    if tracker and Path(tracker).exists():
        code, output = run(["python3", tracker], timeout=20)
        print(output if output else "tracker produced no output")
    else:
        print("active tracker missing")

    section("Kira engine")
    kira_script = Path("tools/status/kira_recommendation_engine.py")
    if kira_script.exists():
        code, kira_output = run(["python3", str(kira_script)], timeout=20)
        print(kira_output if kira_output else "Kira engine produced no output")
    else:
        print("Kira engine missing")

    section("Provenance Vault")
    provenance_report = Path("memory_layer/wiki/operator_memory/workstation_command_center/provenance_vault_report.json")
    if provenance_report.exists():
        data = load_json(provenance_report)
        print(f"status: {data.get('status', 'unknown')}")
        print(f"records created: {data.get('records_created', 'unknown')}")
        print(f"vault: {data.get('vault_artifact', 'unknown')}")
        print(f"report: {provenance_report}")
    else:
        print("Provenance Vault report missing")

    section("Close Universe")
    shutdown_state = Path("memory_layer/wiki/operator_memory/workstation_command_center/close_universe_state.json")
    if shutdown_state.exists():
        data = load_json(shutdown_state)
        print(f"status: {data.get('status', 'unknown')}")
        print(f"tomorrow first task: {data.get('tomorrow_first_task', 'unknown')}")
        print(f"state: {shutdown_state}")
    else:
        print("Close Universe state missing")

    section("Promotion Gate")
    promotion_report = Path("memory_layer/wiki/operator_memory/workstation_command_center/artifact_promotion_gate_report.json")
    if promotion_report.exists():
        data = load_json(promotion_report)
        print(f"status: {data.get('status', 'unknown')}")
        print(f"promotion allowed: {data.get('promotion_allowed', 'unknown')}")
        print(f"holds: {data.get('holds', 'unknown')}")
        print(f"reviews: {data.get('reviews', 'unknown')}")
        print(f"report: {promotion_report}")
    else:
        print("Promotion Gate report missing")

    section("Claim Gauntlet")
    claim_report = Path("memory_layer/wiki/operator_memory/workstation_command_center/claim_gauntlet_report.json")
    if claim_report.exists():
        data = load_json(claim_report)
        print(f"status: {data.get('status', 'unknown')}")
        print(f"risk level: {data.get('risk_level', 'unknown')}")
        print(f"actionable hits: {data.get('actionable_hits', 'unknown')}")
        print(f"report: {claim_report}")
    else:
        print("Claim Gauntlet report missing")

    section("Phil morale")
    phil_script = Path("tools/status/phil_morale_layer.py")
    if phil_script.exists():
        code, phil_output = run(["python3", str(phil_script)], timeout=20)
        print(phil_output if phil_output else "Phil morale layer produced no output")
    else:
        print("Phil morale layer missing")

    section("Open risks")
    risks = []
    if status:
        risks.append("dirty_git")
    if not tracker or not Path(tracker).exists():
        risks.append("missing_active_tracker")
    if not active.get("next_action"):
        risks.append("missing_next_action")
    if not workplan:
        risks.append("missing_command_center_workplan")
    print(", ".join(risks) if risks else "none detected")

    section("Boundary")
    print("Mission Control is read-only dashboarding.")
    print("No autonomous action, production monitoring, external routing, surveillance, targeting, or truth resolution claimed.")
    print()
    print("House rule: completed repo/wiki work still ends with wiki_landing.")

if __name__ == "__main__":
    main()
