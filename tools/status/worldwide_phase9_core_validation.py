#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REGISTRATION = Path("memory_layer/wiki/operator_memory/worldwide_phase9/phase9_analytical_core_registration.json")
OUT_DIR = Path("memory_layer/wiki/operator_memory/worldwide_phase9")
OUT_DIR.mkdir(parents=True, exist_ok=True)

REPORT = OUT_DIR / "phase9_analytical_core_validation_report.json"

now = datetime.now(timezone.utc).isoformat()

if not REGISTRATION.exists():
    raise SystemExit(f"Missing registration: {REGISTRATION}")

data = json.loads(REGISTRATION.read_text(encoding="utf-8"))
lanes = data.get("analysis_lanes", [])

required_lane_names = {
    "pattern_detection_layer",
    "negative_space_pattern_layer",
    "advanced_math_overlay",
    "secondary_condition_math_overlay",
    "scenario_suggestion_layer",
}

forbidden_boundary_terms = [
    "production monitoring",
    "content validation",
    "contradiction detection",
    "causal inference",
    "prediction",
    "alert readiness",
    "autonomous action",
    "truth resolution",
]

lane_reports = []

for lane in lanes:
    problems = []
    lane_name = lane.get("lane", "")

    if lane_name not in required_lane_names:
        problems.append("unexpected_or_missing_lane_name")

    if not lane.get("purpose"):
        problems.append("missing_purpose")

    if not lane.get("allowed_outputs") and not lane.get("allowed_methods"):
        problems.append("missing_allowed_outputs_or_methods")

    if not lane.get("forbidden_outputs"):
        problems.append("missing_forbidden_outputs")

    lane_reports.append({
        "lane": lane_name,
        "status": "validated" if not problems else "held",
        "problems": problems,
        "claim_boundary": "Lane validation only. This does not run analysis or claim pattern truth, causality, prediction, alert readiness, autonomous action, or truth resolution."
    })

registered_lane_names = {lane.get("lane", "") for lane in lanes}
missing_lanes = sorted(required_lane_names - registered_lane_names)

boundary = str(data.get("claim_boundary", "")).lower()
boundary_problems = []
for term in forbidden_boundary_terms:
    if term not in boundary:
        boundary_problems.append(f"missing_boundary_term:{term}")

lanes_checked = len(lane_reports)
lanes_passed = sum(1 for item in lane_reports if item["status"] == "validated")
lanes_held = lanes_checked - lanes_passed

status = "complete" if lanes_checked and lanes_held == 0 and not missing_lanes and not boundary_problems else "partial"

report = {
    "phase": "phase_9_worldwide_analytical_core_registration",
    "status": status,
    "created_at_utc": now,
    "registration_artifact": str(REGISTRATION),
    "lanes_checked": lanes_checked,
    "lanes_passed": lanes_passed,
    "lanes_held": lanes_held,
    "missing_lanes": missing_lanes,
    "boundary_problems": boundary_problems,
    "lane_reports": lane_reports,
    "claim_boundary": "Phase 9 validates the analytical core registration only. It does not run pattern analysis, validate content, infer causality, make predictions, create alerts, take autonomous action, or resolve truth."
}

REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

print(f"Wrote {REPORT}")
print(f"Lanes checked: {lanes_checked}")
print(f"Lanes passed:  {lanes_passed}")
print(f"Lanes held:    {lanes_held}")
print(f"Missing lanes: {missing_lanes}")
print(f"Boundary problems: {boundary_problems}")
