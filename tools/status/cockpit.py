#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ACTIVE = Path("memory_layer/wiki/operator_memory/active_workplan.json")
WORKPLAN = Path("memory_layer/wiki/operator_memory/workstation_command_center/workstation_command_center_upgrade_workplan.json")
OUT_DIR = Path("memory_layer/wiki/operator_memory/workstation_command_center")
STATE = OUT_DIR / "cockpit_state.json"

MODES = {
    "specshift": {
        "purpose": "SpecShift command-center mode for product, audit, reliability, claim-safety, and buyer-safe workflow.",
        "commands": [
            "specshift_board",
            "wiki_landing",
            "claim_gauntlet",
            "promote_artifact",
            "provenance_vault",
            "phase_map",
        ],
        "paths": [
            "~/specshift_terminal_intelligence",
            "memory_layer/wiki/operator_memory/active_workplan.json",
            "memory_layer/wiki/operator_memory/workstation_command_center/",
            "docs/workstation/",
            "tools/status/",
        ],
        "wiki_pages": [
            "docs/workstation/workstation_command_center_upgrade_workplan.md",
            "docs/workstation/phase21_claim_overstatement_detector.md",
            "docs/workstation/phase22_artifact_promotion_gate.md",
            "docs/workstation/phase24_local_provenance_vault.md",
        ],
        "next_actions": [
            "Run specshift_board for current state.",
            "Use claim_gauntlet before public-facing wording.",
            "Use promote_artifact before moving anything public-facing.",
            "End completed repo/wiki work with wiki_landing.",
        ],
        "boundary": "SpecShift cockpit is local workflow context only. No buyer claims, production monitoring, autonomous action, or truth resolution."
    },
    "orchestra": {
        "purpose": "Orchestra mode for source intake, research pulls, global observation scaffolds, and structured data acquisition.",
        "commands": [
            "orchestra_probe",
            "orchestra_conduct",
            "orchestra_signals",
            "orchestra_board",
            "orchestra_sources",
            "orchestra_fetch",
            "fetch_et",
        ],
        "paths": [
            "~/WORK/tools/orchestra/bin/",
            "~/WORK/tools/orchestra/adapters/",
            "~/WORK/tools/orchestra/config/",
            "~/WORK/research/global_observation/",
        ],
        "wiki_pages": [
            "memory_layer/wiki/operator_memory/workstation_command_center/workstation_command_center_upgrade_workplan.json",
        ],
        "next_actions": [
            "Use Orchestra for bounded intake/source work.",
            "Keep source pulls lawful, public, and API-friendly.",
            "Route resulting artifacts through provenance_vault and claim_gauntlet before promotion.",
        ],
        "boundary": "Orchestra cockpit is local intake context only. No surveillance, targeting, unauthorized access, or autonomous monitoring claims."
    },
    "ddf": {
        "purpose": "DDF / analytical-core mode for structural pattern, negative-space, second-order, and math-overlay work.",
        "commands": [
            "phase_map",
            "claim_gauntlet",
            "provenance_vault",
            "wiki_landing",
        ],
        "paths": [
            "memory_layer/wiki/operator_memory/worldwide_phase10/",
            "memory_layer/wiki/operator_memory/worldwide_phase11/",
            "memory_layer/wiki/operator_memory/worldwide_phase12/",
            "memory_layer/wiki/operator_memory/worldwide_phase13/",
            "memory_layer/wiki/operator_memory/worldwide_phase14/",
            "memory_layer/wiki/operator_memory/worldwide_phase15/",
            "memory_layer/wiki/operator_memory/worldwide_phase16/",
        ],
        "wiki_pages": [
            "docs/workstation/worldwide_phase10_pattern_detection_layer.md",
            "docs/workstation/worldwide_phase11_negative_space_pattern_layer.md",
            "docs/workstation/worldwide_phase12_advanced_math_overlay.md",
            "docs/workstation/worldwide_phase13_secondary_condition_math_overlay.md",
            "docs/workstation/worldwide_phase16_analytical_audit_layer.md",
        ],
        "next_actions": [
            "Keep outputs at candidate/review/scaffold tier.",
            "Run claim_gauntlet before translating analytical outputs into external-facing language.",
            "Do not promote pattern candidates into truth, causality, prediction, or alert claims.",
        ],
        "boundary": "DDF cockpit is analysis context only. No validated anomaly, causal, prediction, consciousness, or truth-resolution claims."
    },
    "outreach": {
        "purpose": "Outreach mode for buyer-safe drafts, packets, claim boundaries, provenance checks, and promotion gates.",
        "commands": [
            "claim_gauntlet",
            "promote_artifact",
            "provenance_vault",
            "specshift_board",
            "wiki_landing",
        ],
        "paths": [
            "docs/workstation/",
            "memory_layer/wiki/operator_memory/workstation_command_center/",
            "deliverables/",
        ],
        "wiki_pages": [
            "docs/workstation/phase21_claim_overstatement_detector.md",
            "docs/workstation/phase22_artifact_promotion_gate.md",
            "docs/workstation/phase24_local_provenance_vault.md",
        ],
        "next_actions": [
            "Run claim_gauntlet on external-facing language.",
            "Run promote_artifact before public/buyer-facing promotion.",
            "Keep first-send outreach text-only unless a human chooses otherwise.",
            "Use counsel/CPA threshold if procurement, money, or contract terms become real.",
        ],
        "boundary": "Outreach cockpit is drafting and gate context only. No legal advice, financial advice, binding offers, or autonomous sending."
    },
    "shutdown": {
        "purpose": "Shutdown mode for clean stopping, parking, tomorrow's first task, and canonical landing.",
        "commands": [
            "close_universe",
            "wiki_landing",
            "git status --short",
        ],
        "paths": [
            "memory_layer/wiki/operator_memory/active_workplan.json",
            "memory_layer/wiki/operator_memory/workstation_command_center/close_universe_state.json",
            "memory_layer/wiki/operator_memory/workstation_command_center/close_universe_log.jsonl",
        ],
        "wiki_pages": [
            "docs/workstation/phase23_close_universe_shutdown.md",
        ],
        "next_actions": [
            "Run close_universe to summarize work and tomorrow's first task.",
            "Resolve dirty Git before claiming clean shutdown.",
            "End completed repo/wiki work with wiki_landing.",
        ],
        "boundary": "Shutdown cockpit is local summary only. No OS lockout, autonomous action, or hidden routing."
    }
}

