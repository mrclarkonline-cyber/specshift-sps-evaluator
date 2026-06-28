#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

REG = Path("memory_layer/wiki/operator_memory/worldwide_phase11/phase11_negative_space_registration.json")
REPORT = Path("memory_layer/wiki/operator_memory/worldwide_phase11/phase11_negative_space_report.json")

print("Worldwide Phase 11 negative-space pattern layer status")
print("=" * 72)
print()

if REG.exists():
    data = json.loads(REG.read_text(encoding="utf-8"))
    print("Registration: FOUND")
    print(f"    status: {data.get('status')}")
    print(f"    goal:   {data.get('phase11_goal')}")
else:
    print("Registration: MISSING")

print()

if REPORT.exists():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    count = int(report.get("negative_space_candidates", 0))
    print("Negative-space report: COMPLETE")
    print(f"    candidates detected: {count}")
    print(f"    artifact:            {REPORT}")
    progress = 100.0
else:
    print("Negative-space report: MISSING")
    progress = 20.0 if REG.exists() else 0.0

print()
print(f"Overall Phase 11 progress score: {progress:.1f}%")
print()
print("Boundary: Phase 11 detects negative-space candidates only. Absence is not proof.")
print("No production monitoring, content validation, contradiction detection, causal inference, prediction, alert readiness, autonomous action, or truth resolution claimed.")
