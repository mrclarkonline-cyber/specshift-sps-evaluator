# SpecShift Terminal Complete Capability Map

Status: complete
Date: 2026-06-28

## Purpose

This page records what the SpecShift terminal can now do and how to use it.

It is the canonical operator-facing capability map for the local workstation.

## Safe overall claim

This terminal now supports a bounded SpecShift workstation: command center, active workplan brain, claim gates, promotion gates, provenance, cockpit modes, worldwide analytical scaffold, forecast/negative-space review scaffold, client intake/delivery scaffold, professional lawyer/CPA readiness, and regulatory/procurement readiness documentation.

## Canonical rules

- All Terminal/repo/wiki work ends with wiki_landing.
- Do not hand-code custom fireworks.
- Do not hardcode phase numbers inside wiki_landing.
- active_workplan.json is the active state source.
- Cockpit is read-only by default.
- Claim Gauntlet and Promotion Gate are gates, not certifications.
- Human review remains required.
- Professional review is required before procurement, paid pilot, contract terms, budget, money movement, protected method disclosure, or regulated/certification claims.

## Quickstart

### See current state

```bash
python3 tools/status/specshift_board.py
```

### End repo/wiki work cleanly

```bash
wiki_landing
```

### Check active workplan brain

```bash
python3 tools/status/active_workplan_brain_check.py
```

### Ask Kira for next action

```bash
python3 tools/status/kira_recommendation_engine.py
```

### Run claim language scan

```bash
python3 tools/status/claim_gauntlet.py
```

### Gate an artifact before public/client use

```bash
python3 tools/status/promote_artifact.py <artifact> --target public --dry-run
```

### Register provenance

```bash
python3 tools/status/provenance_vault.py --default-set
```

### View phase map

```bash
python3 tools/status/phase_map.py
```

### Open cockpit

```bash
python3 tools/status/cockpit.py specshift
```

### Shutdown summary

```bash
python3 tools/status/close_universe.py
```

### Check client delivery package

```bash
python3 tools/status/specshift_client_intake_delivery_progress.py
```

### Check lawyer/CPA readiness

```bash
python3 tools/status/professional_readiness_progress.py
```

### Check regulatory/procurement readiness

```bash
python3 tools/status/regulatory_certification_readiness_progress.py
```

## Complete capability list

### 1. Mission Control / Command Center

**Capability:** Open a full local workstation status board.

**Command:**

```bash
python3 tools/status/specshift_board.py
```

**Optional wrapper:** `specshift_board`

**Primary artifacts:**

- `tools/status/specshift_board.py` (FOUND)
- `memory_layer/wiki/operator_memory/active_workplan.json` (FOUND)

**What it does:**

- shows active workplan
- shows active phase
- shows next action
- shows Git status
- shows last commit
- shows tracker output
- shows open risks
- shows Kira, Phil, Claim Gauntlet, Promotion Gate, Provenance, Phase Map, Cockpit summaries when present

**What it does not do:**

- execute autonomous actions
- replace wiki_landing
- claim production monitoring
- claim truth resolution

### 2. Active Workplan Brain

**Capability:** Keep the terminal oriented to one current workplan, phase, tracker, next action, blockers, risk state, and closure rule.

**Command:**

```bash
cat memory_layer/wiki/operator_memory/active_workplan.json
```

**Primary artifacts:**

- `memory_layer/wiki/operator_memory/active_workplan.json` (FOUND)
- `tools/status/active_workplan_brain_check.py` (FOUND)

**What it does:**

- stores active workplan state
- stores active tracker path
- stores next action
- stores closure rule
- stores allowed/forbidden actions
- prevents stale phase guessing when helpers read it

**What it does not do:**

- decide work autonomously
- override human direction
- replace professional review

### 3. Canonical Landing

**Capability:** End repo/wiki work with canonical Git, tracker, Kira, and fireworks check.

**Command:**

```bash
wiki_landing
```

**Optional wrapper:** `wiki_landing`

**Primary artifacts:**

