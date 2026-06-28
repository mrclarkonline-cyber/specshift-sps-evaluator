#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

REG = Path("memory_layer/wiki/operator_memory/worldwide_phase14/phase14_scenario_suggestion_registration.json")
REPORT = Path("memory_layer/wiki/operator_memory/worldwide_phase14/phase14_bounded_scenario_suggestion_report.json")

print("Worldwide Phase 14 bounded scenario suggestion layer status")
print("=" * 76)
print()

if REG.exists():
    data = json.loads(REG.read_text(encoding="utf-8"))
    print("Registration: FOUND")
    print(f"    status: {data.get('status')}")
    print(f"    goal:   {data.get('phase14_goal')}")
else:
    print("Registration: MISSING")

print()

if REPORT.exists():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    count = int(report.get("scenario_suggestions_created", 0))
    print("Bounded scenario suggestion report: COMPLETE")
    print(f"    review suggestions created: {count}")
    print(f"    artifact:                   {REPORT}")
    progress = 100.0
else:
    print("Bounded scenario suggestion report: MISSING")
    progress = 20.0 if REG.exists() else 0.0

print()
print(f"Overall Phase 14 progress score: {progress:.1f}%")
print()
print("Boundary: Phase 14 creates review suggestions only.")
print("No production monitoring, content validation, contradiction detection, causal inference, prediction, alert readiness, autonomous action, or truth resolution claimed.")
