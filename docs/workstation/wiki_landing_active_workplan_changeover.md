# wiki_landing Active Workplan Changeover

Status: active  
Date: 2026-06-28

## Issue

`wiki_landing` was still displaying the Worldwide Phase 2 tracker after Phase 2 had closed at 100%.

The first patch attempt failed because `wiki_landing` resolved as a shell function or alias, not a direct executable file path.

## Fix

Use `active_workplan.json` as the landing router:

`memory_layer/wiki/operator_memory/active_workplan.json`

Current active tracker:

`tools/status/worldwide_phase3_progress.py`

Previous tracker:

`tools/status/worldwide_pipeline_progress.py`

## Rule

Phase 2 remains preserved as closure evidence, but it should not be the active displayed workplan once Phase 3 is registered.

## Boundary

Phase 3 is bounded live-sample runway work only. It does not claim production monitoring, content validation, alert readiness, autonomous action, or truth resolution.
