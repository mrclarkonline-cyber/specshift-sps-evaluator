# SpecShift Operator Quickstart

Status: Outreach-ready v0.1

Stable tag: outreach-ready-v0.1

Core product: SpecShift Architectural Logic Diagnostics

First offer: Focused Diagnostic Pilot

Standing boundary:
SpecShift is a pre-deployment diagnostic and architecture-stage review process. It is not a benchmark, certification, compliance audit, runtime monitor, security tool, deployment approval, or guarantee of AI safety.

What to do now:
Stop building products. Begin focused outreach. When someone responds, use the buyer-call workflow.

Before outreach, run:
cd ~/specshift_terminal_intelligence
python3 v0_5/ops/specshift_ops_dashboard.py
python3 v0_5/claim_scan_git_log.py
git status --short

During a buyer call, run:
cd ~/specshift_terminal_intelligence
python3 v0_5/call_companion/specshift_call_companion.py

Mode guide:
1. Show scoping script only
2. Call mode: notes + Proton-ready follow-up + scope outline + selected v0.5 cases
3. Email mode: follow-up draft + scope outline

Email:
Default path is Proton-ready draft, review, then manual send.
Guarded SMTP sender exists for one-email sending only. It previews first and requires exact typed confirmation.

Guarded sender:
cd ~/specshift_terminal_intelligence
python3 v0_5/email_bridge/proton_guarded_send.py --to recipient@example.com --subject "Subject" --body-file path/to/body.txt

Rules:
No bulk send.
No silent send.
No Apple Mail.
No secrets in repo.
No product sprawl.
No certification, benchmark, compliance, runtime, security, deployment approval, or safety guarantee claims.

Built vertical packs:
- Finance/Reconciliation Agent Diagnostic Pack v0.1
- Procurement Agent Diagnostic Pack v0.1
- Customer Support Escalation Agent Diagnostic Pack v0.1
- Healthcare Operations Agent Diagnostic Pack v0.1
- Education/IEP Workflow Diagnostic Pack v0.1

Failure column:
This quickstart fails if it encourages product sprawl, overclaiming, bulk email, hidden sending, secret leakage, or buyer-facing claims beyond the current outreach-ready internal status.
