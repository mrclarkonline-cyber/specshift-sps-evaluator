#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

REGISTRATION = Path("memory_layer/wiki/operator_memory/worldwide_phase4/phase4_worldwide_claim_safety_registration.json")
REPORT = Path("memory_layer/wiki/operator_memory/worldwide_phase4/phase4_claim_safety_normalization_report.json")

print("Worldwide Phase 4 claim-safety normalization status")
print("=" * 68)
print()

if REGISTRATION.exists():
    data = json.loads(REGISTRATION.read_text(encoding="utf-8"))
    print("Registration: FOUND")
    print(f"    status: {data.get('status')}")
    print(f"    goal:   {data.get('phase4_goal')}")
else:
    print("Registration: MISSING")

print()

if REPORT.exists():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    total = int(report.get("records_checked", 0))
    passed = int(report.get("records_passed", 0))
    held = int(report.get("records_held", 0))
    status = "COMPLETE" if total and passed == total and held == 0 else "PARTIAL" if passed else "HELD"

    print(f"Normalization report: {status}")
    print(f"    records checked: {total}")
    print(f"    records passed:  {passed}")
    print(f"    records held:    {held}")
    print(f"    artifact:        {REPORT}")
    progress = 100.0 if status == "COMPLETE" else 50.0 if status == "PARTIAL" else 20.0
else:
    print("Normalization report: MISSING")
    progress = 20.0 if REGISTRATION.exists() else 0.0

print()
print(f"Overall Phase 4 progress score: {progress:.1f}%")
print()
print("Boundary: Phase 4 checks schema, provenance, uncertainty, and claim-safety labels only.")
print("No production monitoring, content validation, alert readiness, autonomous action, or truth resolution claimed.")
