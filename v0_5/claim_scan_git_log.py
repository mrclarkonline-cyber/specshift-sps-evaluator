#!/usr/bin/env python3
import json
import re
import subprocess
from pathlib import Path

BASE = Path.home() / "specshift_terminal_intelligence"
REGISTER = BASE / "v0_5" / "git_log_claim_language_register_v0_1.json"

RISK_RE = re.compile(
    r"validated|benchmark|certif|compliance|audit|safety|guarantee|deploy|security|proof|proven|hardened",
    re.IGNORECASE,
)

register = json.loads(REGISTER.read_text(encoding="utf-8"))
covered = {
    item["commit"]: item
    for item in register.get("flagged_commit_messages", [])
}

raw = subprocess.check_output(
    ["git", "log", "--oneline", "--max-count=100"],
    cwd=BASE,
    text=True,
)

flagged = []
covered_hits = []
uncovered_hits = []

for line in raw.splitlines():
    if not RISK_RE.search(line):
        continue
    commit = line.split()[0]
    flagged.append(line)
    if commit in covered:
        covered_hits.append(line)
    else:
        uncovered_hits.append(line)

summary = {
    "flagged_total": len(flagged),
    "covered_historical_risks": len(covered_hits),
    "new_uncovered_risks": len(uncovered_hits),
    "status": "PASS" if not uncovered_hits else "REVIEW_REQUIRED",
}

print(json.dumps(summary, indent=2))

if covered_hits:
    print("\nCovered historical risks:")
    for line in covered_hits:
        print(f"- {line}")

if uncovered_hits:
    print("\nNew uncovered risks:")
    for line in uncovered_hits:
        print(f"- {line}")
    raise SystemExit(1)

print("\nStanding interpretation:")
print(register["standing_boundary_line"])
