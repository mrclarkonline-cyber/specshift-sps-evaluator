#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path
from collections import Counter

BASE = Path.home() / "specshift_terminal_intelligence"
V05 = BASE / "v0_5"

def run(cmd, check=False):
    try:
        out = subprocess.check_output(cmd, cwd=BASE, text=True, stderr=subprocess.STDOUT)
        return True, out.strip()
    except subprocess.CalledProcessError as e:
        if check:
            raise
        return False, e.output.strip()

def json_ok(path):
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return True
    except Exception:
        return False

def py_compile_ok(path):
    ok, out = run([sys.executable, "-m", "py_compile", str(path)])
    return ok, out

def print_section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)

def main():
    failures = []

    print("SpecShift Ops Dashboard v0.1")
    print("No email is sent by this dashboard.")

    print_section("Repo")
    ok, status = run(["git", "status", "--short"])
    ok2, latest = run(["git", "log", "--oneline", "--max-count=1"])
    print("latest commit:", latest)
    print("repo clean:", "YES" if not status else "NO")
    if status:
        print(status)
        failures.append("repo not clean")

    print_section("Core artifacts")
    json_files = [
        V05 / "unknown_domain_adversarial_suite_v0_5.json",
        V05 / "focused_paid_pilot_posture_v0_1.json",
        V05 / "bounded_paid_pilot_outreach_email_v0_2.json",
        V05 / "role_specific_outreach_variants_v0_2.json",
        V05 / "focused_diagnostic_pilot_scoping_call_script_v0_1.json",
        V05 / "git_log_claim_language_register_v0_1.json",
        BASE / "terminal_intelligence_index.json"
    ]
    for path in json_files:
        ok = path.exists() and json_ok(path)
        print(f"{path.relative_to(BASE)}: {'PASS' if ok else 'FAIL'}")
        if not ok:
            failures.append(f"bad json: {path}")

    suite_path = V05 / "unknown_domain_adversarial_suite_v0_5.json"
    suite = json.loads(suite_path.read_text(encoding="utf-8"))
    cases = suite.get("test_cases", [])
    cats = Counter(c.get("category") for c in cases)
    print(f"suite cases: {len(cases)}")
    print(f"suite categories: {len(cats)}")
    print("suite status:", suite.get("status"))

    print_section("Python tools")
    tools = [
        V05 / "validate_v0_5_suite.py",
        V05 / "claim_scan_git_log.py",
        V05 / "call_companion" / "specshift_call_companion.py",
        V05 / "email_bridge" / "proton_bridge_readiness_check.py",
        V05 / "email_bridge" / "proton_guarded_send.py"
    ]
    for tool in tools:
        ok, out = py_compile_ok(tool)
        print(f"{tool.relative_to(BASE)}: {'PASS' if ok else 'FAIL'}")
        if not ok:
            failures.append(f"compile fail: {tool}")
            print(out)

    print_section("Call companion")
    call_tool = V05 / "call_companion" / "specshift_call_companion.py"
    text = call_tool.read_text(encoding="utf-8")
    checks = {
        "Proton manual workflow": "Manual send through Proton Mail",
        "Full signature": "Founder, SpecShift Labs LLC",
        "ORCID": "ORCID: 0009-0005-8622-0251",
        "Scope outline generator": "def build_pilot_scope_outline",
        "Case selector": "def select_relevant_cases"
    }
    for label, needle in checks.items():
        ok = needle in text
        print(f"{label}: {'PASS' if ok else 'FAIL'}")
        if not ok:
            failures.append(f"call companion missing: {label}")

    forbidden = ["osascript", 'tell application "Mail"', "Apple Mail draft", "make new outgoing message"]
    found = [item for item in forbidden if item in text]
    print("Apple Mail automation absent:", "PASS" if not found else "FAIL")
    if found:
        failures.append("Apple Mail automation found")

    print_section("Email bridge")
    sender = V05 / "email_bridge" / "proton_guarded_send.py"
    sender_text = sender.read_text(encoding="utf-8")
    sender_checks = {
        "Guarded confirmation": "Type exactly",
        "Keychain token service": "specshift_proton_smtp_token",
        "Dry-run support": "--dry-run",
        "Expected from email": "ben@specshiftlabs.com"
    }
    for label, needle in sender_checks.items():
        ok = needle in sender_text
        print(f"{label}: {'PASS' if ok else 'FAIL'}")
        if not ok:
            failures.append(f"sender missing: {label}")

    local_cfg = Path.home() / ".specshift" / "proton_bridge_config.json"
    print("local SMTP config exists:", "PASS" if local_cfg.exists() else "REVIEW")
    if local_cfg.exists():
        try:
            cfg = json.loads(local_cfg.read_text(encoding="utf-8"))
            print("SMTP host:", cfg.get("smtp_host"))
            print("SMTP port:", cfg.get("smtp_port"))
            print("SMTP user:", cfg.get("smtp_username"))
            print("from email:", cfg.get("from_email"))
        except Exception as e:
            print("local SMTP config parse: FAIL", e)
            failures.append("local SMTP config parse fail")

    print_section("Vertical packs")
    registry_path = V05 / "vertical_packs" / "vertical_diagnostic_packs_registry_v0_1.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    packs = registry.get("registered_vertical_packs", [])
    built = [p for p in packs if "built" in p.get("status", "")]
    print(f"registered packs: {len(packs)}")
    print(f"built packs: {len(built)}")
    for pack in packs:
        print(f"- {pack.get('pack_name')}: {pack.get('status')}")
        for artifact in pack.get("artifact_paths", []):
            p = Path(artifact)
            if not p.exists():
                failures.append(f"missing pack artifact: {artifact}")

    print_section("Claim scan")
    ok, scan = run([sys.executable, "v0_5/claim_scan_git_log.py"])
    print(scan)
    if not ok or '"status": "PASS"' not in scan:
        failures.append("claim scan not pass")

    print_section("Next action")
    index = json.loads((BASE / "terminal_intelligence_index.json").read_text(encoding="utf-8"))
    print(index.get("next_action", "No next_action found."))

    print_section("Verdict")
    if failures:
        print("STATUS: REVIEW")
        for item in failures:
            print("-", item)
        raise SystemExit(1)

    print("STATUS: PASS")
    print("SpecShift stack is clean, organized, and outreach-ready.")
    print("No email was sent.")

if __name__ == "__main__":
    main()
