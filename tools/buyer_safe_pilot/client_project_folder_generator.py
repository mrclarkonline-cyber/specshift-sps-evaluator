#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_ROOT = Path("client_projects")

BOUNDARY_TEXT = """# Project Boundary

This project folder is for a buyer-controlled observable-only pilot scaffold.

## Required boundaries

- buyer-controlled
- observable-only
- exported traces only
- no model weights
- no source code
- no private prompts
- no hidden activations
- no private chain-of-thought
- buyer retains labels
- buyer retains final adjudication
- candidate-discrepancy memos only
- no automated verdict
- no production validation claim
- no legal/compliance/certification claim
- no free pilots

## Professional threshold

If procurement, contract terms, paid pilot, licensing, exclusivity, acquisition, IP assignment, data transfer, or money movement becomes real, engage qualified legal and CPA support before proceeding alone.

## Boundary

This folder is a local project scaffold only.

It does not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdicts, free-pilot commitments, or autonomous client action.
"""

README_TEXT = """# Buyer-Safe Pilot Project

This folder was created by client_project_folder_generator.py.

## Folder purpose

Organize a buyer-safe observable-only pilot from intake through delivery without requesting protected internals or overclaiming results.

## Folder map

- 00_admin: local project notes, scope, contacts, and professional-review flags
- 01_intake: buyer intake questionnaire and scope artifacts
- 02_buyer_exports_observable_only: buyer-provided observable trace exports only
- 03_labels_buyer_controlled: buyer-retained labels or adjudication references, if provided
- 04_redaction_and_field_dictionary: field dictionary, redaction notes, pseudonymization notes
- 05_working_review: internal working review notes
- 06_candidate_discrepancy_memos: candidate-discrepancy memo drafts
- 07_delivery: delivery checklist and final bounded delivery package
- 08_provenance: hashes, intake records, deletion/return status
- 09_archive_or_delete: closeout, retention, return, deletion, or archive-caution notes
- DO_NOT_SEND: material not approved for external sending
- PROTECTED: restricted material requiring review before use

## Boundary

Candidate-discrepancy memos are review scaffolds only.

They are not automated verdicts, legal/compliance/certification conclusions, production validation, or truth validation.
"""

MANIFEST_BOUNDARY = "Project manifest only. It does not authorize data transfer, retention, public use, legal/compliance claims, paid pilot terms, or autonomous client action."

def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "unnamed_client"

def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def main() -> int:
    parser = argparse.ArgumentParser(description="Create a buyer-safe SpecShift pilot project folder.")
    parser.add_argument("client_name", help="Client or project name")
    parser.add_argument("--workflow", default="", help="Workflow under review")
    parser.add_argument("--root", default=str(DEFAULT_ROOT), help="Root project directory")
    parser.add_argument("--dry-run", action="store_true", help="Show paths without creating files")
    args = parser.parse_args()

    now = datetime.now(timezone.utc).isoformat()
    slug = slugify(args.client_name)
    project_root = Path(args.root) / slug

    folders = [
        "00_admin",
        "01_intake",
        "02_buyer_exports_observable_only",
        "03_labels_buyer_controlled",
        "04_redaction_and_field_dictionary",
        "05_working_review",
        "06_candidate_discrepancy_memos",
        "07_delivery",
        "08_provenance",
        "09_archive_or_delete",
        "DO_NOT_SEND",
        "PROTECTED",
    ]

    manifest = {
        "engine": "client_project_folder_generator_v1",
        "created_at_utc": now,
        "client_name": args.client_name,
        "project_slug": slug,
        "workflow": args.workflow,
        "project_root": str(project_root),
        "folders": folders,
        "required_boundaries": [
            "buyer-controlled",
            "observable-only",
            "exported traces only",
            "no model weights",
            "no source code",
            "no private prompts",
            "no hidden activations",
            "no private chain-of-thought",
            "buyer retains labels",
            "buyer retains final adjudication",
            "candidate-discrepancy memos only",
            "no automated verdict",
            "no production validation claim",
            "no legal/compliance/certification claim",
            "no free pilots"
        ],
        "professional_threshold": "If procurement, contract terms, paid pilot, licensing, exclusivity, acquisition, IP assignment, data transfer, or money movement becomes real, engage qualified legal and CPA support before proceeding alone.",
        "claim_boundary": MANIFEST_BOUNDARY,
    }

    print("Buyer-Safe Pilot Project Folder Generator")
    print("=" * 72)
    print(f"Client/project: {args.client_name}")
    print(f"Project root:   {project_root}")
    print(f"Dry run:        {args.dry_run}")
    print()

    for folder in folders:
        print(f"  - {project_root / folder}")

    if args.dry_run:
        print()
        print("Dry run only. No files created.")
        return 0

    for folder in folders:
        (project_root / folder).mkdir(parents=True, exist_ok=True)

    write_text(project_root / "README.md", README_TEXT)
    write_text(project_root / "PROJECT_BOUNDARY.md", BOUNDARY_TEXT)
    write_text(project_root / "00_admin" / "scope_notes.md", "# Scope Notes\n\nStatus: draft\n\n")
    write_text(project_root / "00_admin" / "professional_threshold_flags.md", "# Professional Threshold Flags\n\nCheck before proceeding:\n\n- procurement\n- contract terms\n- paid pilot\n- licensing\n- exclusivity\n- acquisition\n- IP assignment\n- data transfer\n- money movement\n\nIf any are real, engage qualified legal and CPA support before proceeding alone.\n")
    write_text(project_root / "01_intake" / "PLACE_BUYER_INTAKE_HERE.md", "# Buyer Intake\n\nPlace completed buyer intake questionnaire here.\n")
    write_text(project_root / "02_buyer_exports_observable_only" / "ONLY_OBSERVABLE_EXPORTS_HERE.md", "# Observable Exports Only\n\nDo not place model weights, source code, private prompts, hidden activations, private chain-of-thought, credentials, or secrets here.\n")
    write_text(project_root / "03_labels_buyer_controlled" / "BUYER_RETAINS_LABELS.md", "# Buyer-Retained Labels\n\nLabels and final adjudication remain buyer-controlled.\n")
    write_text(project_root / "04_redaction_and_field_dictionary" / "FIELD_DICTIONARY_AND_REDACTION_NOTES.md", "# Field Dictionary and Redaction Notes\n\nDocument fields, redactions, pseudonymization, and removed sensitive data here.\n")
    write_text(project_root / "06_candidate_discrepancy_memos" / "MEMOS_ARE_CANDIDATE_ONLY.md", "# Candidate Memos Only\n\nMemos are review prompts only, not automated verdicts or findings.\n")
    write_text(project_root / "07_delivery" / "DELIVERY_BOUNDARY.md", "# Delivery Boundary\n\nDelivery package must preserve limitations, human review, and no legal/compliance/certification/production-validation claims.\n")
    write_text(project_root / "08_provenance" / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    write_text(project_root / "09_archive_or_delete" / "RETENTION_RETURN_DELETE_STATUS.md", "# Retention / Return / Delete Status\n\nDocument final retention, return, deletion, or archive-caution status here.\n")
    write_text(project_root / "DO_NOT_SEND" / "README.md", "# DO NOT SEND\n\nMaterial in this folder is not approved for external sending.\n")
    write_text(project_root / "PROTECTED" / "README.md", "# PROTECTED\n\nRestricted material requiring review before use.\n")

    print()
    print(f"Created project scaffold: {project_root}")
    print("Boundary: local project scaffold only. No legal/compliance/certification/production-validation claims.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