- `~/.specshift_landing.zsh` (FOUND)
- `memory_layer/wiki/operator_memory/active_workplan.json` (FOUND)

**What it does:**

- checks Git status
- shows recent commits
- runs active tracker from active_workplan.json
- prints Kira recommendation
- prints fireworks only when Git is happy

**What it does not do:**

- hand-code phase-specific fireworks
- replace actual commits
- prove substantive correctness

### 4. Kira Recommendation Engine

**Capability:** Produce rule-based local next-action guidance.

**Command:**

```bash
python3 tools/status/kira_recommendation_engine.py
```

**Optional wrapper:** `kira_recommend`

**Primary artifacts:**

- `tools/status/kira_recommendation_engine.py` (FOUND)
- `memory_layer/wiki/operator_memory/workstation_command_center/kira_recommendation_state.json` (FOUND)

**What it does:**

- reads active_workplan.json
- checks active tracker progress
- checks Git dirty state
- checks blockers
- checks claim/boundary risk
- recommends close/park/continue/claim scan

**What it does not do:**

- execute commands
- route externally
- replace human judgment

### 5. Phil Morale Layer

**Capability:** Give safe comic pacing feedback only after serious checks pass.

**Command:**

```bash
python3 tools/status/phil_morale_layer.py
```

**Optional wrapper:** `phil_summary`

**Primary artifacts:**

- `tools/status/phil_morale_layer.py` (FOUND)
- `memory_layer/wiki/operator_memory/workstation_command_center/phil_morale_state.json` (FOUND)

**What it does:**

- holds if Git is dirty
- holds if Kira severity is high
- gives human-friendly pacing feedback
- writes state for pass/held outcomes

**What it does not do:**

- override Kira
- execute workflow
- replace wiki_landing

### 6. Claim Gauntlet

**Capability:** Scan local text for risky overstatement language and suggest safer wording.

**Command:**

```bash
python3 tools/status/claim_gauntlet.py
```

**Optional wrapper:** `claim_gauntlet`

**Primary artifacts:**

- `tools/status/claim_gauntlet.py` (FOUND)
- `memory_layer/wiki/operator_memory/workstation_command_center/claim_gauntlet_report.json` (FOUND)
- `memory_layer/wiki/operator_memory/workstation_command_center/claim_gauntlet_hits.jsonl` (FOUND)

**What it does:**

- flags terms like proves, validates, predicts, autonomous, truth, production-ready
- distinguishes some boundary/allowlisted contexts
- suggests safer bounded wording
- updates claim-risk state

**What it does not do:**

- certify legal/compliance/scientific correctness
- guarantee buyer-safe language
- replace human or lawyer review

### 7. Artifact Promotion Gate

**Capability:** Gate artifacts before promotion to public/client-facing use.

**Command:**

```bash
python3 tools/status/promote_artifact.py <artifact> --target public --dry-run
```

**Optional wrapper:** `promote_artifact`

**Primary artifacts:**

- `tools/status/promote_artifact.py` (FOUND)
- `memory_layer/wiki/operator_memory/workstation_command_center/artifact_promotion_gate_report.json` (FOUND)
- `memory_layer/wiki/operator_memory/workstation_command_center/artifact_promotion_history.jsonl` (FOUND)

**What it does:**

- checks Git cleanliness
- references Claim Gauntlet status
- records SHA-256 provenance
- checks public/private/protected boundary
- checks buyer-safe wording
- writes gate report/history

**What it does not do:**

- publish automatically
- certify legal/compliance readiness
- allow protected artifacts to public by default

### 8. Provenance Vault

**Capability:** Record artifact hashes, timestamps, status, path, wiki link, commit, and promotion history.

**Command:**

```bash
python3 tools/status/provenance_vault.py --default-set
```

**Optional wrapper:** `provenance_vault`

**Primary artifacts:**

- `tools/status/provenance_vault.py` (FOUND)
- `memory_layer/wiki/operator_memory/workstation_command_center/provenance_vault.jsonl` (FOUND)
- `memory_layer/wiki/operator_memory/workstation_command_center/provenance_vault_report.json` (FOUND)

