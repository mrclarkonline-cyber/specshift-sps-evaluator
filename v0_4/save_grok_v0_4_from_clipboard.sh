#!/usr/bin/env bash
set -euo pipefail

OUT="$HOME/specshift_terminal_intelligence/v0_4/unknown_domain_adversarial_suite_v0_4.json"

pbpaste > "$OUT"

python3 - <<'PY'
import json
from pathlib import Path

path = Path.home() / "specshift_terminal_intelligence" / "v0_4" / "unknown_domain_adversarial_suite_v0_4.json"

raw = path.read_text(encoding="utf-8").strip()

# If Grok wraps in markdown fences, strip them.
if raw.startswith("```"):
    lines = raw.splitlines()
    lines = [ln for ln in lines if not ln.strip().startswith("```")]
    raw = "\n".join(lines).strip()
    path.write_text(raw + "\n", encoding="utf-8")

data = json.loads(raw)

cases = data.get("test_cases", [])
categories = {}
for c in cases:
    categories[c.get("category", "UNKNOWN")] = categories.get(c.get("category", "UNKNOWN"), 0) + 1

required = [
    "provenance",
    "observable_anchor",
    "failure_column",
    "proxy_honesty",
    "claim_boundary",
    "implementation_safety",
    "workflow_traceability",
    "human_review_trigger",
    "operational_impact",
    "recovery_path"
]

missing = []
for c in cases:
    rubric = c.get("scoring_rubric", {})
    miss = [r for r in required if r not in rubric]
    if miss:
        missing.append({"id": c.get("id"), "missing": miss})

print("Saved:", path)
print("Suite:", data.get("suite_name"))
print("Status:", data.get("status"))
print("Cases:", len(cases))
print("Categories:")
for k, v in sorted(categories.items()):
    print(f"  {k}: {v}")

if missing:
    print("\nMissing scoring fields:")
    print(json.dumps(missing, indent=2))
else:
    print("\nAll required scoring fields present.")

print("\nDone.")
PY
