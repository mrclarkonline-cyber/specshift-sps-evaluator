#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

BATCHES = [
    (
        "Batch 1",
        Path("memory_layer/wiki/operator_memory/worldwide_phase3/live_sample_batch1/phase3_batch1_summary.json"),
    ),
    (
        "Batch 2",
        Path("memory_layer/wiki/operator_memory/worldwide_phase3/live_sample_batch2/phase3_batch2_summary.json"),
    ),
]

print("Worldwide Phase 3 bounded live-sample status")
print("=" * 64)
print()

complete = 0
attempted_total = 0
fetched_total = 0
parsed_total = 0

for name, path in BATCHES:
    if not path.exists():
        print(f"{name}: MISSING")
        print(f"    {path}")
        continue

    data = json.loads(path.read_text(encoding="utf-8"))
    attempted = int(data.get("sources_attempted", 0))
    fetched = int(data.get("sources_fetched", 0))
    parsed = int(data.get("samples_parsed", 0))

    attempted_total += attempted
    fetched_total += fetched
    parsed_total += parsed

    status = "COMPLETE" if attempted and parsed == attempted else "PARTIAL" if parsed > 0 else "HELD"
    if status == "COMPLETE":
        complete += 1

    print(f"{name}: {status}")
    print(f"    attempted: {attempted}")
    print(f"    fetched:   {fetched}")
    print(f"    parsed:    {parsed}")
    print(f"    artifact:  {path}")

print()
print(f"Phase 3 batches complete: {complete}/{len(BATCHES)}")
print(f"Phase 3 total sources attempted: {attempted_total}")
print(f"Phase 3 total sources fetched:   {fetched_total}")
print(f"Phase 3 total samples parsed:    {parsed_total}")
print()
print("Boundary: Phase 3 live samples are bounded sample records only.")
print("No production monitoring, content validation, alert readiness, autonomous action, or truth resolution claimed.")
