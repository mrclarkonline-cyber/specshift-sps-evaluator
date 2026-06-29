#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

BOUNDARY = (
    "SpecShift systems integration survey only. It checks whether local tools, reports, "
    "workplan state, QA, security scans, and dependency records are present and connected. "
    "It does not create legal advice, financial advice, binding terms, compliance certification, "
    "production validation, automated verdict, free pilot commitment, autonomous client action, "
    "surveillance authorization, truth validation, or hidden-mechanism claim."
)

REQUIRED_FILES = {
    "qa_command": "tools/status/specshift_qa.py",
    "qa_tracker": "tools/status/specshift_qa_regression_progress.py",
    "security_doctor": "tools/status/specshift_security_doctor.py",
    "security_scan": "tools/status/specshift_security_scan.py",
    "path_watch": "tools/status/specshift_path_watch.py",
    "claim_logic_classifier": "tools/claim_logic/claim_logic_classifier.py",
    "claim_logic_audit_gate": "tools/claim_logic/claim_logic_audit_gate.py",
    "delivery_packet_generator": "tools/pilot_intake/delivery_packet_generator.py",
    "evidence_ledger": "tools/pilot_intake/evidence_ledger.py",
    "qa_workplan": "memory_layer/wiki/operator_memory/specshift_qa_regression_harness/specshift_qa_regression_harness_workplan.json",
    "active_workplan": "memory_layer/wiki/operator_memory/active_workplan.json",
    "brewfile": "memory_layer/wiki/operator_memory/workstation_dependencies/Brewfile",
    "brew_versions": "memory_layer/wiki/operator_memory/workstation_dependencies/brew_installed_versions.txt",
    "brew_taps": "memory_layer/wiki/operator_memory/workstation_dependencies/brew_taps.txt",
    "security_monitoring_doc": "docs/workstation/security/security_monitoring_baseline.md",
    "workstation_tooling_doc": "docs/workstation/dependencies/workstation_tooling_baseline.md",
    "research_tooling_doc": "docs/workstation/dependencies/research_intelligence_tooling_baseline.md",
}

def run(cmd: list[str], ok_codes: set[int] | None = None) -> dict:
    ok_codes = ok_codes or {0}
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    return {
        "cmd": cmd,
        "returncode": proc.returncode,
        "passed": proc.returncode in ok_codes,
        "stdout_tail": proc.stdout[-2500:],
        "stderr_tail": proc.stderr[-2500:],
    }

def file_presence() -> dict:
    rows = []
    missing = []
    for name, rel in REQUIRED_FILES.items():
        path = ROOT / rel
        exists = path.exists()
        rows.append({
            "name": name,
            "path": rel,
            "exists": exists,
            "is_executable": path.exists() and path.is_file() and bool(path.stat().st_mode & 0o111),
        })
        if not exists:
            missing.append(rel)
    return {
        "status": "pass" if not missing else "fail",
        "missing": missing,
        "files": rows,
    }

def active_workplan_state() -> dict:
    path = ROOT / REQUIRED_FILES["active_workplan"]
    if not path.exists():
        return {"status": "fail", "issue": "active_workplan.json missing"}

    data = json.loads(path.read_text(encoding="utf-8"))
    active_phase = data.get("active_phase", "")
    next_action = data.get("next_action", "")
    last_completed = data.get("last_completed_workplan", "")

    expected_complete = active_phase == "specshift_qa_regression_harness_complete"

    return {
        "status": "pass" if expected_complete else "review",
        "active_phase": active_phase,
        "next_action": next_action,
        "last_completed_workplan": last_completed,
        "expected_complete": expected_complete,
    }

