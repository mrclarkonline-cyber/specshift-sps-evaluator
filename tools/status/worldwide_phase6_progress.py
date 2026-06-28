#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

REGISTRATION = Path("memory_layer/wiki/operator_memory/worldwide_phase6/phase6_candidate_pair_inspection_registration.json")
REPORT = Path("memory_layer/wiki/operator_memory/worldwide_phase6/phase6_candidate_pair_inspection_report.json")

print("Worldwide Phase 6 candidate-pair inspection scaffold status")
print("=" * 74)
print()

if REGISTRATION.exists():
    data = json.loads(REGISTRATION.read_text(encoding="utf-8"))
    print("Registration: FOUND")
    print(f"    status: {data.get('status')}")
    print(f"    goal:   {data.get('phase6_goal')}")
else:
    print("Registration: MISSING")

print()

if REPORT.exists():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    pairs_checked = int(report.get("pairs_checked", 0))
    ready_pairs = int(report.get("inspection_ready_pairs", 0))
    held_pairs = int(report.get("inspection_held_pairs", 0))
    status = "COMPLETE" if pairs_checked and held_pairs == 0 else "PARTIAL" if ready_pairs else "HELD"

    print(f"Candidate-pair inspection report: {status}")
    print(f"    pairs checked:      {pairs_checked}")
    print(f"    inspection ready:   {ready_pairs}")
    print(f"    held pairs:         {held_pairs}")
    print(f"    artifact:           {REPORT}")

    progress = 100.0 if status == "COMPLETE" else 60.0 if status == "PARTIAL" else 30.0
else:
    print("Candidate-pair inspection report: MISSING")
    progress = 20.0 if REGISTRATION.exists() else 0.0

print()
print(f"Overall Phase 6 progress score: {progress:.1f}%")
print()
print("Boundary: Phase 6 inspects candidate-pair metadata only.")
print("No production monitoring, content validation, contradiction detection, agreement detection, alert readiness, autonomous action, or truth resolution claimed.")
