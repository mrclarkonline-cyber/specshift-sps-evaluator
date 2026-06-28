#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

REG = Path("memory_layer/wiki/operator_memory/worldwide_phase13/phase13_secondary_condition_math_registration.json")
REPORT = Path("memory_layer/wiki/operator_memory/worldwide_phase13/phase13_secondary_condition_math_report.json")

print("Worldwide Phase 13 secondary-condition math overlay status")
print("=" * 76)
print()

if REG.exists():
    data = json.loads(REG.read_text(encoding="utf-8"))
    print("Registration: FOUND")
    print(f"    status: {data.get('status')}")
    print(f"    goal:   {data.get('phase13_goal')}")
else:
    print("Registration: MISSING")

print()

if REPORT.exists():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    count = int(report.get("secondary_condition_candidates", 0))
    print("Secondary-condition math report: COMPLETE")
    print(f"    secondary-condition candidates: {count}")
    print(f"    artifact:                       {REPORT}")
    progress = 100.0
else:
    print("Secondary-condition math report: MISSING")
    progress = 20.0 if REG.exists() else 0.0

print()
print(f"Overall Phase 13 progress score: {progress:.1f}%")
print()
print("Boundary: Phase 13 uses secondary-condition descriptive metadata math only.")
print("No production monitoring, content validation, contradiction detection, causal inference, prediction, validated hidden-structure claims, alert readiness, autonomous action, or truth resolution claimed.")
