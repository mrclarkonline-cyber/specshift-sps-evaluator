# Phase 22 Artifact Promotion Gate

Status: complete  
Date: 2026-06-28

## Purpose

Phase 22 adds `promote_artifact`, a local gate for deciding whether an artifact is safe to promote.

## Command

Repo-local:

`python3 tools/status/promote_artifact.py <artifact> --target public --dry-run`

Optional wrapper:

`promote_artifact`

## Required checks

- Git clean status
- Claim Gauntlet report
- SHA-256 provenance
- timestamp
- file path
- public/private/protected boundary
- buyer-safe wording
- boundary language

## Outputs

- `memory_layer/wiki/operator_memory/workstation_command_center/artifact_promotion_gate_report.json`
- `memory_layer/wiki/operator_memory/workstation_command_center/artifact_promotion_history.jsonl`

## Boundary

This is a local workflow gate only.

It does not certify legal, compliance, scientific, factual, production, public-release, or buyer readiness.

Human review remains required.
