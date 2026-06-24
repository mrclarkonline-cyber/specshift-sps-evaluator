# SpecShift Outreach Pipeline v0.1

Purpose:
Track focused outreach without turning the repo into a CRM or storing unnecessary personal data.

Files:
- outreach_targets_v0_1.csv
- outreach_touch_log_v0_1.csv

Use:
1. Add one row per target company/contact.
2. Match the target to one likely workflow.
3. Match the workflow to one built vertical pack or candidate skin.
4. Send only bounded focused-diagnostic outreach.
5. Log each touch.
6. If a person responds or calls, use the buyer-call companion.

Buyer-call companion:
cd ~/specshift_terminal_intelligence
python3 v0_5/call_companion/specshift_call_companion.py

Email bridge:
Use Proton-ready drafts by default.
Use guarded SMTP sender only after preview and exact typed confirmation.

Rules:
- No bulk send.
- No silent send.
- No scraped personal-data dump.
- No certification, benchmark, compliance, runtime, security, deployment approval, or safety guarantee language.
- Track one concrete workflow per serious conversation.

Status values:
- not_contacted
- contacted
- replied
- call_scheduled
- call_done
- qualified
- no_fit
- paused
- closed

Failure column:
This tracker fails if it becomes bulk-spam tooling, stores unnecessary personal data, weakens claim boundaries, or replaces actual buyer discovery.

## Outreach Pipeline Manager

Run:

cd ~/specshift_terminal_intelligence
python3 v0_5/outreach_pipeline/outreach_pipeline_manager.py dashboard

Add a target:

python3 v0_5/outreach_pipeline/outreach_pipeline_manager.py add-target --company "Company Name" --person "Name" --role "Role" --email "name@example.com" --workflow "one concrete workflow" --pack "Finance/Reconciliation Agent Diagnostic Pack" --priority high

Log a touch:

python3 v0_5/outreach_pipeline/outreach_pipeline_manager.py log-touch --target-id T001 --touch-type initial_email --subject "SpecShift focused diagnostic pilot" --response-status contacted --next-action "wait for reply"

List targets:

python3 v0_5/outreach_pipeline/outreach_pipeline_manager.py list-targets

List touches:

python3 v0_5/outreach_pipeline/outreach_pipeline_manager.py list-touches

Rules:
- Focused outreach only.
- No bulk send.
- No silent send.
- One buyer/workflow at a time.
