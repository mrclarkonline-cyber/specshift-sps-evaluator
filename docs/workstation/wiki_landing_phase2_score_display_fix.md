# wiki_landing Phase 2 Score Display Fix

Status: active
Date: 2026-06-28

## Issue

`wiki_landing` is a shell function from `~/.zshrc`, but the existing function body was not discoverable by the earlier patch pattern.

## Fix

A later override definition was appended to `~/.zshrc`.

The override makes the fireworks box display the live Phase 2 score from:

`tools/status/worldwide_pipeline_progress.py`

## Boundary

Display fix only. This does not claim live ingestion, validation, alerting, or production readiness.
