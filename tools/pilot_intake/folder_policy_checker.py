#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

BOUNDARY = (
    "Folder policy checker only. It checks local project folder placement against buyer-safe lockdown rules. "
    "It does not create legal advice, financial advice, binding terms, compliance certification, production validation, "
    "automated verdicts, free-pilot commitments, autonomous client action, truth validation, or hidden-mechanism claims."
)

RISK_TERMS = {
    "model_weights": ["model weights", "checkpoint", ".safetensors", ".ckpt"],
    "source_code": ["source code", "repo.zip", "repository"],
    "private_prompts": ["private prompt", "system prompt", "developer prompt"],
    "chain_of_thought": ["chain-of-thought", "chain of thought", "hidden reasoning", "scratchpad"],
    "hidden_activations": ["hidden activation", "activation dump", "latent state"],
    "secrets": ["password", "api key", "secret key", "credential", "token", "private key"],
    "legal_claims": ["legal advice", "legally defensible", "legal conclusion"],
    "compliance_claims": ["compliance certification", "certify compliance", "compliance certified"],
    "production_claims": ["production validation", "production validated", "automated verdict", "truth validation"],
}

SAFE_FOLDERS_FOR_RISK = {
    "model_weights": {"PROTECTED"},
    "source_code": {"PROTECTED"},
    "private_prompts": {"PROTECTED"},
    "chain_of_thought": {"PROTECTED"},
    "hidden_activations": {"PROTECTED"},
    "secrets": {"PROTECTED"},
    "legal_claims": {"DO_NOT_SEND", "PROTECTED"},
    "compliance_claims": {"DO_NOT_SEND", "PROTECTED"},
    "production_claims": {"DO_NOT_SEND", "PROTECTED"},
}

EXPECTED_FOLDERS = [
    "01_received_observable_traces",
    "02_sanitized_working_data",
    "03_review_notes",
    "04_candidate_discrepancy_memos",
    "05_delivery_packet",
    "06_post_pilot_feedback",
    "DO_NOT_SEND",
    "PROTECTED",
]

SOURCE_CODE_SUFFIXES = {".py", "source_code_suffix", ".ts", ".java"}

def scan_file(path: Path) -> str:
    if path.is_dir():
        return ""
    name = path.name.lower()
    suffix = path.suffix.lower()
    suffix_marker = " source_code_suffix " if suffix in SOURCE_CODE_SUFFIXES else ""
    if path.stat().st_size > 300_000:
        return name + suffix_marker
    try:
        return (name + suffix_marker + "\n" + path.read_text(encoding="utf-8", errors="ignore")).lower()
    except Exception:
        return name + suffix_marker

def check_project(project_dir: Path) -> dict:
    findings = []
    missing_folders = [folder for folder in EXPECTED_FOLDERS if not (project_dir / folder).exists()]

    for path in project_dir.rglob("*"):
        if path.is_dir():
            continue

        rel = path.relative_to(project_dir)
        top = rel.parts[0] if rel.parts else ""
        text = scan_file(path)

        for risk, terms in RISK_TERMS.items():
            hits = [term for term in terms if term in text]
            if not hits:
                continue
            allowed_folders = SAFE_FOLDERS_FOR_RISK.get(risk, set())
            if top not in allowed_folders:
                findings.append({
                    "file": str(rel),
                    "folder": top,
                    "risk": risk,
                    "hits": hits,
                    "status": "violation",
                    "recommended_action": "move_to_PROTECTED_or_DO_NOT_SEND_and_review",
                })

    status = "pass" if not findings and not missing_folders else "review"

    return {
        "engine": "folder_policy_checker_v1",
        "project_dir": str(project_dir),
        "status": status,
        "missing_folders": missing_folders,
        "finding_count": len(findings),
        "findings": findings,
        "claim_boundary": BOUNDARY,
    }

def main() -> int:
    parser = argparse.ArgumentParser(description="Check buyer-safe client project folder policy.")
    parser.add_argument("--project-dir", required=True)
    parser.add_argument("--output", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = check_project(Path(args.project_dir))

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print("Folder Policy Checker")
        print("=" * 72)
        print(f"status: {result['status']}")
        print(f"missing_folders: {len(result['missing_folders'])}")
        print(f"finding_count: {result['finding_count']}")
        if result["findings"]:
            print(json.dumps(result["findings"], ensure_ascii=False, indent=2, sort_keys=True))
        print()
        print(f"Boundary: {BOUNDARY}")

    return 0 if result["status"] == "pass" else 1

if __name__ == "__main__":
    raise SystemExit(main())
