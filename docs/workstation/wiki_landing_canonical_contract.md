# wiki_landing Canonical Contract

Status: active
Date: 2026-06-28

## Rule

All Terminal/repo/wiki work should end by calling the canonical `wiki_landing` helper.

Do not hand-code custom final fireworks, progress boxes, or Kira recommendation endings inside each Bash.

## Active Workplan Selection

`wiki_landing` must not infer the active workplan merely because a progress script exists.

The optional marker file is:

`memory_layer/wiki/operator_memory/ACTIVE_WORKPLAN`

Supported marker values:

- `worldwide_phase2`
- `worldwide_phase3`
- `pipeline_implementation`

If the marker is absent, `wiki_landing` should report no active workplan selected and recommend stopping or naming a new work block.

## Canonical Fireworks Sentence

`Wiki updated. Git happy. ___% progress through your workplan`

## Ownership

`wiki_landing` owns Git status, recent commits, workplan progress, Kira recommendation, and clean-status fireworks.

## Bash Style

Use this pattern:

```bash
cd ~/specshift_terminal_intelligence || exit 1
set -euo pipefail

# do the work
# stage / commit / pull --rebase / push when appropriate

wiki_landing
```
