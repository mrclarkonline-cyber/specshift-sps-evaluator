#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import stat
import subprocess
from datetime import datetime, timezone
from pathlib import Path

BOUNDARY = (
    "SpecShift security doctor only. Defensive local workstation posture checks. "
    "No offensive tooling, surveillance, intrusion, credential collection, legal advice, "
    "compliance certification, or production validation."
)

ROOT = Path(__file__).resolve().parents[2]

CORE_COMMANDS = [
    "curl",
    "wget",
    "git",
    "python3",
    "pip3",
    "ssh",
    "gpg",
    "brew",
]

EXPECTED_COMMAND_PATH_HINTS = {
    "curl": ["/usr/bin/curl", "/opt/homebrew/bin/curl"],
    "git": ["/usr/bin/git", "/opt/homebrew/bin/git"],
    "ssh": ["/usr/bin/ssh"],
    "brew": ["/opt/homebrew/bin/brew"],
}

def run(cmd: list[str]) -> dict:
    proc = subprocess.run(cmd, text=True, capture_output=True)
    return {
        "cmd": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }

def command_paths(command: str) -> list[str]:
    proc = subprocess.run(["/usr/bin/which", "-a", command], text=True, capture_output=True)
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]

def check_command_shadows() -> dict:
    findings = []
    for command in CORE_COMMANDS:
        paths = command_paths(command)
        expected = EXPECTED_COMMAND_PATH_HINTS.get(command, [])
        suspicious = []
        for path in paths:
            if "/Users/" in path and "/.venv" not in path and "/.local" not in path:
                suspicious.append(path)
            if "/WORK/" in path:
                suspicious.append(path)
        findings.append({
            "command": command,
            "paths": paths,
            "expected_path_hints": expected,
            "suspicious_paths": sorted(set(suspicious)),
            "status": "review" if suspicious else "pass",
        })
    return {
        "status": "review" if any(f["status"] == "review" for f in findings) else "pass",
        "findings": findings,
    }

def check_macos_security() -> dict:
    checks = {}

    checks["filevault"] = run(["/usr/bin/fdesetup", "status"])
    checks["firewall"] = run(["/usr/libexec/ApplicationFirewall/socketfilterfw", "--getglobalstate"])
    checks["gatekeeper"] = run(["/usr/sbin/spctl", "--status"])
    checks["sip"] = run(["/usr/bin/csrutil", "status"])

    status = "pass"
    review = []

    if "FileVault is On" not in checks["filevault"]["stdout"]:
        status = "review"
        review.append("FileVault may not be on.")

    if "enabled" not in checks["firewall"]["stdout"].lower():
        status = "review"
        review.append("Firewall may not be enabled.")

    if "assessments enabled" not in checks["gatekeeper"]["stdout"].lower():
        status = "review"
        review.append("Gatekeeper assessments may not be enabled.")

    if "enabled" not in checks["sip"]["stdout"].lower():
        status = "review"
        review.append("System Integrity Protection may not be enabled.")

    return {
        "status": status,
        "review": review,
        "checks": checks,
    }

def check_brew() -> dict:
    taps = run(["brew", "tap"])
    outdated = run(["brew", "outdated"])
    microsoft_hits = [
        line for line in taps["stdout"].splitlines()
        if "microsoft" in line.lower()
    ]

    return {
        "status": "review" if microsoft_hits else "pass",
        "microsoft_taps": microsoft_hits,
        "tap_count": len([x for x in taps["stdout"].splitlines() if x.strip()]),
        "outdated_count": len([x for x in outdated["stdout"].splitlines() if x.strip()]),
        "outdated_tail": outdated["stdout"].splitlines()[:50],
    }

def check_git() -> dict:
    remote = run(["git", "remote", "-v"])
    status = run(["git", "status", "--short"])
    branch = run(["git", "branch", "--show-current"])
    credential_helpers = run(["git", "config", "--global", "--get-all", "credential.helper"])

    return {
        "status": "pass" if not status["stdout"] else "review",
        "branch": branch["stdout"],
        "uncommitted": status["stdout"].splitlines(),
        "remotes": remote["stdout"].splitlines(),
        "credential_helpers": credential_helpers["stdout"].splitlines(),
    }

def check_ssh_permissions() -> dict:
    ssh_dir = Path.home() / ".ssh"
    findings = []

    if not ssh_dir.exists():
        return {"status": "review", "findings": [{"issue": "No ~/.ssh directory found."}]}

    for path in ssh_dir.iterdir():
        if not path.is_file():
            continue
        mode = stat.S_IMODE(path.stat().st_mode)
        if path.name.endswith(".pub") or path.name in {"known_hosts", "config"}:
            continue
        if mode & 0o077:
            findings.append({
                "file": str(path),
                "mode": oct(mode),
                "issue": "Private SSH key may be too permissive.",
                "suggested_fix": f"chmod 600 {path}",
            })

    return {
        "status": "review" if findings else "pass",
        "findings": findings,
    }

def check_qa() -> dict:
    qa = run(["python3", "tools/status/specshift_qa.py"])
    status = "pass"
    parsed = None

    if qa["returncode"] != 0:
        status = "fail"
    else:
        try:
            parsed = json.loads(qa["stdout"])
            if parsed.get("status") != "pass":
                status = "fail"
        except Exception:
            status = "review"

    return {
        "status": status,
        "returncode": qa["returncode"],
        "parsed": parsed,
        "stdout_tail": qa["stdout"][-2000:],
        "stderr_tail": qa["stderr"][-2000:],
    }

def main() -> int:
    report = {
        "engine": "specshift_security_doctor_v1",
        "ran_at_utc": datetime.now(timezone.utc).isoformat(),
        "repo": str(ROOT),
        "checks": {
            "macos_security": check_macos_security(),
            "command_shadows": check_command_shadows(),
            "brew": check_brew(),
            "git": check_git(),
            "ssh_permissions": check_ssh_permissions(),
            "specshift_qa": check_qa(),
        },
        "claim_boundary": BOUNDARY,
    }

    statuses = [
        item.get("status", "review")
        for item in report["checks"].values()
    ]

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
