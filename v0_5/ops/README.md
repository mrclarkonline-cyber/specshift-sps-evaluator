# SpecShift Ops Dashboard v0.1

Purpose:
One command to check the current SpecShift stack.

Run:

cd ~/specshift_terminal_intelligence
python3 v0_5/ops/specshift_ops_dashboard.py

Checks:
- repo cleanliness
- core JSON artifacts
- v0.5 suite case/category count
- Python compile status
- call companion features
- Proton email bridge/sender features
- vertical diagnostic pack registry
- claim-language scan
- current next action

Safety:
- Does not send email.
- Does not print SMTP token.
- Does not use Apple Mail.
- Does not modify repo state.

Failure column:
This dashboard fails if it becomes a replacement for actual validation, sends email, stores secrets, hides claim risks, or implies buyer readiness beyond the current outreach-ready internal status.

## Asset audit

Run:

cd ~/specshift_terminal_intelligence
python3 v0_5/ops/specshift_asset_audit.py

Purpose:
Checks that known SpecShift company assets are present and findable without crawling unrelated local/personal Ben files.

Safety:
- Does not send email.
- Does not print secrets.
- Does not crawl the whole Mac.
- Checks only the mapped SpecShift operating stack.
