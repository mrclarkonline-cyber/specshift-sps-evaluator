#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

REGISTRATION = Path("memory_layer/wiki/operator_memory/worldwide_phase9/phase9_analytical_core_registration.json")
VALIDATION = Path("memory_layer/wiki/operator_memory/worldwide_phase9/phase9_analytical_core_validation_report.json")

print("Worldwide Phase 9 analytical core registration status")
print("=" * 70)
print()

if REGISTRATION.exists():
    data = json.loads(REGISTRATION.read_text(encoding="utf-8"))
    print("Registration: FOUND")
    print(f"    status: {data.get('status')}")
    print(f"    goal:   {data.get('phase9_goal')}")
    print()
    print("Analysis lanes:")
    for lane in data.get("analysis_lanes", []):
        print(f"    - {lane.get('lane')}: {lane.get('purpose')}")
else:
    print("Registration: MISSING")

print()

if VALIDATION.exists():
    report = json.loads(VALIDATION.read_text(encoding="utf-8"))
    lanes_checked = int(report.get("lanes_checked", 0))
    lanes_passed = int(report.get("lanes_passed", 0))
    lanes_held = int(report.get("lanes_held", 0))
    status = "COMPLETE" if lanes_checked and lanes_held == 0 else "PARTIAL" if lanes_passed else "HELD"

    print(f"Analytical core validation report: {status}")
    print(f"    lanes checked: {lanes_checked}")
    print(f"    lanes passed:  {lanes_passed}")
    print(f"    lanes held:    {lanes_held}")
    print(f"    artifact:      {VALIDATION}")

    progress = 100.0 if status == "COMPLETE" else 60.0 if status == "PARTIAL" else 30.0
else:
    print("Analytical core validation report: MISSING")
    progress = 20.0 if REGISTRATION.exists() else 0.0

print()
print(f"Overall Phase 9 progress score: {progress:.1f}%")
print()
print("Boundary: Phase 9 registers the analytical core only.")
print("No production monitoring, content validation, contradiction detection, causal inference, prediction, alert readiness, autonomous action, or truth resolution claimed.")