def completed_workplans() -> dict:
    workplan_paths = [
        "memory_layer/wiki/operator_memory/specshift_buyer_artifact_simulator/specshift_buyer_artifact_simulator_pilot_readiness_score_workplan.json",
        "memory_layer/wiki/operator_memory/specshift_claim_logic/specshift_claim_logic_negation_aware_safety_scanner_workplan.json",
        "memory_layer/wiki/operator_memory/specshift_qa_regression_harness/specshift_qa_regression_harness_workplan.json",
    ]

    rows = []
    bad = []
    for rel in workplan_paths:
        path = ROOT / rel
        if not path.exists():
            rows.append({"path": rel, "status": "missing"})
            bad.append(rel)
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        status = data.get("status")
        phases = data.get("phases", [])
        incomplete = [p.get("phase") for p in phases if p.get("status") != "complete"]
        okay = status in {"complete", "complete_parked"} and not incomplete
        rows.append({
            "path": rel,
            "status": status,
            "phase_count": len(phases),
            "incomplete": incomplete,
            "okay": okay,
        })
        if not okay:
            bad.append(rel)

    return {
        "status": "pass" if not bad else "review",
        "workplans": rows,
    }

def command_matrix() -> dict:
    checks = {
        "specshift_qa": run(["python3", "tools/status/specshift_qa.py"]),
        "security_doctor": run(["python3", "tools/status/specshift_security_doctor.py"], ok_codes={0}),
        "path_watch": run(["python3", "tools/status/specshift_path_watch.py"], ok_codes={0, 1}),
        "security_scan": run(["python3", "tools/status/specshift_security_scan.py"], ok_codes={0}),
        "qa_tracker": run(["python3", "tools/status/specshift_qa_regression_progress.py"]),
    }

    parsed = {}
    for name in ["specshift_qa", "security_doctor", "path_watch", "security_scan"]:
        out = checks[name]["stdout_tail"]
        try:
            parsed[name] = json.loads(out)
        except Exception:
            parsed[name] = {"parse_status": "not_json_or_truncated"}

    hard_failures = [
        name for name, result in checks.items()
        if not result["passed"] and name not in {"path_watch"}
    ]

    return {
        "status": "pass" if not hard_failures else "fail",
        "hard_failures": hard_failures,
        "checks": checks,
        "parsed_statuses": {
            name: parsed.get(name, {}).get("status", parsed.get(name, {}).get("parse_status"))
            for name in parsed
        },
    }

def dependency_records() -> dict:
    paths = [
        ROOT / "memory_layer/wiki/operator_memory/workstation_dependencies/Brewfile",
        ROOT / "memory_layer/wiki/operator_memory/workstation_dependencies/brew_installed_versions.txt",
        ROOT / "memory_layer/wiki/operator_memory/workstation_dependencies/brew_taps.txt",
    ]
    missing = [str(p.relative_to(ROOT)) for p in paths if not p.exists()]
    sizes = {
        str(p.relative_to(ROOT)): p.stat().st_size if p.exists() else 0
        for p in paths
    }
    return {
        "status": "pass" if not missing else "fail",
        "missing": missing,
        "sizes": sizes,
    }

def git_state() -> dict:
    status = run(["git", "status", "--short"])
    log = run(["git", "log", "--oneline", "-5"])
    return {
        "status": "pass" if not status["stdout_tail"].strip() else "review",
        "dirty_lines": status["stdout_tail"].splitlines(),
        "recent_commits": log["stdout_tail"].splitlines(),
    }

def main() -> int:
    report = {
        "engine": "specshift_systems_survey_v1",
        "ran_at_utc": datetime.now(timezone.utc).isoformat(),
        "repo": str(ROOT),
        "checks": {
            "file_presence": file_presence(),
            "active_workplan_state": active_workplan_state(),
            "completed_workplans": completed_workplans(),
            "dependency_records": dependency_records(),
            "command_matrix": command_matrix(),
            "git_state": git_state(),
        },
        "claim_boundary": BOUNDARY,
    }

    statuses = [v.get("status", "review") for v in report["checks"].values()]
    if "fail" in statuses:
        report["status"] = "fail"
    elif "review" in statuses:
        report["status"] = "review"
    else:
        report["status"] = "pass"

    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["status"] in {"pass", "review"} else 1

if __name__ == "__main__":
    raise SystemExit(main())
