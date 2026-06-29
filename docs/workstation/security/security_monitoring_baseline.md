# Security Monitoring Baseline

Status: defensive scaffold

## Purpose

Add defensive monitoring and audit tools for command shadows, local posture, repo secrets, and system hardening.

## Installed tools

- fswatch: file/path change monitoring
- osquery: host inventory and process/launch-agent queries
- lynis: local system hardening audit
- gitleaks: repository secret scanning
- trufflehog: deeper filesystem secret scanning

## Commands

Run PATH shadow check:

    python3 tools/status/specshift_path_watch.py

Run broader defensive scan:

    python3 tools/status/specshift_security_scan.py

Run existing doctor:

    python3 tools/status/specshift_security_doctor.py

## Boundary

This is defensive local workstation monitoring only.

It does not create offensive tooling, surveillance authorization, credential collection, legal advice, compliance certification, production validation, automated verdict, free pilot commitment, autonomous client action, truth validation, or hidden-mechanism claim.
