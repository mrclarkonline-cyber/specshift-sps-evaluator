# Terminal Kira Codex Escalation Policy

Status: active guidance

## Purpose

Define when Terminal Kira should recommend using Codex instead of continuing with Bash-only repair loops.

## Default rule

Terminal remains primary for:

- simple file edits
- status checks
- commits
- dependency records
- documentation updates
- wiki updates
- QA runs
- small deterministic patches

Codex should be recommended when a coding task becomes too complex or failure-prone for safe paste-based Bash.

## Primary escalation trigger

If coding fails more than once on the same prompt or same phase, Terminal Kira should recommend Codex.

Rule:

    2 failures on the same coding task = recommend Codex

## Other Codex triggers

Recommend Codex when:

- the Bash block is becoming too large or fragile
- nested quoting/heredoc complexity is causing errors
- the same classifier/test logic needs repeated structural repair
- multiple files need coordinated code edits
- a real refactor is needed instead of a patch
- tests fail because the design is wrong, not because of a typo
- a reusable module should replace duplicated local logic

## Do not use Codex for

- git status
- git add/commit/push
- wiki_landing
- dependency inventory
- brew/tap recording
- one-line shell fixes
- simple documentation updates
- running QA/security/survey commands

## Kira recommendation wording

When the trigger is met, Terminal Kira should say:

    This has failed twice on the same coding task. Use Codex for the code edit, then return to Terminal for tests, commit, push, and wiki_landing.

## Workflow

1. Terminal detects repeated failure.
2. Terminal Kira recommends Codex.
3. Codex performs bounded code edit only.
4. Terminal runs tests.
5. Terminal commits, pulls/rebases, pushes.
6. Terminal runs wiki_landing.

## Boundary

This is workstation workflow guidance only. It does not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdict, free pilot commitment, autonomous client action, surveillance authorization, truth validation, or hidden-mechanism claim.
