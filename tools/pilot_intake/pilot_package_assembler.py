#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

BOUNDARY = (
    "Pilot package assembler only. It creates a review workspace scaffold from accepted observable artifacts. "
    "It does not create legal advice, financial advice, binding terms, compliance certification, production validation, "
    "automated verdicts, free-pilot commitments, autonomous client action, truth validation, or hidden-mechanism claims."
)

PACKAGE_FILES = {
    "01_received_manifest.md": "# Received Manifest\n\nStatus: draft\n\nList buyer-provided observable artifacts only.\n\n",
    "02_scope_boundary_check.md": "# Scope Boundary Check\n\n- [ ] buyer-controlled\n- [ ] observable-only\n- [ ] exported traces only\n- [ ] no model weights\n- [ ] no source code\n- [ ] no private prompts\n- [ ] no hidden activations\n- [ ] no private chain-of-thought\n- [ ] buyer retains labels\n- [ ] human adjudication retained\n- [ ] candidate-discrepancy memos only\n- [ ] no automated verdict\n- [ ] no production validation claim\n- [ ] no legal/compliance/certification claim\n- [ ] no free pilot\n\n",
    "03_trace_review_workspace.md": "# Trace Review Workspace\n\nUse normalized observable traces only.\n\n| Trace ID | Step/action | Claimed output | Final state | Candidate prompt | Limitation |\n|---|---|---|---|---|---|\n|  |  |  |  |  |  |\n\n",
    "04_candidate_discrepancy_memo_draft.md": "# Candidate-Discrepancy Memo Draft\n\nThis is a candidate-discrepancy memo only. It is not an automated verdict.\n\n## Candidate prompts\n\n| Candidate ID | Trace reference | Candidate prompt | Limitation | Buyer review needed |\n|---|---|---|---|---|\n| CD-001 |  |  |  | yes |\n\n",
    "05_limitations_and_non_claims.md": "# Limitations and Non-Claims\n\nThis package does not provide:\n\n- legal advice\n- financial advice\n- binding terms\n- compliance certification\n- production validation\n- automated verdicts\n- truth validation\n- autonomous client action\n\n",
    "06_buyer_questions.md": "# Buyer Questions\n\n- What final adjudication process will the buyer use?\n- Are labels retained by the buyer?\n- Is more observable context needed?\n- Should the package be delivered, parked, rescoped, or paused for professional review?\n\n",
}

def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def assemble(project_dir: Path, package_name: str = "pilot_review_package") -> dict:
    package_dir = project_dir / "07_delivery" / package_name
    package_dir.mkdir(parents=True, exist_ok=True)

    created = []
    for filename, content in PACKAGE_FILES.items():
        path = package_dir / filename
        write(path, content)
        created.append(str(path))

    manifest = {
        "engine": "pilot_package_assembler_v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "project_dir": str(project_dir),
        "package_dir": str(package_dir),
        "created_files": created,
        "required_boundaries": [
            "buyer-controlled",
            "observable-only",
            "exported traces only",
            "buyer retains labels",
            "human adjudication retained",
            "candidate-discrepancy memos only",
            "no automated verdict",
            "no production validation claim",
            "no legal/compliance/certification claim",
            "no free pilot"
        ],
        "claim_boundary": BOUNDARY,
    }
    manifest_path = package_dir / "package_manifest.json"
    write(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    created.append(str(manifest_path))
    manifest["created_files"] = created
    return manifest

def main() -> int:
    parser = argparse.ArgumentParser(description="Assemble a buyer-safe pilot review package scaffold.")
    parser.add_argument("--project-dir", required=True, help="Buyer-safe pilot project directory")
    parser.add_argument("--package-name", default="pilot_review_package")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = assemble(Path(args.project_dir), args.package_name)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print("Pilot Package Assembler")
        print("=" * 72)
        print(f"project_dir: {result['project_dir']}")
        print(f"package_dir: {result['package_dir']}")
        print()
        for item in result["created_files"]:
            print(f"  - {item}")
        print()
        print(f"Boundary: {BOUNDARY}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
