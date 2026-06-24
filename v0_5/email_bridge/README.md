# SpecShift Email Bridge

SpecShift email is handled through `ben@specshiftlabs.com`.

## Current capabilities

1. Proton SMTP readiness check
2. Guarded one-email SMTP sender

## Safety rules

- No bulk sending.
- No silent sending.
- No Apple Mail.
- No osascript.
- No SMTP token stored in repo.
- Token is retrieved from macOS Keychain service: `specshift_proton_smtp_token`.
- Every send previews the message first.
- Every send requires exact typed confirmation: `SEND recipient@example.com`.

## Readiness check

```bash
cd ~/specshift_terminal_intelligence
python3 v0_5/email_bridge/proton_bridge_readiness_check.py
Dry run:

cd ~/specshift_terminal_intelligence
python3 v0_5/email_bridge/proton_guarded_send.py --to mrclarkonline@protonmail.com --subject "test" --body "test" --dry-run

Real send:

cd ~/specshift_terminal_intelligence
python3 v0_5/email_bridge/proton_guarded_send.py --to mrclarkonline@protonmail.com --subject "test" --body "test"

The script will require exact typed confirmation before sending.

Failure column:
This bridge fails if it sends without preview, sends without typed confirmation, sends in bulk, stores secrets in the repo, logs full email bodies unnecessarily, uses Apple Mail automation, or bypasses Ben's review.
