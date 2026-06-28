# wiki_landing Phase 2 Patch Note

Status: Applied to shell function
Location: ~/.zshrc

`wiki_landing` is a shell function loaded from the user's zsh configuration, not a repo-local script.

It has been patched to print:

- Worldwide Phase 2 progress
- per-pipeline registered status
- implementation percentage
- next worldwide build group

The canonical rule remains:

Bash blocks should do the work, then end with `wiki_landing`.
