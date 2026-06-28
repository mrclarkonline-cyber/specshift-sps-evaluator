# Cockpit Read-Only Default Fix

Status: complete  
Date: 2026-06-28

## Issue

Running `cockpit specshift` displayed the cockpit correctly, but it rewrote:

`memory_layer/wiki/operator_memory/workstation_command_center/cockpit_state.json`

That made Git dirty, so `wiki_landing` correctly withheld fireworks.

## Fix

`cockpit` is now read-only by default.

It only writes `cockpit_state.json` when explicitly run with:

`--write-state`

## Rule

Viewing cockpit mode should not dirty the repo.

State files should be written only when intentionally updating registered state.
