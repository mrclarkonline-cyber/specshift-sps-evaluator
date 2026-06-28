#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

BOUNDARY = (
    "Buyer artifact simulator only. It generates synthetic fixture artifacts for internal testing. "
    "It does not use real buyer data and does not create legal advice, financial advice, binding terms, "
    "compliance certification, production validation, automated verdicts, free-pilot commitments, "
    "autonomous client action, truth validation, or hidden-mechanism claims."
)

SYNTHETIC_CASES = [
    {
        "case_id": "clean_trace_file",
        "filename": "clean_workflow_trace.csv",
        "artifact_class": "trace data",
        "expected_decision_hint": "ACCEPT",
        "description": "Clean observable workflow trace file with timestamp, actor/system, step/action, claimed output, final state, and observable evidence.",
        "format": "csv",
        "content_kind": "trace",
    },
    {
        "case_id": "final_state_only_claim",
        "filename": "final_state_only_claim.md",
        "artifact_class": "final-state claim",
        "expected_decision_hint": "ACCEPT_NEEDS_TRACE_LINK",
        "description": "Claimed final state only, without supporting observable trace export.",
        "format": "md",
        "content_kind": "final_state",
    },
    {
        "case_id": "buyer_retained_label_file",
        "filename": "buyer_retained_labels.csv",
        "artifact_class": "buyer-retained label file",
        "expected_decision_hint": "HOLD_FOR_REVIEW",
        "description": "Buyer-retained label file for post-reveal reconciliation only.",
        "format": "csv",
        "content_kind": "labels",
    },
    {
        "case_id": "support_context",
        "filename": "field_dictionary_and_redaction_notes.md",
        "artifact_class": "support context",
        "expected_decision_hint": "ACCEPT",
        "description": "Field dictionary, schema notes, redaction explanation, and pseudonymization mapping.",
        "format": "md",
        "content_kind": "support",
    },
    {
        "case_id": "mixed_trace_label_artifact",
        "filename": "mixed_trace_and_labels.csv",
        "artifact_class": "mixed trace + label artifact",
        "expected_decision_hint": "HOLD_FOR_REVIEW",
        "description": "Mixed observable traces and buyer labels in a single file; should be split or held for review.",
        "format": "csv",
        "content_kind": "mixed_trace_labels",
    },
    {
        "case_id": "prohibited_prompt_dump",
        "filename": "private_prompt_dump.txt",
        "artifact_class": "prohibited/internal material",
        "expected_decision_hint": "REJECT",
        "description": "Private prompts, system prompt, hidden reasoning, and chain-of-thought examples.",
        "format": "txt",
        "content_kind": "prompt_dump",
    },
    {
        "case_id": "source_code_model_weight_request",
        "filename": "source_and_weights_request.md",
        "artifact_class": "prohibited/internal material",
        "expected_decision_hint": "REJECT",
        "description": "Buyer asks whether they can send source code, model weights, and checkpoints.",
        "format": "md",
        "content_kind": "source_weights",
    },
    {
        "case_id": "compliance_certification_request",
        "filename": "compliance_certification_request.md",
        "artifact_class": "out-of-scope material",
        "expected_decision_hint": "HOLD_FOR_REVIEW",
        "description": "Buyer asks SpecShift to certify that their AI is compliant and legally defensible.",
        "format": "md",
        "content_kind": "compliance_request",
    },
    {
        "case_id": "messy_spreadsheet_export",
        "filename": "messy_spreadsheet_export.csv",
        "artifact_class": "trace data",
        "expected_decision_hint": "NEEDS_SCOPING_OR_NORMALIZATION",
        "description": "Messy spreadsheet-style export with partial event fields and inconsistent headers.",
        "format": "csv",
        "content_kind": "messy_trace",
    },
    {
        "case_id": "out_of_scope_artifact",
        "filename": "production_incident_verdict_request.md",
        "artifact_class": "out-of-scope material",
        "expected_decision_hint": "HOLD_FOR_REVIEW",
        "description": "Production incident demand asking for automated verdict, truth validation, and production validation.",
        "format": "md",
        "content_kind": "production_incident",
    },
]