def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def main() -> int:
    parser = argparse.ArgumentParser(description="SpecShift cockpit mode")
    parser.add_argument("mode", nargs="?", default="specshift", choices=sorted(MODES), help="Cockpit mode to load")
    args = parser.parse_args()

    now = datetime.now(timezone.utc).isoformat()
    active = load_json(ACTIVE)
    workplan = load_json(WORKPLAN)
    mode = MODES[args.mode]

    state = {
        "engine": "cockpit_mode_v1",
        "created_at_utc": now,
        "mode": args.mode,
        "purpose": mode["purpose"],
        "commands": mode["commands"],
        "paths": mode["paths"],
        "wiki_pages": mode["wiki_pages"],
        "next_actions": mode["next_actions"],
        "active_workplan": active.get("active_workplan", ""),
        "active_phase": active.get("active_phase", ""),
        "active_tracker": active.get("active_tracker", ""),
        "workplan_status": workplan.get("status", ""),
        "boundary": mode["boundary"],
        "claim_boundary": "Cockpit mode is local context loading only. It does not execute autonomous work, route externally, monitor production, authorize actions, or resolve truth."
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"SpecShift Cockpit: {args.mode}")
    print("=" * 72)
    print(f"purpose: {mode['purpose']}")
    print()
    print("Commands:")
    for item in mode["commands"]:
        print(f"  - {item}")
    print()
    print("Paths:")
    for item in mode["paths"]:
        print(f"  - {item}")
    print()
    print("Wiki/pages:")
    for item in mode["wiki_pages"]:
        print(f"  - {item}")
    print()
    print("Next actions:")
    for item in mode["next_actions"]:
        print(f"  - {item}")
    print()
    print(f"Active workplan: {state['active_workplan']}")
    print(f"Active phase: {state['active_phase']}")
    print()
    print(f"Boundary: {mode['boundary']}")
    print("Cockpit mode loads context only. It does not execute autonomous work.")
    print(f"State: {STATE}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
