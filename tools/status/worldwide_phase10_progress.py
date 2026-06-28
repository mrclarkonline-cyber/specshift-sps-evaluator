#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

REGISTRATION = Path("memory_layer/wiki/operator_memory/worldwide_phase10/phase10_pattern_detection_registration.json")
REPORT = Path("memory_layer/wiki/operator_memory/worldwide_phase10/phase10_pattern_detection_report.json")

print("Worldwide Phase 10 pattern detection layer status")
print("=" * 68)
print()

if REGISTRATION.exists():
    data = json.loads(REGISTRATION.read_text(encoding="utf-8"))
    print("Registration: FOUND")
    print(f"    status: {data.get('status')}")
    print(f"    goal:   {data.get('phase10_goal')}")
else:
    print("Registration: MISSING")

print()

if REPORT.exists():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    patterns_detected = int(report.get("candidate_patterns_detected", 0))
    artifacts_checked = int(report.get("artifacts_checked", 0))
    held = int(report.get("patterns_held", 0))
    status = "COMPLETE" if artifacts_checked and held == 0 else "PARTIAL" if patterns_detected else "HELD"

    print(f"Pattern detection report: {status}")
    print(f"    artifacts checked:           {artifacts_checked}")
    print(f"    candidate patterns detected: {patterns_detected}")
    print(f"    patterns held:               {held}")
    print(f"    artifact:                    {REPORT}")

    progress = 100.0 if status == "COMPLETE" else 60.0 if status == "PARTIAL" else 30.0
else:
    print("Pattern detection report: MISSING")
    progress = 20.0 if REGISTRATION.exists() else 0.0

print()
print(f"Overall Phase 10 progress score: {progress:.1f}%")
print()
print("Boundary: Phase 10 detects metadata-level candidate patterns only.")
print("No production monitoring, content validation, contradiction detection, causal inference, prediction, alert readiness, autonomous action, or truth resolution claimed.")
