# SpecShift Local Asset Map v0.1

Status: internal local organization map, no secrets included.

Purpose: document where known SpecShift assets live without crawling the whole Mac.

Root repo: ~/specshift_terminal_intelligence

Start here:
- OPERATOR_QUICKSTART.md
- SPECSHIFT_COMMANDS.md
- terminal_intelligence_index.json
- LOCAL_ASSET_MAP.json
- LOCAL_ASSET_MAP.md

Core engine:
- v0_5/unknown_domain_adversarial_suite_v0_5.json
- v0_5/validate_v0_5_suite.py
- v0_5/claim_scan_git_log.py
- v0_5/git_log_claim_language_register_v0_1.json

Commercial and outreach assets:
- v0_5/focused_paid_pilot_posture_v0_1.json
- v0_5/bounded_paid_pilot_outreach_email_v0_2.json
- v0_5/role_specific_outreach_variants_v0_2.json
- v0_5/focused_diagnostic_pilot_scoping_call_script_v0_1.json
- v0_5/specshift_focused_diagnostic_pilot_one_pager_v0_1.pdf
- v0_5/specshift_focused_diagnostic_pilot_one_pager_v0_1.txt
- v0_5/outreach_readiness/

Buyer call companion:
Run: cd ~/specshift_terminal_intelligence && python3 v0_5/call_companion/specshift_call_companion.py
Main file: v0_5/call_companion/specshift_call_companion.py

Email bridge:
- readiness check: v0_5/email_bridge/proton_bridge_readiness_check.py
- guarded sender: v0_5/email_bridge/proton_guarded_send.py
- local config: ~/.specshift/proton_bridge_config.json
- SMTP: smtp.protonmail.ch:587
- from: ben@specshiftlabs.com
- Keychain service: specshift_proton_smtp_token
- Keychain account: ben@specshiftlabs.com

Email safety:
- preview first
- exact typed confirmation per email
- no bulk send
- no silent send
- no Apple Mail
- no secrets in repo

Vertical packs folder: v0_5/vertical_packs/
Built v0.1 packs:
- Finance/Reconciliation Agent Diagnostic Pack
- Procurement Agent Diagnostic Pack
- Customer Support Escalation Agent Diagnostic Pack
- Healthcare Operations Agent Diagnostic Pack
- Education/IEP Workflow Diagnostic Pack

Ops dashboard:
Run: cd ~/specshift_terminal_intelligence && python3 v0_5/ops/specshift_ops_dashboard.py

Exports:
- ~/specshift_terminal_intelligence/exports/
- ignored by git

Stable points:
- tag: outreach-ready-v0.1
- commit: 5bcfcd1 Add operator quickstart

Do not commit or expose:
- SMTP passwords or tokens
- macOS Keychain token value
- private keys
- buyer confidential materials
- unrelated personal files
- future live buyer data without explicit review

Standard health check:
cd ~/specshift_terminal_intelligence && python3 v0_5/ops/specshift_ops_dashboard.py && python3 v0_5/claim_scan_git_log.py && git status --short

Failure column:
This map fails if it becomes a secret store, claims total knowledge of the Mac, indexes unrelated personal files, or replaces actual health checks.
