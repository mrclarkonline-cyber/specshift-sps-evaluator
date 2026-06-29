# Systems Integration Survey Audit

Status: scaffold

## Purpose

Survey whether SpecShift workstation systems are present, connected, and runnable.

## Checks

- Required scripts and docs exist
- Active workplan state is coherent
- Completed workplans are closed or parked
- Dependency records exist
- QA command runs
- Security doctor runs
- Path watch runs
- Security scan runs
- QA tracker runs
- Git state is inspected

## Command

    python3 tools/status/specshift_systems_survey.py

## Interpretation

- `pass`: systems are present and connected
- `review`: systems work, but something deserves human review
- `fail`: a required system or command failed

## Boundary

This is an internal systems survey only.

It does not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdict, free pilot commitment, autonomous client action, surveillance authorization, truth validation, or hidden-mechanism claim.
