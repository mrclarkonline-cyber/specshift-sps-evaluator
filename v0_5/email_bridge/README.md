# SpecShift Proton Bridge Readiness Checker v0.1

Purpose:
Prepare for a future guarded Terminal-authorized send mode through Proton Mail Bridge.

Current status:
Readiness check only. This does not send email.

Current SpecShift email:
ben@specshiftlabs.com

Safety rules:
- No auto-send.
- No bulk send.
- No silent send.
- No Apple Mail.
- No osascript.
- No SMTP password committed to git.
- Any future send mode must preview the email and require typed confirmation per email.

Local config:
~/.specshift/proton_bridge_config.json

The repo includes only:
v0_5/email_bridge/proton_bridge_config.example.json

Edit the local config with the SMTP host, port, and username shown by Proton Mail Bridge.
Do not commit secrets.

Run:
cd ~/specshift_terminal_intelligence
python3 v0_5/email_bridge/proton_bridge_readiness_check.py

Failure column:
This bridge plan fails if it stores secrets in the repo, sends without typed confirmation, sends in bulk, bypasses manual review, uses Apple Mail automation, or changes claim-bounded outreach language without review.
