#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

REGISTRATION = Path("memory_layer/wiki/operator_memory/worldwide_phase8/phase8_review_packet_index_closeout_registration.json")
REPORT = Path("memory_layer/wiki/operator_memory/worldwide_phase8/phase8_review_packet_index_closeout_report.json")

print("Worldwide Phase 8 review-packet index closeout status")
print("=" * 70)
print()

if REGISTRATION.exists():
    data = json.loads(REGISTRATION.read_text(encoding="utf-8"))
    print("Registration: FOUND")
    print(f"    status: {data.get('status')}")
    print(f"    goal:   {data.get('phase8_goal')}")
else:
    print("Registration: MISSING")

print()

if REPORT.exists():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    indexed = int(report.get("packets_indexed", 0))
    held = int(report.get("packets_held", 0))
    status = "COMPLETE" if indexed and held == 0 else "PARTIAL" if indexed else "HELD"

    print(f"Review-packet index closeout report: {status}")
    print(f"    packets indexed: {indexed}")
    print(f"    packets held:    {held}")
    print(f"    artifact:        {REPORT}")

    progress = 100.0 if status == "COMPLETE" else 60.0 if status == "PARTIAL" else 30.0
else:
    print("Review-packet index closeout report: MISSING")
    progress = 20.0 if REGISTRATION.exists() else 0.0

print()
print(f"Overall Phase 8 progress score: {progress:.1f}%")
print()
print("Boundary: Phase 8 creates packet indexes and closeout summaries only.")
print("No production monitoring, content validation, contradiction detection, agreement detection, corroboration, alert readiness, autonomous action, or truth resolution claimed.")