**What it does:**

- records SHA-256
- records timestamp
- records artifact status
- records linked wiki page
- records commit reference
- references promotion history

**What it does not do:**

- publish
- certify
- replace CPA/lawyer audit

### 9. Visual Phase Map

**Capability:** Render a terminal map of registered phases and statuses.

**Command:**

```bash
python3 tools/status/phase_map.py
```

**Optional wrapper:** `phase_map`

**Primary artifacts:**

- `tools/status/phase_map.py` (FOUND)
- `memory_layer/wiki/operator_memory/workstation_command_center/phase_map_state.json` (FOUND)

**What it does:**

- shows complete/active/parked/protected/caution statuses
- reads registered workplan state
- writes phase map state

**What it does not do:**

- execute phase work
- alter source of truth beyond state output
- replace tracker

### 10. Cockpit Modes

**Capability:** Load local mission context for specific work modes.

**Command:**

```bash
python3 tools/status/cockpit.py specshift
```

**Optional wrapper:** `cockpit specshift`

**Primary artifacts:**

- `tools/status/cockpit.py` (FOUND)
- `memory_layer/wiki/operator_memory/workstation_command_center/cockpit_state.json` (FOUND)

**What it does:**

- loads specshift/orchestra/ddf/outreach/shutdown context
- lists relevant commands
- lists relevant paths
- lists relevant wiki/docs
- is read-only by default
- writes state only with --write-state

**What it does not do:**

- execute autonomous work
- route externally
- dirty Git by default

### 11. Close Universe

**Capability:** Summarize shutdown state, landed work, parked work, and tomorrow's first task.

**Command:**

```bash
python3 tools/status/close_universe.py
```

**Optional wrapper:** `close_universe`

**Primary artifacts:**

- `tools/status/close_universe.py` (FOUND)
- `memory_layer/wiki/operator_memory/workstation_command_center/close_universe_state.json` (FOUND)
- `memory_layer/wiki/operator_memory/workstation_command_center/close_universe_log.jsonl` (FOUND)

**What it does:**

- shows active workplan
- shows active phase
- shows latest commit
- shows Git dirty state
- shows completed phases
- shows parked phases
- shows tomorrow's first task

**What it does not do:**

- lock the OS
- replace wiki_landing
- execute autonomous shutdown

### 12. Worldwide Intake + Analytical Core

**Capability:** Track the completed chain from intake through analysis, scenario suggestions, implementation scaffolds, and audit.

**Command:**

```bash
python3 tools/status/worldwide_phase16_progress.py
```

**Primary artifacts:**

- `memory_layer/wiki/operator_memory/worldwide_phase16/phase16_analytical_audit_report.json` (FOUND)
- `memory_layer/wiki/operator_memory/worldwide_phase15/phase15_implementation_suggestion_report.json` (FOUND)
- `memory_layer/wiki/operator_memory/worldwide_phase14/phase14_bounded_scenario_suggestion_report.json` (FOUND)

**What it does:**

- confirms analytical chain closeout
- preserves claim boundaries
- audits continuity/counts/runner presence
- documents pattern, negative-space, math, secondary-condition, scenario, and implementation scaffold layers

**What it does not do:**

- claim live production value
- claim prediction
- claim alerting
- claim truth validation

### 13. Forecast + Negative-Space Engine

**Capability:** Create bounded forecast candidates, negative-space watchlists, and human-review queues.

**Command:**

```bash
python3 tools/status/workstation_forecast_negative_space_progress.py
```

**Primary artifacts:**

- `memory_layer/wiki/operator_memory/workstation_forecast_negative_space/forecast_phase6_audit_closeout_report.json` (FOUND)
- `memory_layer/wiki/operator_memory/workstation_forecast_negative_space/forecast_phase5_scenario_review_queue_report.json` (FOUND)
- `memory_layer/wiki/operator_memory/workstation_forecast_negative_space/forecast_phase4_descriptive_forecast_candidate_report.json` (FOUND)

**What it does:**

- inventories usable signals
- creates negative-space watchlists
- creates descriptive forecast candidates
- creates human-review queue items
- audits output and boundaries

