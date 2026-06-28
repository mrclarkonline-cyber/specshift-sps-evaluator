# wiki_landing Dynamic Phase 2 Footer Fix

Status: Applied to shell function
Location: ~/.zshrc

Issue found:
The stale footer was not an exact hardcoded string. It was dynamically generated from:

- `${pct}% progress through your workplan`
- `tools/status/pipeline_progress.py`

Fix:
The landing footer now distinguishes Phase 1 from Phase 2.

- Phase 1 workstation/orchestra pipelines: complete
- Phase 2 worldwide expansion: registered and visible, not yet implemented
- Next build group: WHO, ReliefWeb/OCHA, GDACS, World Bank, IMF, EU Open Data, ECDC
