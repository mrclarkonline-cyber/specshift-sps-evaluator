# Phase 20 Phil Morale Layer

Status: complete  
Date: 2026-06-28

## Purpose

Phase 20 adds Phil as a safe morale and pacing layer.

Phil speaks only after serious checks pass.

## Command

Repo-local:

`python3 tools/status/phil_morale_layer.py`

Optional wrapper:

`phil_summary`

## Rules

- If Git is dirty, Phil holds.
- If Kira severity is high, Phil holds.
- If the command-center workplan is missing, Phil holds.
- Phil never executes commands.
- Phil never overrides Kira.
- Phil never replaces `wiki_landing`.
- Phil gives human-friendly feedback only.

## Boundary

Phil morale feedback is local pacing only.

It does not execute commands, route externally, monitor production, validate truth, authorize autonomous action, or provide workflow authority.
