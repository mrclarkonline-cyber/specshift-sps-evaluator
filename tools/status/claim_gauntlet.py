#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ACTIVE = Path("memory_layer/wiki/operator_memory/active_workplan.json")
OUT_DIR = Path("memory_layer/wiki/operator_memory/workstation_command_center")
REPORT = OUT_DIR / "claim_gauntlet_report.json"
RECORDS = OUT_DIR / "claim_gauntlet_hits.jsonl"

SCAN_ROOTS = [
    Path("docs/workstation"),
    Path("memory_layer/wiki/operator_memory"),
]

RISK_TERMS = {
    "proves": "supports / suggests / is consistent with",
    "prove": "support / suggest / test",
    "proof": "evidence / support / candidate indication",
    "detects": "flags / identifies as candidate / surfaces for review",
    "detected": "flagged / surfaced / identified as candidate",
    "guarantees": "is intended to reduce risk / may support",
    "guaranteed": "bounded / intended / not guaranteed",
    "validates": "checks / reviews / tests / supports",
    "validated": "checked / reviewed / not yet externally validated",
    "validation": "review / check / evaluation",
    "truth": "source content / claim status / reviewer determination",
    "truth-resolution": "reviewer-controlled assessment",
    "consciousness": "reported behavior / observed pattern / theoretical claim",
    "intent": "apparent behavior / inferred objective / stated purpose",
    "production-ready": "prototype / bounded scaffold / not production-ready",
    "production ready": "prototype / bounded scaffold / not production-ready",
    "predicts": "estimates / suggests / flags for review",
    "prediction": "forecast candidate / review prompt / estimate",
    "autonomous": "human-reviewed / reviewer-controlled / non-autonomous",
    "alert": "review prompt / flag / note",
    "alerts": "review prompts / flags / notes",
    "causal": "associated / candidate relationship / not causal",
    "causality": "association / possible relationship / not established",
    "contradiction detection": "candidate comparison / human-review prompt",
    "agreement detection": "candidate comparison / human-review prompt",
    "corroborates": "appears related / may support later review",
    "confirms": "is consistent with / supports review / does not confirm",
}

ALLOWLIST_CONTEXT = [
    "does not claim",
    "no ",
    "not ",
    "forbidden",
    "boundary",
    "risk",
    "claim_boundary",
    "do not",
    "without claiming",
    "not claim",
    "no production monitoring",
]

def run(cmd: list[str], timeout: int = 15) -> tuple[int, str]:
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)
    return proc.returncode, (proc.stdout + proc.stderr).strip()

def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def git_dirty() -> bool:
    code, output = run(["git", "status", "--short"])
    return code != 0 or bool(output.strip())

def should_scan(path: Path) -> bool:
    if not path.is_file():
        return False
    if path.stat().st_size > 750_000:
        return False
    return path.suffix.lower() in {".md", ".txt", ".json", ".jsonl", ".py"}

def context_is_allowlisted(line: str, term: str) -> bool:
    lower = line.lower()
    term_idx = lower.find(term.lower())
    window = lower[max(0, term_idx - 80):term_idx + 120] if term_idx >= 0 else lower
    return any(marker in window for marker in ALLOWLIST_CONTEXT)

def main() -> int:
    now = datetime.now(timezone.utc).isoformat()
    active = load_json(ACTIVE)

    hits = []
    files_scanned = 0

    for root in SCAN_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not should_scan(path):
                continue
            files_scanned += 1
            text = path.read_text(encoding="utf-8", errors="ignore")
            lines = text.splitlines()

            for line_no, line in enumerate(lines, start=1):
                lower_line = line.lower()
                for term, safer in RISK_TERMS.items():
                    pattern = r"\b" + re.escape(term.lower()) + r"\b"
                    if re.search(pattern, lower_line):
                        allowlisted = context_is_allowlisted(line, term)
                        hits.append({
                            "path": str(path),
                            "line": line_no,
                            "term": term,
                            "suggested_replacement": safer,
                            "allowlisted_context": allowlisted,
                            "line_text": line[:300],
                            "severity": "review" if allowlisted else "flag",
                            "claim_boundary": "Claim Gauntlet is a local language-risk scanner only. It does not certify legal, compliance, scientific, or factual correctness."
                        })

    actionable = [h for h in hits if not h["allowlisted_context"]]
    by_term = Counter(h["term"] for h in actionable)

    status = "pass" if not actionable else "review"
    risk_level = "low" if not actionable else "medium" if len(actionable) < 20 else "high"

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECORDS.write_text(
        "\n".join(json.dumps(hit, ensure_ascii=False, sort_keys=True) for hit in hits) + ("\n" if hits else ""),
        encoding="utf-8"
    )

    report = {
        "engine": "claim_gauntlet_v1",
        "status": status,
        "risk_level": risk_level,
        "created_at_utc": now,
        "active_workplan": active.get("active_workplan", ""),
        "active_phase": active.get("active_phase", ""),
        "files_scanned": files_scanned,
        "total_hits": len(hits),
        "actionable_hits": len(actionable),
        "allowlisted_hits": len(hits) - len(actionable),
        "actionable_terms": dict(sorted(by_term.items())),
        "records_artifact": str(RECORDS),
        "safer_language_rule": "Prefer candidate, bounded, review, scaffold, flags, supports, suggests, and human-review wording over proof, validation, detection, guarantees, predictions, autonomy, or truth-resolution wording.",
        "claim_boundary": "Claim Gauntlet scans local text for risky overstatement language and suggests safer wording. It does not certify legal, compliance, scientific, factual, or production readiness."
    }

    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("Claim Gauntlet")
    print("=" * 64)
    print(f"Status: {status.upper()}")
    print(f"Risk level: {risk_level}")
    print(f"Files scanned: {files_scanned}")
    print(f"Total hits: {len(hits)}")
    print(f"Actionable hits: {len(actionable)}")
    print(f"Allowlisted hits: {len(hits) - len(actionable)}")
    print(f"Report: {REPORT}")
    print(f"Records: {RECORDS}")
    print()

    if actionable:
        print("Top actionable terms:")
        for term, count in by_term.most_common(12):
            print(f"  - {term}: {count} -> {RISK_TERMS.get(term, 'safer bounded wording')}")
        print()
        print("Kira note: review flagged wording before public promotion. Internal scaffolds may continue if boundaries remain explicit.")
    else:
        print("Kira note: no actionable overstatement hits found.")

    print()
    print("Boundary: local language-risk scanner only. No legal/compliance/scientific certification.")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
