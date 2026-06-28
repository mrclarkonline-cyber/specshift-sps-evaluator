#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "configs" / "worldwide_sources" / "phase2_group1_sources.json"
REPORT = ROOT / "memory_layer" / "wiki" / "operator_memory" / "phase2_group1_healthcheck_latest.json"

data = json.loads(CONFIG.read_text(encoding="utf-8"))
sources = data.get("sources", [])

print("Phase 2 Worldwide Group 1")
print(f"Configuration status: {data.get('status')}")
print(f"Configured sources: {len(sources)}/7")
print("Implementation status: scaffold configured; live ingestion not claimed")
print()

if REPORT.exists():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    ok = sum(1 for s in report.get("sources", []) if s.get("any_ok"))
    total = report.get("sources_total", len(sources))
    print(f"Latest health check: {report.get('checked_at_utc')}")
    print(f"Reachability: {ok}/{total}")
else:
    print("Latest health check: not run yet")

print()
print("Configured group:")
for i, src in enumerate(sources, 1):
    print(f"{i}. {src['name']} [{src['status']}]")