**What it does not do:**

- predict
- alert
- monitor production
- infer causality
- resolve truth

### 14. SpecShift Client Intake + Delivery System

**Capability:** Run a client-safe intake, data-room, provenance gate, review packet, delivery scaffold, and closeout audit workflow.

**Command:**

```bash
python3 tools/status/specshift_client_intake_delivery_progress.py
```

**Primary artifacts:**

- `memory_layer/wiki/operator_memory/specshift_client_intake_delivery/client_phase6_closeout_audit_report.json` (FOUND)
- `memory_layer/wiki/operator_memory/specshift_client_intake_delivery/client_phase5_delivery_package_scaffold.json` (FOUND)
- `memory_layer/wiki/operator_memory/specshift_client_intake_delivery/client_data_room_index.json` (FOUND)

**What it does:**

- defines client scope boundaries
- creates intake checklist
- creates data-room index
- routes artifacts through provenance and claim gates
- creates review packet scaffolds
- creates candidate-discrepancy memo scaffolds
- creates delivery package scaffold
- audits human review, language, retention, classification

**What it does not do:**

- provide legal advice
- provide financial advice
- create binding contract terms
- certify compliance
- validate truth
- authorize autonomous client action

### 15. Professional Readiness / Lawyer + CPA Package

**Capability:** Prepare forensic accounting and conservative viability documentation for lawyer/CPA review.

**Command:**

```bash
python3 tools/status/professional_readiness_progress.py
```

**Primary artifacts:**

- `memory_layer/wiki/operator_memory/professional_readiness/professional_phase5_audit_closeout_report.json` (FOUND)
- `memory_layer/wiki/operator_memory/professional_readiness/professional_forensic_artifact_index.json` (FOUND)
- `memory_layer/wiki/operator_memory/professional_readiness/professional_viability_claim_matrix.json` (FOUND)
- `memory_layer/wiki/operator_memory/professional_readiness/professional_financial_contract_thresholds.json` (FOUND)
- `memory_layer/wiki/operator_memory/professional_readiness/professional_exportable_review_packet_index.json` (FOUND)

**What it does:**

- indexes artifacts with hashes
- separates viable/scaffolded/unvalidated/professional-review-required claims
- records financial/contract trigger thresholds
- records no-free-pilot posture
- prepares lawyer/CPA questions
- builds exportable professional-review packet index

**What it does not do:**

- provide legal advice
- provide tax advice
- provide financial advice
- provide valuation
- certify compliance
- guarantee commercial viability

### 16. Regulatory, Certification, and Procurement Readiness

**Capability:** Prepare internal documentation scaffolds for future regulator/certification/procurement diligence.

**Command:**

```bash
python3 tools/status/regulatory_certification_readiness_progress.py
```

**Primary artifacts:**

- `memory_layer/wiki/operator_memory/regulatory_certification_readiness/regulatory_phase6_audit_closeout_report.json` (FOUND)
- `memory_layer/wiki/operator_memory/regulatory_certification_readiness/regulatory_phase5_certification_gap_analysis_report.json` (FOUND)
- `memory_layer/wiki/operator_memory/regulatory_certification_readiness/regulatory_phase4_procurement_due_diligence_packet.json` (FOUND)
- `memory_layer/wiki/operator_memory/regulatory_certification_readiness/regulatory_phase3_governance_policy_scaffold.json` (FOUND)

**What it does:**

- maps scope and likely standards/reference categories
- inventories controls/evidence
- creates governance-policy scaffolds
- creates procurement diligence packet index
- creates certification/procurement gap analysis
- audits readiness boundaries

**What it does not do:**

- claim certification
- claim compliance
- claim government approval
- claim procurement approval
- claim legal sufficiency
- claim financial/tax approval
- claim production monitoring
- claim truth validation

## Boundary

This capability map documents local workstation capabilities only. It does not claim certification, compliance, government approval, procurement approval, legal sufficiency, financial/tax approval, professional audit, production monitoring, prediction, autonomous action, or truth validation.
