#!/usr/bin/env bash
set -euo pipefail

echo "======================================================================="
echo "SpecShift Civilian Intelligence Workstation Status"
echo "======================================================================="
echo

echo "=== Git ==="
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "branch: $(git branch --show-current)"
  short_status="$(git status --short)"
  if [ -z "$short_status" ]; then
    echo "status: clean"
  else
    echo "status: dirty"
    printf '%s\n' "$short_status"
  fi

  echo
  echo "latest commits:"
  git log --oneline -5 || true

  echo
  echo "remote:"
  git remote -v | sed -n '1,4p' || true
else
  echo "FAIL not inside a git repo"
fi

echo
echo "=== Workstation Docs ==="
for f in \
  docs/workstation/fast_relevance_pipelines.md \
  docs/workstation/unified_pipeline_data_schema.md \
  docs/workstation/pipeline_safety_and_provenance_guardrails.md \
  docs/workstation/ai_pipeline_recommendation_synthesis.md \
  docs/workstation/fast_pipeline_mvp_7_day_build_plan.md \
  docs/workstation/minimum_viable_source_registry.md \
  docs/workstation/landing_progress_display.md \
  workplans/workstation_pipeline_execution_workplan_2026-06-27.md
do
  if [ -s "$f" ]; then
    echo "PASS $f"
  else
    echo "MISSING $f"
  fi
done

echo
echo "=== Pipeline Progress ==="
if [ -x tools/status/pipeline_progress.py ]; then
  python3 tools/status/pipeline_progress.py
elif [ -s tools/status/pipeline_progress.py ]; then
  python3 tools/status/pipeline_progress.py
else
  echo "MISSING tools/status/pipeline_progress.py"
fi

echo
echo "=== Core Artifact Count ==="
if [ -d docs/specshift_core ]; then
  find docs/specshift_core -maxdepth 1 -type f -name "*.md" | wc -l | awk '{print "core_md_files: " $1}'
else
  echo "MISSING docs/specshift_core"
fi

echo
echo "=== Finance Outreach Files ==="
for f in \
  outreach/finance_integrity_review/README.md \
  outreach/finance_integrity_review/finance_integrity_first_send_email.md \
  outreach/finance_integrity_review/finance_integrity_outreach_tracker.csv \
  outreach/finance_integrity_review/finance_integrity_initial_target_shortlist.md
do
  if [ -s "$f" ]; then
    echo "PASS $f"
  else
    echo "MISSING $f"
  fi
done

echo
echo "=== Pipeline Registry Validation ==="
if [ -x tools/pipelines/pipeline_registry_check.py ]; then
  python3 tools/pipelines/pipeline_registry_check.py || true
elif [ -s tools/pipelines/pipeline_registry_check.py ]; then
  python3 tools/pipelines/pipeline_registry_check.py || true
else
  echo "MISSING tools/pipelines/pipeline_registry_check.py"
fi

echo
echo "=== Source Health Baseline ==="
if [ -x tools/pipelines/source_health_check.py ]; then
  python3 tools/pipelines/source_health_check.py || true
elif [ -s tools/pipelines/source_health_check.py ]; then
  python3 tools/pipelines/source_health_check.py || true
else
  echo "MISSING tools/pipelines/source_health_check.py"
fi

echo
echo "=== Environment ==="
echo "python3: $(python3 --version 2>/dev/null || echo missing)"
echo "shell: ${SHELL:-unknown}"

echo
echo "=== Recommended Commands ==="
for cmd in git python3 jq rg fd tree gh shellcheck; do
  if command -v "$cmd" >/dev/null 2>&1; then
    echo "PASS $cmd -> $(command -v "$cmd")"
  else
    echo "MISSING $cmd"
  fi
done

echo
echo "=== Orchestra / Fetch_ET Commands ==="
for cmd in orchestra_probe orchestra_conduct orchestra_signals orchestra_board radar_run radar_status radar_open orchestra_sources orchestra_fetch orchestra_global_observation fetch_et; do
  if command -v "$cmd" >/dev/null 2>&1; then
    echo "PASS $cmd -> $(command -v "$cmd")"
  else
    echo "MISSING $cmd"
  fi
done

echo
echo "=== Next Recommended Action ==="
echo "Build the next TODO item shown in Pipeline Progress."
echo

echo "======================================================================="
echo "Status complete. Terminal owes fireworks on clean push."
echo "======================================================================="
