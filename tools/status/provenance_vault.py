#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

VAULT_DIR = Path("memory_layer/wiki/operator_memory/workstation_command_center")
VAULT = VAULT_DIR / "provenance_vault.jsonl"
REPORT = VAULT_DIR / "provenance_vault_report.json"
ACTIVE = Path("memory_layer/wiki/operator_memory/active_workplan.json")
PROMOTION_HISTORY = VAULT_DIR / "artifact_promotion_history.jsonl"

DEFAULT_STATUS = "private"
ALLOWED_STATUS = {"public", "private", "protected", "archive-caution"}

DEFAULT_ARTIFACTS = [
    "docs/workstation/phase17_mission_control_dashboard.md",
    "docs/workstation/phase18_active_workplan_brain.md",
    "docs/workstation/phase19_kira_recommendation_engine.md",
    "docs/workstation/phase20_phil_morale_layer.md",
    "docs/workstation/phase21_claim_overstatement_detector.md",
    "docs/workstation/phase22_artifact_promotion_gate.md",
    "docs/workstation/phase23_close_universe_shutdown.md",
    "memory_layer/wiki/operator_memory/workstation_command_center/workstation_command_center_upgrade_workplan.json",
    "memory_layer/wiki/operator_memory/workstation_command_center/claim_gauntlet_report.json",
    "memory_layer/wiki/operator_memory/workstation_command_center/artifact_promotion_gate_report.json",
    "memory_layer/wiki/operator_memory/workstation_command_center/close_universe_state.json",
    "tools/status/specshift_board.py",
    "tools/status/active_workplan_brain_check.py",
    "tools/status/kira_recommendation_engine.py",
    "tools/status/phil_morale_layer.py",
    "tools/status/claim_gauntlet.py",
    "tools/status/promote_artifact.py",
    "tools/status/close_universe.py",
]

def run(cmd: list[str], timeout: int = 20) -> tuple[int, str]:
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)
    return proc.returncode, (proc.stdout + proc.stderr).strip()

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def latest_commit() -> str:
    code, output = run(["git", "log", "-1", "--pretty=%H"])
    return output if code == 0 and output else "unknown"

def infer_status(path: Path, requested: str | None) -> str:
    if requested:
        return requested
    lower = str(path).lower()
    if "protected" in lower or "do_not" in lower:
        return "protected"
    if "archive" in lower or "caution" in lower:
        return "archive-caution"
    if str(path).startswith("docs/") or str(path).startswith("tools/"):
        return "private"
    return DEFAULT_STATUS

def infer_wiki_link(path: Path) -> str:
    stem = path.stem
    candidates = [
        Path("docs/workstation") / f"{stem}.md",
        Path("docs/workstation") / f"{path.name}.md",
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    if str(path).startswith("docs/workstation/"):
        return str(path)
    return ""

def load_promotion_refs() -> dict[str, list[dict]]:
    refs: dict[str, list[dict]] = {}
    if not PROMOTION_HISTORY.exists():
        return refs
    for line in PROMOTION_HISTORY.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except Exception:
            continue
        artifact = rec.get("artifact", {}).get("artifact", "")
        if artifact:
            refs.setdefault(artifact, []).append({
                "status": rec.get("status"),
                "target": rec.get("target"),
                "created_at_utc": rec.get("created_at_utc"),
                "promotion_allowed": rec.get("promotion_allowed"),
            })
    return refs

def append_record(record: dict) -> None:
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    with VAULT.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

def main() -> int:
    parser = argparse.ArgumentParser(description="SpecShift local provenance vault")
    parser.add_argument("artifacts", nargs="*", help="Artifact paths to register")
    parser.add_argument("--status", choices=sorted(ALLOWED_STATUS), default=None)
    parser.add_argument("--wiki-link", default="")
    parser.add_argument("--default-set", action="store_true", help="Register default command-center artifacts")
    args = parser.parse_args()

    now = datetime.now(timezone.utc).isoformat()
    active = load_json(ACTIVE)
    promotion_refs = load_promotion_refs()

    artifact_paths = args.artifacts
    if args.default_set or not artifact_paths:
        artifact_paths = DEFAULT_ARTIFACTS

    records = []
    missing = []

    for raw in artifact_paths:
        path = Path(raw)
        if not path.exists():
            missing.append(str(path))
            continue

        status = infer_status(path, args.status)
        wiki_link = args.wiki_link or infer_wiki_link(path)
        record = {
            "engine": "provenance_vault_v1",
            "registered_at_utc": now,
            "path": str(path),
            "sha256": sha256(path),
            "size_bytes": path.stat().st_size,
            "status": status,
            "linked_wiki_page": wiki_link,
            "active_workplan": active.get("active_workplan", ""),
            "active_phase": active.get("active_phase", ""),
            "git_commit": latest_commit(),
            "promotion_history": promotion_refs.get(str(path), []),
            "claim_boundary": "Local provenance record only. This does not publish, promote, certify, validate, or externally route the artifact."
        }
        append_record(record)
        records.append(record)

    status_counts: dict[str, int] = {}
    for rec in records:
        status_counts[rec["status"]] = status_counts.get(rec["status"], 0) + 1

    report = {
        "engine": "provenance_vault_v1",
        "status": "complete" if records and not missing else "partial" if records else "held",
        "created_at_utc": now,
        "records_created": len(records),
        "missing_artifacts": missing,
        "status_counts": status_counts,
        "vault_artifact": str(VAULT),
        "claim_boundary": "Provenance Vault records local artifact hashes, timestamps, paths, status, wiki links, and promotion references only. It does not publish, promote, certify, validate, or externally route artifacts."
    }

    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("Provenance Vault")
    print("=" * 64)
    print(f"Status: {report['status'].upper()}")
    print(f"Records created: {len(records)}")
    print(f"Missing artifacts: {len(missing)}")
    print(f"Vault: {VAULT}")
    print(f"Report: {REPORT}")
    print()
    for key, value in sorted(status_counts.items()):
        print(f"{key}: {value}")
    if missing:
        print()
        print("Missing:")
        for item in missing:
            print(f"  - {item}")
    print()
    print("Boundary: local provenance only. No publication, promotion, certification, or external routing.")
    return 0 if records else 1

if __name__ == "__main__":
    raise SystemExit(main())
