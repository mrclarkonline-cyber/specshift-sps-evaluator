#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

REGISTRATION = Path("memory_layer/wiki/operator_memory/worldwide_phase7/phase7_human_review_packet_registration.json")
REPORT = Path("memory_layer/wiki/operator_memory/worldwide_phase7/phase7_human_review_packet_report.json")

print("Worldwide Phase 7 human-review packet scaffold status")
print("=" * 70)
print()

if REGISTRATION.exists():
    data = json.loads(REGISTRATION.read_text(encoding="utf-8"))
    print("Registration: FOUND")
    print(f"    status: {data.get('status')}")
    print(f"    goal:   {data.get('phase7_goal')}")
else:
    print("Registration: MISSING")

print()

if REPORT.exists():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    packets_created = int(report.get("review_packets_created", 0))
    packets_held = int(report.get("review_packets_held", 0))
    status = "COMPLETE" if packets_created and packets_held == 0 else "PARTIAL" if packets_created else "HELD"

    print(f"Human-review packet report: {status}")
    print(f"    review packets created: {packets_created}")
    print(f"    review packets held:    {packets_held}")
    print(f"    artifact:               {REPORT}")

    progress = 100.0 if status == "COMPLETE" else 60.0 if status == "PARTIAL" else 30.0
else:
    print("Human-review packet report: MISSING")
    progress = 20.0 if REGISTRATION.exists() else 0.0

print()
print(f"Overall Phase 7 progress score: {progress:.1f}%")
print()
print("Boundary: Phase 7 creates human-review packet scaffolds only.")
print("No production monitoring, content validation, contradiction detection, agreement detection, corroboration, alert readiness, autonomous action, or truth resolution claimed.")
