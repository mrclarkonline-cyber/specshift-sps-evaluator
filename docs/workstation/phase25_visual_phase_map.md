# Phase 25 Visual Phase Map

Status: complete  
Date: 2026-06-28

## Purpose

Phase 25 adds `phase_map`, a read-only terminal map of registered command-center phases.

## Command

Repo-local:

`python3 tools/status/phase_map.py`

Optional wrapper:

`phase_map`

## Legend

- ✅ complete
- 🟡 registered or partial
- 🎯 active
- 🔒 protected
- ⚠️ caution or held
- 💤 parked

## Artifacts

- `tools/status/phase_map.py`
- `memory_layer/wiki/operator_memory/workstation_command_center/phase_map_state.json`

## Boundary

This is a read-only local visualization.

It does not execute commands, alter state, route externally, monitor production, or resolve truth.

`wiki_landing` owns fireworks.
