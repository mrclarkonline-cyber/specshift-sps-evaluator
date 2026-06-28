# Intake Risk Policy

Status: scaffold  
Date: 2026-06-28

## Purpose

Risk-gate buyer artifacts before accepting or routing them.

## Decisions

### ACCEPT

Allowed observable-only material may enter the correct buyer-safe folder.

### HOLD_FOR_REVIEW

Do not route into working review until human/professional review resolves the issue.

### REJECT

Do not accept the material. Ask buyer to remove prohibited/internal material and resend only appropriate observable exports if applicable.

### NEEDS_REDACTION

Do not accept until redaction, pseudonymization, written terms, or professional review is complete.

## Reject by default

- source code
- model weights
- private prompts
- private chain-of-thought
- hidden activations
- secrets, credentials, keys, tokens, or passwords

## Hold or redact by default

- customer PII
- regulated data
- legal/compliance requests
- production incident demands
- requests for production validation
- requests for automated verdicts
- requests for truth validation
- anything outside pilot scope

## Boundary

This is an intake risk policy scaffold only.

It does not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdicts, free-pilot commitments, autonomous client action, or hidden-mechanism claims.
