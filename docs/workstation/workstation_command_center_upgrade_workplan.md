# Workstation Command Center Upgrade Workplan

Status: registered  
Date: 2026-06-28

## Purpose

Upgrade the terminal from a repo/workflow runner into a civilian-safe command center.

The point is not more tools. The point is less guessing.

The machine should know:

- what phase it is in
- what it is allowed to say
- what it is not allowed to touch
- what the next bounded action is
- when Git is clean
- when the workplan is complete
- when the user gets fireworks

## Registered upgrade sequence

1. Mission Control dashboard: `specshift_board`
2. Active workplan brain: `active_workplan.json`
3. Kira recommendation engine
4. Phil morale layer
5. Claim-overstatement detector: `claim_gauntlet`
6. Artifact promotion gate: `promote_artifact`
7. One-command nightly shutdown: `close_universe`
8. Local provenance vault: `provenance_vault`
9. Visual phase map: `phase_map`
10. SpecShift cockpit mode: `cockpit`

## Active tracker

`tools/status/workstation_command_center_progress.py`

## Boundary

This workplan registers local workstation upgrades only.

It does not implement autonomous action, production monitoring, external routing, hidden escalation, surveillance, targeting, or truth-resolution systems.

## House rule

All completed Terminal/repo/wiki work ends with:

`wiki_landing`

No custom fireworks.
