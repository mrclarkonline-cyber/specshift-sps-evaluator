#!/usr/bin/env bash
set -euo pipefail

# Terminal Kira → Codex Referral Gate
# Gold+ boundary:
#   Kira controls policy/workplan/escalation.
#   Codex is implementation-only.
#   QA is the executable gate.
#   Human operator is final authority.

task="${*:-}"

if [[ -z "$task" ]]; then
  cat <<'HELP'
Usage:
  tools/workstation/kira_codex_referral_gate.sh "task to evaluate before Codex referral"

Allowed:
  code, tests, fixtures, docs, wiki updates, refactors, diff review, bounded QA runs

Blocked:
  legal/financial advice, binding terms, compliance certification, production validation,
  buyer/client promises, autonomous client action, final approval, truth validation

Decision model:
  Kira = controller
  Codex = bounded implementation agent
  QA = gate
  Human = final authority
HELP
  exit 0
fi

normalized="$(printf '%s' "$task" | tr '[:upper:]' '[:lower:]')"

blocked_re='legal advice|financial advice|binding terms|compliance certification|certify compliance|production validation|production ready|production readiness|buyer-facing promise|client promise|client commitment|autonomous client|contact client|send to buyer|approve buyer|final authority|truth validation|certify correctness|guarantee|guaranteed|deploy to production'
sensitive_re='legal|financial|compliance|production|buyer|client|vendor|contract|terms|guarantee|certify|approve|deploy'
implementation_re='code|script|test|pytest|fixture|docs|documentation|wiki|refactor|diff|lint|qa|smoke check|regression|implementation|broken link|claim scan|audit gate'

if [[ "$normalized" =~ $blocked_re ]]; then
  cat <<'BLOCKED'
BLOCKED: Do not refer this task to Codex.

Codex is implementation-only. It must not make legal, financial, compliance,
production-readiness, buyer-facing, autonomous-client, truth-validation, or final
authority decisions.

Safe rewrite:
  Ask Codex to edit files, add tests, update docs, inspect a diff, or run bounded
  local checks without certifying status or making promises.
BLOCKED
  exit 2
fi

if [[ "$normalized" =~ $sensitive_re && ! "$normalized" =~ $implementation_re ]]; then
  cat <<'REVIEW'
REVIEW REQUIRED: Reframe before Codex referral.

This task uses authority-adjacent language but is not clearly implementation-only.
Kira should rewrite it as a bounded repo task before handing it to Codex.
REVIEW
  exit 1
fi

cat <<'ALLOWED'
ALLOWED: May refer to Codex with this prepend:

You are Codex acting as a bounded repo-editing implementation agent.
You may edit code, tests, fixtures, docs, wiki, and local workflow files.
You may run bounded local QA checks.
You must not create legal advice, financial advice, binding terms, compliance
certification, production validation, automated verdicts, buyer/client promises,
autonomous client action, truth validation, or hidden-mechanism claims.
Kira remains the policy/workplan controller.
The QA harness remains the executable gate.
The human operator remains final authority.
ALLOWED
