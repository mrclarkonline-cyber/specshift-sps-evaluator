# Phase 24 Local Provenance Vault

Status: complete  
Date: 2026-06-28

## Purpose

Phase 24 adds `provenance_vault`, a local provenance registry for important workstation artifacts.

## Command

Repo-local:

`python3 tools/status/provenance_vault.py --default-set`

Optional wrapper:

`provenance_vault`

## What it records

- SHA-256
- timestamp
- file path
- artifact status: public, private, protected, archive-caution
- linked wiki page
- git commit
- promotion history references

## Artifacts

- `memory_layer/wiki/operator_memory/workstation_command_center/provenance_vault.jsonl`
- `memory_layer/wiki/operator_memory/workstation_command_center/provenance_vault_report.json`

## Boundary

This is a local provenance record only.

It does not publish, promote, certify, validate, or externally route artifacts.
