#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

REG = Path("memory_layer/wiki/operator_memory/worldwide_phase16/phase16_analytical_audit_registration.json")
REPORT = Path("memory_layer/wiki/operator_memory/worldwide_phase16/phase16_analytical_audit_report.json")

print("Worldwide Phase 16 analytical audit layer status")
print("=" * 70)
print()

if REG.exists():
    data = json.loads(REG.read_text(encoding="utf-8"))
    print("Registration: FOUND")
    print(f"    status: {data.get('status')}")
    print(f"    goal:   {data.get('phase16_goal')}")
else:
    print("Registration: MISSING")

print()

if REPORT.exists():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    status = str(report.get("status", "unknown")).upper()
    checks = int(report.get("audit_checks_run", 0))
    passed = int(report.get("audit_checks_passed", 0))
    review = int(report.get("audit_checks_review", 0))
    held = int(report.get("audit_checks_held", 0))

    print(f"Analytical audit report: {status}")
    print(f"    audit checks run:    {checks}")
    print(f"    audit checks passed: {passed}")
    print(f"    audit checks review: {review}")
    print(f"    audit checks held:   {held}")
    print(f"    artifact:            {REPORT}")

    progress = 100.0 if held == 0 and checks else 60.0 if passed else 30.0
else:
    print("Analytical audit report: MISSING")
    progress = 20.0 if REG.exists() else 0.0

print()
print(f"Overall Phase 16 progress score: {progress:.1f}%")
print()
print("Boundary: Phase 16 audits artifacts and boundaries only.")
print("No production monitoring, content validation, contradiction detection, causal inference, prediction, alert readiness, autonomous action, legal/medical/financial advice, policy decision support, or truth resolution claimed.")
