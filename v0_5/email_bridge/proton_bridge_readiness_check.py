#!/usr/bin/env python3
import json
import os
import socket
import subprocess
from pathlib import Path

CONFIG = Path.home() / ".specshift" / "proton_bridge_config.json"

EXPECTED_FROM = "ben@specshiftlabs.com"

def load_config():
    if not CONFIG.exists():
        return None
    return json.loads(CONFIG.read_text(encoding="utf-8"))

def port_open(host, port, timeout=2.0):
    try:
        with socket.create_connection((host, int(port)), timeout=timeout):
            return True
    except OSError:
        return False

def process_hint():
    try:
        out = subprocess.check_output(["pgrep", "-fl", "Proton Mail Bridge|proton"], text=True)
        return [line for line in out.splitlines() if line.strip()]
    except Exception:
        return []

def main():
    print("SpecShift Proton Bridge Readiness Check v0.1")
    print()

    cfg = load_config()
    if cfg is None:
        print("CONFIG: MISSING")
        print(f"Expected local config at: {CONFIG}")
        raise SystemExit(1)

    host = cfg.get("smtp_host", "127.0.0.1")
    port = cfg.get("smtp_port", 1025)
    from_email = cfg.get("from_email", "")

    print(f"Config path: {CONFIG}")
    print(f"From email: {from_email}")
    print(f"SMTP host: {host}")
    print(f"SMTP port: {port}")
    print()

    checks = []

    checks.append(("from_email_is_specshift", from_email == EXPECTED_FROM))
    checks.append(("config_not_in_repo", ".specshift" in str(CONFIG)))
    checks.append(("send_mode_disabled", cfg.get("mode") == "readiness_only"))
    checks.append(("typed_confirmation_required", cfg.get("send_requires_typed_confirmation") is True))
    checks.append(("smtp_port_open", port_open(host, port)))

    procs = process_hint()
    print("Process hints:")
    if procs:
        for line in procs[:10]:
            print(f"- {line}")
    else:
        print("- No Proton Bridge-like process found by pgrep.")
    print()

    print("Checks:")
    failed = []
    for name, ok in checks:
        print(f"- {name}: {'PASS' if ok else 'REVIEW'}")
        if not ok:
            failed.append(name)

    print()
    if failed:
        print("READINESS: REVIEW")
        print("Items needing attention:")
        for item in failed:
            print(f"- {item}")
        print()
        print("No email was sent. This checker never sends email.")
        raise SystemExit(1)

    print("READINESS: PASS")
    print("Local Proton Bridge settings appear ready for a future guarded send-mode script.")
    print("No email was sent. This checker never sends email.")

if __name__ == "__main__":
    main()
