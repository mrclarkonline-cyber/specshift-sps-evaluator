#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

REG = Path("memory_layer/wiki/operator_memory/professional_readiness/professional_readiness_workplan.json")
ACTIVE = Path("memory_layer/wiki/operator_memory/active_workplan.json")

print("Professional Readiness Forensic Accounting Package status")
print("=" * 78)
print()

active = json.loads(ACTIVE.read_text(encoding="utf-8")) if ACTIVE.exists() else {}
active_phase = active.get("active_phase", "")
next_action = active.get("next_action", "")

if not REG.exists():
    print("Registration: MISSING")
    progress = 0.0
else:
    data = json.loads(REG.read_text(encoding="utf-8"))
    phases = data.get("phases", [])
    completed = sum(1 for p in phases if p.get("status") == "complete")
    total = len(phases)

    print("Registration: FOUND")
    print(f"    status: {data.get('status')}")
    print(f"    purpose: {data.get('purpose')}")
    print()

    print("Professional readiness phases:")
    for item in phases:
        phase = item.get("phase", "unknown")
        goal = item.get("goal", "")
        status = item.get("status", "registered")
        if phase == active_phase:
            icon = "🎯"
        elif status == "complete":
            icon = "✅"
        else:
            icon = "🟡"
        print(f"    {icon} {phase}: {goal}")

    progress = round((completed / total) * 100, 1) if total else 0.0

print()
print(f"Current active phase: {active_phase or 'unknown'}")
print(f"Next action: {next_action or 'unknown'}")
print()
print(f"Overall Professional Readiness progress score: {progress:.1f}%")
print()
print("Boundary: Professional readiness is preparation for lawyer/CPA review only.")
print("No legal advice, financial advice, tax advice, valuation, compliance certification, or commercial guarantee claimed.")
