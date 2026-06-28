#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

REGISTRATION = Path("memory_layer/wiki/operator_memory/worldwide_phase5/phase5_worldwide_cross_source_comparison_registration.json")
REPORT = Path("memory_layer/wiki/operator_memory/worldwide_phase5/phase5_cross_source_comparison_readiness_report.json")

print("Worldwide Phase 5 cross-source comparison runway status")
print("=" * 70)
print()

if REGISTRATION.exists():
    data = json.loads(REGISTRATION.read_text(encoding="utf-8"))
    print("Registration: FOUND")
    print(f"    status: {data.get('status')}")
    print(f"    goal:   {data.get('phase5_goal')}")
else:
    print("Registration: MISSING")

print()

if REPORT.exists():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    categories_checked = int(report.get("categories_checked", 0))
    ready_categories = int(report.get("comparison_ready_categories", 0))
    held_categories = int(report.get("comparison_held_categories", 0))
    status = "COMPLETE" if categories_checked and held_categories == 0 else "PARTIAL" if ready_categories else "HELD"

    print(f"Comparison readiness report: {status}")
    print(f"    categories checked: {categories_checked}")
    print(f"    comparison ready:   {ready_categories}")
    print(f"    held categories:    {held_categories}")
    print(f"    artifact:           {REPORT}")

    progress = 100.0 if status == "COMPLETE" else 60.0 if status == "PARTIAL" else 30.0
else:
    print("Comparison readiness report: MISSING")
    progress = 20.0 if REGISTRATION.exists() else 0.0

print()
print(f"Overall Phase 5 progress score: {progress:.1f}%")
print()
print("Boundary: Phase 5 identifies comparison readiness only.")
print("No production monitoring, content validation, contradiction detection, alert readiness, autonomous action, or truth resolution claimed.")
