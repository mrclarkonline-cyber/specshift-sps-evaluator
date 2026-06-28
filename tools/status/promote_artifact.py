#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ACTIVE = Path("memory_layer/wiki/operator_memory/active_workplan.json")
OUT_DIR = Path("memory_layer/wiki/operator_memory/workstation_command_center")
REPORT = OUT_DIR / "artifact_promotion_gate_report.json"
HISTORY = OUT_DIR / "artifact_promotion_history.jsonl"
CLAIM_REPORT = OUT_DIR / "claim_gauntlet_report.json"

PUBLIC_ROOTS = [
    Path("docs"),
    Path("public_release_hashes"),
    Path("release"),
    Path("deliverables"),
]

PRIVATE_MARKERS = [
    "protected",
    "private",
    "do_not_first_send",
    "do_not_send",
    "archive-caution",
    "operator_memory",
    "scratch",
]

BUYER_RISK_TERMS = [
    "proves",
    "guarantees",
    "validated",
    "production-ready",
    "truth",
    "autonomous",
    "alert ready",
    "contradiction detection",
    "agreement detection",
    "causal",
]

BOUNDARY_TERMS = [
    "does not claim",
    "no production monitoring",
    "content validation",
    "truth resolution",
    "human review",
]

def run(cmd: list[str], timeout: int = 20) -> tuple[int, str]:
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)
    return proc.returncode, (proc.stdout + proc.stderr).strip()

def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def git_dirty() -> tuple[bool, str]:
    code, output = run(["git", "status", "--short"])
    return code != 0 or bool(output.strip()), output

def classify_path(path: Path) -> str:
    lower = str(path).lower()
    if any(marker in lower for marker in PRIVATE_MARKERS):
        return "private_or_protected"
    if any(str(path).startswith(str(root)) for root in PUBLIC_ROOTS):
        return "public_candidate"
    return "internal_candidate"

def text_for_scan(path: Path) -> str:
    if path.suffix.lower() not in {".md", ".txt", ".json", ".jsonl", ".py", ".csv"}:
        return ""
    if path.stat().st_size > 1_000_000:
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")

