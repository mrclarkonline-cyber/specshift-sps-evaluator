#!/usr/bin/env bash
set -euo pipefail

REPORT="docs/workstation/workstation_validation_sweep_latest.md"
RUN_TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

mkdir -p docs/workstation reports/fast_relevance

: > "$REPORT"

log() {
  printf '%s\n' "$*" | tee -a "$REPORT"
}

run_step() {
  local name="$1"
  shift

  log ""
  log "### $name"
  log ""
  log '```text'

  set +e
  "$@" >> "$REPORT" 2>&1
  local code=$?
  set -e

  log '```'
  log ""
  if [ "$code" -eq 0 ]; then
    log "Result: PASS"
  else
    log "Result: WARN_EXIT_$code"
  fi

  return 0
}

log "# Workstation Validation Sweep"
log ""
log "Generated at UTC: $RUN_TS"
log ""
log "## Scope"
log ""
log "This sweep validates the local SpecShift workstation stack, the Orchestra baseline, and the first public-source pipeline pass."
log ""
log "The sweep is defensive/public-source only. It does not perform active probing, exploit generation, individual tracking, automated trading, legal advice, medical advice, or automated operational action."
log ""
log "## Validation Steps"

run_step "Git status before validation" git status --short
run_step "Orchestra audit" python3 tools/orchestra/orchestra_audit.py
run_step "Orchestra status" tools/status/orchestra_status.sh
run_step "Pipeline registry check" python3 tools/pipelines/pipeline_registry_check.py
run_step "Source health check" python3 tools/pipelines/source_health_check.py
run_step "Pipeline progress board" python3 tools/status/pipeline_progress.py

log ""
log "## Dry-Run Validation"
run_step "CISA KEV dry-run" python3 tools/pipelines/cisa_kev_fetch.py --dry-run --limit 3
run_step "USGS earthquake dry-run" python3 tools/pipelines/usgs_earthquake_fetch.py --dry-run --limit 3
run_step "Federal Register dry-run" python3 tools/pipelines/federal_register_fetch.py --dry-run --limit 3 --days 7
run_step "arXiv dry-run" python3 tools/pipelines/arxiv_fetch.py --dry-run --limit 3
run_step "NOAA/NWS alerts dry-run" python3 tools/pipelines/noaa_alerts_fetch.py --dry-run --limit 3
run_step "Hugging Face metadata dry-run" python3 tools/pipelines/huggingface_metadata_fetch.py --dry-run --limit 3
run_step "SEC EDGAR dry-run" python3 tools/pipelines/sec_edgar_fetch.py --dry-run --limit 3
run_step "World news RSS dry-run" python3 tools/pipelines/world_news_rss_fetch.py --dry-run --limit 3
run_step "World news RSS verify-only" python3 tools/pipelines/world_news_rss_fetch.py --verify-only

log ""
log "## Guarded Live Fetch Validation"
log ""
log "Live fetches below are guarded, public-source, low-limit checks. Network failure is recorded as WARN rather than treated as repo failure."

run_step "CISA KEV live fetch" python3 tools/pipelines/cisa_kev_fetch.py --limit 3
run_step "USGS earthquake live fetch" python3 tools/pipelines/usgs_earthquake_fetch.py --limit 3
run_step "Federal Register live fetch" python3 tools/pipelines/federal_register_fetch.py --limit 3 --days 7
run_step "arXiv live fetch" python3 tools/pipelines/arxiv_fetch.py --limit 3
run_step "NOAA/NWS alerts live fetch" python3 tools/pipelines/noaa_alerts_fetch.py --limit 3
run_step "Hugging Face metadata live fetch" python3 tools/pipelines/huggingface_metadata_fetch.py --limit 3
run_step "SEC EDGAR live fetch" python3 tools/pipelines/sec_edgar_fetch.py --limit 3
run_step "World news RSS live fetch" python3 tools/pipelines/world_news_rss_fetch.py --limit 3

log ""
log "## Local Synthesis Validation"
run_step "Daily digest generation" python3 tools/pipelines/daily_digest.py
run_step "SpecShift buyer trigger watch" python3 tools/pipelines/specshift_buyer_trigger_watch.py
run_step "Finance integrity watch" python3 tools/pipelines/finance_integrity_watch.py
run_step "Contradiction detector" python3 tools/pipelines/contradiction_detector.py
run_step "Claim-overstatement detector" python3 tools/pipelines/claim_overstatement_detector.py
run_step "Low-frequency anomaly detector" python3 tools/pipelines/low_frequency_anomaly_detector.py
run_step "Claim safety gate" python3 tools/pipelines/claim_safety_gate.py --path reports/fast_relevance

log ""
log "## Final Local Status"
run_step "Workstation status" tools/status/specshift_status.sh
run_step "Git status after validation" git status --short

log ""
log "## Validation Interpretation"
log ""
log "PASS means the local step completed."
log ""
log "WARN means the step returned nonzero and should be inspected, but the sweep continued so the whole stack could be observed."
log ""
log "Live network fetch WARNs can be caused by upstream network/API availability and do not necessarily indicate code failure."
log ""
log "## Safety Boundary"
log ""
log "No generated report should be treated as a validated conclusion without human review and source inspection."
log ""
log "## Kira Recommendation"
log ""
log "If this sweep completes with the repo clean after committing the validation report, the workstation stack has moved from implementation-complete to validation-baselined."
