#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

BOUNDARY = (
    "SpecShift QA command only. It runs local regression and smoke checks. "
    "It does not create legal advice, financial advice, binding terms, compliance certification, "
    "production validation, automated verdict, free pilot commitment, autonomous client action, "
    "truth validation, or hidden-mechanism claim."
)

ROOT = Path(__file__).resolve().parents[2]
VENV_PYTHON = ROOT / ".venv_specshift_qa" / "bin" / "python"

def run(cmd: list[str], expected_returncodes: set[int] | None = None) -> dict:
    expected_returncodes = expected_returncodes or {0}
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    return {
        "cmd": cmd,
        "returncode": proc.returncode,
        "expected_returncodes": sorted(expected_returncodes),
        "passed": proc.returncode in expected_returncodes,
        "stdout_tail": proc.stdout[-2000:],
        "stderr_tail": proc.stderr[-2000:],
    }

def main() -> int:
    python = str(VENV_PYTHON if VENV_PYTHON.exists() else sys.executable)

    checks = []

    checks.append(run([python, "-m", "pytest", "-q"]))

    checks.append(run([
        python,
        "tools/claim_logic/claim_logic_classifier.py",
        "--text",
        "SpecShift does not provide production validation.",
        "--json",
    ]))

    checks.append(run([
        python,
        "tools/claim_logic/claim_logic_audit_gate.py",
        "--file",
        "tests/fixtures/claim_logic/audit_gate/safe_non_claims.md",
        "--output",
        "/tmp/specshift_qa_safe_gate.json",
    ]))

    checks.append(run([
        python,
        "tools/claim_logic/claim_logic_audit_gate.py",
        "--file",
        "tests/fixtures/claim_logic/audit_gate/unsafe_assertions.md",
        "--output",
        "/tmp/specshift_qa_unsafe_gate.json",
    ], expected_returncodes={1}))

    checks.append(run([
        python,
        "tools/pilot_intake/delivery_packet_generator.py",
        "--project-dir",
        "tests/fixtures/buyer_artifact_simulator/delivery_packet_sample_project",
        "--output",
        "/tmp/specshift_qa_delivery_packet.md",
        "--recommendation",
        "REPEAT_WITH_CLEANER_DATA",
        "--report",
        "/tmp/specshift_qa_delivery_packet_report.json",
    ]))

    checks.append(run([
        python,
        "tools/pilot_intake/evidence_ledger.py",
        "summary",
        "--ledger",
        "tests/fixtures/buyer_artifact_simulator/sample_evidence_ledger.jsonl",
        "--output",
        "/tmp/specshift_qa_evidence_ledger_summary.json",
    ]))

    failed = [check for check in checks if not check["passed"]]

    report = {
        "engine": "specshift_qa_v1",
        "ran_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "pass" if not failed else "fail",
        "check_count": len(checks),
        "failed_count": len(failed),
        "checks": checks,
        "claim_boundary": BOUNDARY,
    }

    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not failed else 1

if __name__ == "__main__":
    raise SystemExit(main())
