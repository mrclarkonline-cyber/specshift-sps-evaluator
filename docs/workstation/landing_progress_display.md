# Landing Progress Display

Date created: 2026-06-27
Status: Draft v0.1
Scope: Required landing display behavior for Gold+ Bash workflows.

## Requirement

Every Gold+ Bash that lands a work block should show the workstation pipeline progress board before final status/fireworks.

The progress board should list every pipeline in the active workplan and include:

- item number
- DONE/TODO marker
- pipeline name
- expected file path
- total count complete
- percentage complete
- next pipeline

## Current Tool

Path:

tools/status/pipeline_progress.py

## Required Landing Pattern

Before the final fireworks box, run:

python3 tools/status/pipeline_progress.py

Then run:

git status --short

If final status is clean, show the full Terminal fireworks box.

## Reason

Ben should always be able to see:

- what landed
- what remains
- percentage progress
- next pipeline
- whether Git is clean

Terminal owes fireworks only when the landing is clean.
