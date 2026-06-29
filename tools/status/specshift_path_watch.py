#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

CORE = ["curl", "wget", "git", "python3", "pip3", "ssh", "gpg", "brew"]

ALLOW_REVIEW = {
    "python3",
    "pip3",
}

def paths_for(cmd: str) -> list[str]:
    proc = subprocess.run(["/usr/bin/which", "-a", cmd], text=True, capture_output=True)
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]

def is_suspicious(path: str) -> bool:
    return "/WORK/" in path or ("/Users/" in path and "/.venv" not in path and "/.local" not in path)

findings = []
for cmd in CORE:
    paths = paths_for(cmd)
    suspicious = sorted({p for p in paths if is_suspicious(p)})
    status = "pass"
    if suspicious:
        status = "review_allowed" if cmd in ALLOW_REVIEW else "review"
    findings.append({
        "command": cmd,
        "paths": paths,
        "suspicious_paths": suspicious,
        "status": status,
    })

hard_reviews = [f for f in findings if f["status"] == "review"]

report = {
    "engine": "specshift_path_watch_v1",
    "ran_at_utc": datetime.now(timezone.utc).isoformat(),
    "status": "pass" if not hard_reviews else "review",
    "findings": findings,
    "hard_review_count": len(hard_reviews),
    "allowed_review_commands": sorted(ALLOW_REVIEW),
    "claim_boundary": "Defensive PATH monitoring only. No offensive tooling, surveillance authorization, credential collection, legal advice, compliance certification, or production validation."
}

print(json.dumps(report, indent=2, sort_keys=True))
raise SystemExit(0 if report["status"] == "pass" else 1)
