# Phase 19 Kira Recommendation Engine

Status: complete  
Date: 2026-06-28

## Purpose

Phase 19 upgrades Kira from generic advice into a rule-based local recommendation engine.

## Command

Repo-local:

`python3 tools/status/kira_recommendation_engine.py`

Optional wrapper:

`kira_recommend`

## Inputs

- `memory_layer/wiki/operator_memory/active_workplan.json`
- active tracker progress
- Git status
- blockers
- risk state
- next action
- active phase

## Rules

- If Git is dirty: commit, park, or restore before clean landing.
- If blockers exist: resolve or park blockers first.
- If claim or boundary risk is elevated: run claim-overstatement scan.
- If progress is 100%: close or park the work block.
- If partial: use the active next action.
- If next action is missing: update the active workplan brain.

## Boundary

Kira recommendations are local workflow guidance only.

They do not execute commands, route externally, monitor production, validate truth, or authorize autonomous action.
