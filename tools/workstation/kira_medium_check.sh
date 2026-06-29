#!/usr/bin/env bash
set -euo pipefail

charter="docs/kira/medium_consistency_charter.md"
gate="tools/workstation/kira_codex_referral_gate.sh"

missing=0

if [[ ! -f "$charter" ]]; then
  echo "MISSING: $charter"
  missing=1
else
  echo "OK: $charter"
fi

if [[ ! -x "$gate" ]]; then
  echo "MISSING OR NOT EXECUTABLE: $gate"
  missing=1
else
  echo "OK: $gate"
fi

required_phrases=(
  "Kira = controller"
  "Codex = bounded implementation agent"
  "QA harness = executable truth gate"
  "Human operator = final authority"
  "Kira must not:"
  "Before referring work to Codex"
  "Escalate to the human operator"
)

for phrase in "${required_phrases[@]}"; do
  if ! grep -Fq "$phrase" "$charter"; then
    echo "MISSING PHRASE: $phrase"
    missing=1
  else
    echo "OK PHRASE: $phrase"
  fi
done

if [[ "$missing" -ne 0 ]]; then
  echo "FAIL: Kira medium consistency check failed."
  exit 1
fi

echo "PASS: Kira medium consistency charter is present and aligned."