def main() -> int:
    parser = argparse.ArgumentParser(description="SpecShift artifact promotion gate")
    parser.add_argument("artifact", nargs="?", help="Artifact path to gate for promotion")
    parser.add_argument("--target", default="public", choices=["public", "private", "protected", "archive"], help="Promotion target class")
    parser.add_argument("--dry-run", action="store_true", help="Run checks without creating a promotion history entry")
    args = parser.parse_args()

    now = datetime.now(timezone.utc).isoformat()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    artifact = Path(args.artifact) if args.artifact else None
    checks = []

    def add_check(name: str, status: str, detail: object, severity: str = "info") -> None:
        checks.append({
            "check": name,
            "status": status,
            "severity": severity,
            "detail": detail,
            "checked_at_utc": now,
        })

    dirty, dirty_output = git_dirty()
    add_check(
        "git_clean_status",
        "pass" if not dirty else "hold",
        {"dirty": dirty, "status": dirty_output},
        "high" if dirty else "info",
    )

    claim_report = load_json(CLAIM_REPORT)
    actionable_hits = int(claim_report.get("actionable_hits", 0)) if claim_report else None
    claim_status = "pass" if claim_report and actionable_hits == 0 else "review" if claim_report else "hold"
    add_check(
        "claim_scan",
        claim_status,
        {
            "claim_report": str(CLAIM_REPORT),
            "actionable_hits": actionable_hits,
            "risk_level": claim_report.get("risk_level", "missing") if claim_report else "missing",
            "note": "Promotion may proceed only with human review if claim scan is review; public promotion should require pass or explicit counsel/reviewer override.",
        },
        "medium" if claim_status == "review" else "high" if claim_status == "hold" else "info",
    )

    if artifact is None:
        add_check(
            "artifact_path",
            "hold",
            "No artifact path supplied. Use: promote_artifact <path> --target public|private|protected|archive",
            "high",
        )
        artifact_info = {}
    elif not artifact.exists():
        add_check("artifact_path", "hold", {"artifact": str(artifact), "exists": False}, "high")
        artifact_info = {"artifact": str(artifact), "exists": False}
    else:
        artifact_class = classify_path(artifact)
        artifact_hash = sha256(artifact)
        text = text_for_scan(artifact)

        artifact_info = {
            "artifact": str(artifact),
            "exists": True,
            "sha256": artifact_hash,
            "size_bytes": artifact.stat().st_size,
            "path_classification": artifact_class,
            "target": args.target,
        }

        add_check("artifact_path", "pass", artifact_info)

        if args.target == "public" and artifact_class == "private_or_protected":
            add_check(
                "public_private_boundary",
                "hold",
                "Private/protected/operator-memory artifact cannot be promoted directly to public target.",
                "high",
            )
        else:
            add_check(
                "public_private_boundary",
                "pass",
                f"path_classification={artifact_class}, target={args.target}",
            )

        if text:
            lower = text.lower()
            risky_terms = [term for term in BUYER_RISK_TERMS if term in lower]
            boundary_terms = [term for term in BOUNDARY_TERMS if term in lower]

            add_check(
                "buyer_safe_wording",
                "pass" if not risky_terms else "review",
                {"risky_terms": risky_terms},
                "medium" if risky_terms else "info",
            )

            add_check(
                "boundary_language",
                "pass" if boundary_terms else "review",
                {"boundary_terms_found": boundary_terms},
                "medium" if not boundary_terms else "info",
            )
        else:
            add_check(
                "buyer_safe_wording",
                "review",
                "Artifact is binary, large, or unsupported for text scan. Human review required.",
                "medium",
            )
            add_check(
                "boundary_language",
                "review",
                "Artifact is binary, large, or unsupported for boundary scan. Human review required.",
                "medium",
            )

        add_check(
            "provenance_check",
            "pass",
            {
                "sha256": artifact_hash,
                "timestamp_utc": now,
                "path": str(artifact),
                "target": args.target,
            },
        )

    holds = [c for c in checks if c["status"] == "hold"]
    reviews = [c for c in checks if c["status"] == "review"]

    if holds:
        gate_status = "held"
    elif reviews:
        gate_status = "review_required"
    else:
        gate_status = "pass"

    report = {
        "engine": "artifact_promotion_gate_v1",
        "status": gate_status,
        "created_at_utc": now,
        "artifact": artifact_info,
        "target": args.target,
        "dry_run": args.dry_run,
        "checks": checks,
        "holds": len(holds),
        "reviews": len(reviews),
        "promotion_allowed": gate_status == "pass",
        "human_review_required": gate_status != "pass",
        "claim_boundary": "Artifact promotion gate is a local workflow gate only. It does not certify legal, compliance, scientific, factual, production, or buyer readiness. Human review remains required for public-facing promotion.",
    }

    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if not args.dry_run and artifact is not None and artifact.exists():
        with HISTORY.open("a", encoding="utf-8") as f:
            f.write(json.dumps(report, ensure_ascii=False, sort_keys=True) + "\n")

    print("Artifact Promotion Gate")
    print("=" * 64)
    print(f"Status: {gate_status.upper()}")
    print(f"Target: {args.target}")
    print(f"Artifact: {artifact if artifact else 'none supplied'}")
    print(f"Holds: {len(holds)}")
    print(f"Reviews: {len(reviews)}")
    print(f"Promotion allowed: {gate_status == 'pass'}")
    print(f"Report: {REPORT}")
    print(f"History: {HISTORY}")
    print()

    if holds:
        print("Holds:")
        for item in holds:
            print(f"  - {item['check']}: {item['detail']}")
        print()

    if reviews:
        print("Review required:")
        for item in reviews:
            print(f"  - {item['check']}: {item['detail']}")
        print()

    print("Boundary: local promotion gate only. Human review remains required.")
    return 0 if gate_status != "held" else 1

if __name__ == "__main__":
    raise SystemExit(main())
