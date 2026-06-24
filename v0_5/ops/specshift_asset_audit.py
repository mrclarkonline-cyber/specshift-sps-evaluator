#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

BASE = Path.home() / "specshift_terminal_intelligence"
V05 = BASE / "v0_5"

def json_ok(path):
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return True
    except Exception:
        return False

def py_ok(path):
    try:
        subprocess.check_output([sys.executable, "-m", "py_compile", str(path)], text=True, stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

def check_file(label, path, kind="file", required=True):
    p = Path(path)
    if kind == "json":
        ok = p.exists() and p.is_file() and json_ok(p)
    elif kind == "python":
        ok = p.exists() and p.is_file() and py_ok(p)
    elif kind == "dir":
        ok = p.exists() and p.is_dir()
    else:
        ok = p.exists() and p.is_file() and p.stat().st_size > 0

    status = "PASS" if ok else ("REVIEW" if not required else "FAIL")
    print(f"- {label}: {status} :: {p}")
    return ok or not required

def main():
    print("SpecShift Asset Audit v0.1")
    print("Safe local company-asset audit. No email sent. No secrets printed.")
    print()

    failures = []

    sections = {
        "Top-level operator files": [
            ("Operator quickstart", BASE / "OPERATOR_QUICKSTART.md", "file", True),
            ("Command reference", BASE / "SPECSHIFT_COMMANDS.md", "file", True),
            ("Local asset map JSON", BASE / "LOCAL_ASSET_MAP.json", "json", True),
            ("Local asset map MD", BASE / "LOCAL_ASSET_MAP.md", "file", True),
            ("Terminal index", BASE / "terminal_intelligence_index.json", "json", True)
        ],
        "Core engine": [
            ("v0.5 suite", V05 / "unknown_domain_adversarial_suite_v0_5.json", "json", True),
            ("v0.5 validator", V05 / "validate_v0_5_suite.py", "python", True),
            ("Claim scanner", V05 / "claim_scan_git_log.py", "python", True),
            ("Claim register", V05 / "git_log_claim_language_register_v0_1.json", "json", True)
        ],
        "Call companion": [
            ("Call companion script", V05 / "call_companion" / "specshift_call_companion.py", "python", True),
            ("Call companion README", V05 / "call_companion" / "README.md", "file", True)
        ],
        "Email bridge": [
            ("Readiness checker", V05 / "email_bridge" / "proton_bridge_readiness_check.py", "python", True),
            ("Guarded sender", V05 / "email_bridge" / "proton_guarded_send.py", "python", True),
            ("Example config", V05 / "email_bridge" / "proton_bridge_config.example.json", "json", True),
            ("Email bridge README", V05 / "email_bridge" / "README.md", "file", True),
            ("Local SMTP config", Path.home() / ".specshift" / "proton_bridge_config.json", "json", True)
        ],
        "Vertical packs": [
            ("Vertical registry", V05 / "vertical_packs" / "vertical_diagnostic_packs_registry_v0_1.json", "json", True),
            ("Finance pack", V05 / "vertical_packs" / "finance_reconciliation_agent_diagnostic_pack_v0_1.json", "json", True),
            ("Procurement pack", V05 / "vertical_packs" / "procurement_agent_diagnostic_pack_v0_1.json", "json", True),
            ("Customer support pack", V05 / "vertical_packs" / "customer_support_escalation_agent_diagnostic_pack_v0_1.json", "json", True),
            ("Healthcare operations pack", V05 / "vertical_packs" / "healthcare_operations_agent_diagnostic_pack_v0_1.json", "json", True),
            ("Education IEP pack", V05 / "vertical_packs" / "education_iep_workflow_diagnostic_pack_v0_1.json", "json", True),
            ("Candidate skin registry", V05 / "vertical_packs" / "candidate_skin_registry_v0_1.json", "json", False)
        ],
        "Outreach pipeline": [
            ("Pipeline summary", V05 / "outreach_pipeline" / "outreach_pipeline_summary_v0_1.json", "json", True),
            ("Targets CSV", V05 / "outreach_pipeline" / "outreach_targets_v0_1.csv", "file", True),
            ("Touch log CSV", V05 / "outreach_pipeline" / "outreach_touch_log_v0_1.csv", "file", True),
            ("Pipeline manager", V05 / "outreach_pipeline" / "outreach_pipeline_manager.py", "python", True),
            ("Pipeline README", V05 / "outreach_pipeline" / "README.md", "file", True)
        ],
        "Ops": [
            ("Ops dashboard", V05 / "ops" / "specshift_ops_dashboard.py", "python", True),
            ("Asset audit", V05 / "ops" / "specshift_asset_audit.py", "python", True),
            ("Ops README", V05 / "ops" / "README.md", "file", True)
        ],
        "Local export area": [
            ("Exports folder", BASE / "exports", "dir", False)
        ]
    }

    for section, checks in sections.items():
        print("=" * 72)
        print(section)
        print("=" * 72)
        for label, path, kind, required in checks:
            ok = check_file(label, path, kind, required)
            if not ok:
                failures.append(label)
        print()

    print("=" * 72)
    print("Safety checks")
    print("=" * 72)

    sender = V05 / "email_bridge" / "proton_guarded_send.py"
    sender_text = sender.read_text(encoding="utf-8")
    safety = {
        "Guarded sender requires exact confirmation": "Type exactly" in sender_text,
        "Guarded sender supports dry-run": "--dry-run" in sender_text,
        "Guarded sender uses Keychain service": "specshift_proton_smtp_token" in sender_text,
        "No Apple Mail automation in guarded sender": "osascript" not in sender_text and "tell application" not in sender_text
    }

    for label, ok in safety.items():
        print(f"- {label}: {'PASS' if ok else 'FAIL'}")
        if not ok:
            failures.append(label)

    print()
    print("=" * 72)
    print("Verdict")
    print("=" * 72)

    if failures:
        print("STATUS: REVIEW")
        for item in failures:
            print(f"- {item}")
        raise SystemExit(1)

    print("STATUS: PASS")
    print("Known SpecShift company assets are mapped and findable.")
    print("Personal/local Ben files were not crawled or indexed.")
    print("No email was sent.")

if __name__ == "__main__":
    main()
