# Phase 17 Mission Control Dashboard

Status: complete  
Date: 2026-06-28

## Command

`specshift_board`

Repo-local implementation:

`tools/status/specshift_board.py`

Optional wrapper:

`~/WORK/tools/orchestra/bin/specshift_board`

## Purpose

`specshift_board` is a read-only Mission Control dashboard.

It shows:

- active workplan
- active phase
- active tracker
- next action
- blockers
- closure rule
- Git state
- latest commit
- tracker output
- open risks
- boundary reminder

## Boundary

This is dashboarding only.

It does not replace `wiki_landing`, hand-code fireworks, execute actions, route externally, monitor production, or resolve truth.
