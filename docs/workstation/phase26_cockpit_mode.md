# Phase 26 Cockpit Mode

Status: complete  
Date: 2026-06-28

## Purpose

Phase 26 adds `cockpit`, a local mission-mode context loader.

## Command

Repo-local:

`python3 tools/status/cockpit.py specshift`

Optional wrapper:

`cockpit specshift`

## Modes

- `cockpit specshift`
- `cockpit orchestra`
- `cockpit ddf`
- `cockpit outreach`
- `cockpit shutdown`

## What it loads

Each mode shows:

- relevant commands
- relevant paths
- relevant wiki/docs pages
- next actions
- active workplan state
- boundaries

## Artifacts

- `tools/status/cockpit.py`
- `memory_layer/wiki/operator_memory/workstation_command_center/cockpit_state.json`

## Boundary

Cockpit mode loads local context only.

It does not execute autonomous work, route externally, monitor production, authorize actions, or resolve truth.
