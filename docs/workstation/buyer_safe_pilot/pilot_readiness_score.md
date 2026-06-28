# Pilot Readiness Score

Status: scaffold  
Date: 2026-06-28

## Purpose

`pilot_readiness_score.py` scores whether a buyer-safe pilot is ready to accept.

## Command

    python3 tools/pilot_intake/pilot_readiness_score.py --status-json tests/fixtures/buyer_artifact_simulator/pilot_readiness_cases.json --json

For a single status file:

    python3 tools/pilot_intake/pilot_readiness_score.py --status-json /path/to/status.json --output /tmp/readiness_score.json

## Decisions

- READY
- NOT_READY
- NEEDS_SCOPING
- NEEDS_REDACTION
- NEEDS_COUNSEL
- DECLINE

## Important meaning of READY

READY means internally intake-ready only.

It does not mean:

- legally approved
- compliance certified
- production validated
- automatically accepted
- commercially proven
- safe without human review

## Boundary

This scoring tool is an internal buyer-safe intake scaffold only.

It does not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdicts, free-pilot commitments, autonomous client action, truth validation, or hidden-mechanism claims.
