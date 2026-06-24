# SpecShift Commands

Health check:
cd ~/specshift_terminal_intelligence
python3 v0_5/ops/specshift_ops_dashboard.py
python3 v0_5/claim_scan_git_log.py
git status --short

Buyer call companion:
cd ~/specshift_terminal_intelligence
python3 v0_5/call_companion/specshift_call_companion.py

Proton SMTP readiness:
cd ~/specshift_terminal_intelligence
python3 v0_5/email_bridge/proton_bridge_readiness_check.py

Guarded Proton SMTP dry run:
cd ~/specshift_terminal_intelligence
python3 v0_5/email_bridge/proton_guarded_send.py --to mrclarkonline@protonmail.com --subject "test" --body "test" --dry-run

Guarded Proton SMTP send:
cd ~/specshift_terminal_intelligence
python3 v0_5/email_bridge/proton_guarded_send.py --to recipient@example.com --subject "Subject" --body-file path/to/body.txt

Required confirmation format:
SEND recipient@example.com

Show stable tag:
cd ~/specshift_terminal_intelligence
git show --stat outreach-ready-v0.1 --oneline --decorate --no-renames | head -n 40

Rule:
If the dashboard passes and the repo is clean, stop maintaining and start outreach.