def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else ["empty"]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def write_case_artifact(case: dict, output_dir: Path) -> Path:
    path = output_dir / case["filename"]
    kind = case["content_kind"]

    if kind == "trace":
        write_csv(path, [
            {
                "record_id": "SIM-001",
                "event_time": "2026-01-01T10:00:00Z",
                "actor_system": "agent_pseudonym",
                "step_action": "task_started",
                "claimed_output": "workflow started",
                "final_state": "in_progress",
                "observable_evidence": "synthetic_source_row_1",
                "notes": "synthetic clean trace",
            },
            {
                "record_id": "SIM-001",
                "event_time": "2026-01-01T10:02:00Z",
                "actor_system": "agent_pseudonym",
                "step_action": "task_completed",
                "claimed_output": "workflow completed",
                "final_state": "complete",
                "observable_evidence": "synthetic_source_row_2",
                "notes": "synthetic clean trace",
            },
        ])
    elif kind == "labels":
        write_csv(path, [
            {"trace_id": "SIM-001", "buyer_label": "discrepancy", "buyer_adjudicator": "buyer_reviewer_1"},
            {"trace_id": "SIM-002", "buyer_label": "no_discrepancy", "buyer_adjudicator": "buyer_reviewer_1"},
        ])
    elif kind == "mixed_trace_labels":
        write_csv(path, [
            {"trace_id": "SIM-MIX-001", "event_time": "2026-01-01T10:00:00Z", "event_type": "task_started", "buyer_label": "discrepancy"},
            {"trace_id": "SIM-MIX-002", "event_time": "2026-01-01T10:05:00Z", "event_type": "task_closed", "buyer_label": "no_discrepancy"},
        ])
    elif kind == "messy_trace":
        write_csv(path, [
            {"Case Number": "M-1", "When": "yesterday-ish", "Thing That Happened": "agent says done", "Status???": "maybe complete"},
            {"Case Number": "M-2", "When": "", "Thing That Happened": "handoff failed", "Status???": "unknown"},
        ])
    else:
        text_map = {
            "final_state": "# Final-State Claim\n\nThe workflow is claimed complete, but no linked observable trace export is included.\n",
            "support": "# Field Dictionary and Redaction Notes\n\nFields: record_id, event_time, actor_system, step_action, final_state. All actors are pseudonymized.\n",
            "prompt_dump": "# Private Prompt Dump\n\nThis synthetic bad artifact pretends to include private prompts, system prompt, hidden reasoning, and chain-of-thought. Do not accept.\n",
            "source_weights": "# Source Code and Model Weights Request\n\nCan we send source code, model weights, checkpoints, and internal architecture for review?\n",
            "compliance_request": "# Compliance Certification Request\n\nCan SpecShift certify that our AI is compliant, safe, and legally defensible?\n",
            "production_incident": "# Production Incident Verdict Request\n\nWe need an automated verdict on a live production incident and production validation today.\n",
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text_map.get(kind, "# Synthetic Artifact\n"), encoding="utf-8")

    return path

def simulate(output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts = []

    for case in SYNTHETIC_CASES:
        path = write_case_artifact(case, output_dir)
        record = dict(case)
        record["path"] = str(path)
        record["synthetic"] = True
        record["created_at_utc"] = datetime.now(timezone.utc).isoformat()
        artifacts.append(record)

    manifest = {
        "engine": "buyer_artifact_simulator_v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "output_dir": str(output_dir),
        "artifact_count": len(artifacts),
        "artifacts": artifacts,
        "claim_boundary": BOUNDARY,
    }

    manifest_path = output_dir / "simulator_fixture_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest

def main() -> int:
    parser = argparse.ArgumentParser(description="Generate safe synthetic buyer artifact fixtures.")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    manifest = simulate(Path(args.output_dir))

    if args.json:
        print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print("Buyer Artifact Simulator")
        print("=" * 72)
        print(f"output_dir: {manifest['output_dir']}")
        print(f"artifact_count: {manifest['artifact_count']}")
        print()
        for artifact in manifest["artifacts"]:
            print(f"  - {artifact['case_id']}: {artifact['path']}")
        print()
        print(f"Boundary: {BOUNDARY}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
