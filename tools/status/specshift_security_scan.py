#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

def run(cmd: list[str], ok_codes={0}) -> dict:
    proc = subprocess.run(cmd, text=True, capture_output=True)
    return {
        "cmd": cmd,
        "returncode": proc.returncode,
        "passed": proc.returncode in ok_codes,
        "stdout_tail": proc.stdout[-3000:],
        "stderr_tail": proc.stderr[-3000:],
    }

checks = []

checks.append(run(["python3", "tools/status/specshift_security_doctor.py"], ok_codes={0}))
checks.append(run(["python3", "tools/status/specshift_path_watch.py"], ok_codes={0, 1}))
checks.append(run(["gitleaks", "detect", "--source", ".", "--no-git", "--redact", "--verbose"], ok_codes={0}))
checks.append(run(["trufflehog", "filesystem", ".", "--no-update"], ok_codes={0}))
checks.append(run(["lynis", "audit", "system", "--quick"], ok_codes={0, 1}))

failed = [c for c in checks if not c["passed"]]

report = {
    "engine": "specshift_security_scan_v1",
    "ran_at_utc": datetime.now(timezone.utc).isoformat(),
    "status": "pass" if not failed else "review",
    "check_count": len(checks),
    "failed_or_review_count": len(failed),
    "checks": checks,
    "claim_boundary": "Defensive local security scan only. No offensive tooling, surveillance authorization, credential collection, legal advice, compliance certification, or production validation."
}

print(json.dumps(report, indent=2, sort_keys=True))
raise SystemExit(0)
