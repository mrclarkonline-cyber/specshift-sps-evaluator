# SpecShift Security Doctor

Status: defensive scaffold

## Purpose

Run local workstation security posture checks for SpecShift.

## Command

    python3 tools/status/specshift_security_doctor.py

## Checks

- FileVault status
- Firewall status
- Gatekeeper status
- System Integrity Protection status
- Homebrew taps and Microsoft tap detection
- Core command path shadows
- Git remotes and clean status
- SSH private-key permissions
- SpecShift QA pass/fail

## Interpretation

- `pass`: no immediate issue detected
- `review`: something deserves human review
- `fail`: a hard check failed

## Boundary

This is defensive local workstation hygiene only.

It does not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdict, free pilot commitment, autonomous client action, surveillance authorization, truth validation, or hidden-mechanism claim.
