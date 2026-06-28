# Buyer Data Request Template

Status: scaffold  
Date: 2026-06-28

## Purpose

This template defines what a buyer may send for a buyer-controlled observable-only pilot.

## Request only

### 1. Observable workflow trace export

Visible time-ordered events, states, actions, outputs, claimed final states, or workflow milestones.

### 2. Claimed final state export

Visible final status, ledger/payment state, task completion state, or other claimed endpoint.

### 3. Buyer-retained labels or adjudication sheet, optional

Buyer-controlled labels or human adjudication outcomes.

### 4. Scope memo

Plain-language scope memo identifying:

- workflow
- sample window
- systems in scope
- systems out of scope
- known limitations

### 5. Field dictionary

Data dictionary for exported observable fields.

### 6. Redaction or pseudonymization note

Explanation of redactions, pseudonymization, or removed sensitive fields.

## Do not send

- model weights
- source code
- private prompts
- hidden activations
- private chain-of-thought
- internal architecture diagrams unless lawyer/security approved
- training data
- raw secrets, credentials, keys, tokens, or passwords
- unredacted personal data unless written terms authorize it
- regulated sensitive data unless written terms and professional review authorize it

## Preferred formats

- CSV
- JSONL
- JSON
- Parquet only if agreed
- PDF scope memo
- Markdown or text field dictionary

## Minimum suggested fields

- `record_id`
- `event_time_or_sequence`
- `visible_event_type`
- `visible_actor_or_system_id_pseudonymized`
- `visible_input_or_trigger_summary_if_available`
- `visible_output_or_state_summary`
- `claimed_final_state_if_available`
- `buyer_label_if_available`
- `notes_if_available`

## Retention default

Do not retain raw client artifacts beyond the scoped review unless written terms say otherwise.

## Boundary

This is a buyer data request scaffold only.

It requests observable exported traces and scope materials only.

It does not request protected internals and does not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdicts, or autonomous client action.
