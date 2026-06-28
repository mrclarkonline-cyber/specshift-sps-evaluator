# Pilot Success and Failure Criteria

Status: scaffold  
Date: 2026-06-28

## Purpose

These criteria measure whether a buyer-safe observable-only pilot is useful and in scope.

They do not validate production performance, certify compliance, determine truth, create legal/financial conclusions, or authorize automated action.

## Success criteria

### 1. Scope fit

Buyer can provide observable exported traces without protected internals.

Measurement:

- trace export includes visible sequence
- event/state fields are present
- claimed final state is available if relevant
- field dictionary is provided
- scope memo is provided

### 2. Label or adjudication fit

Buyer retains labels or can perform human adjudication.

Measurement:

- buyer confirms label ownership
- buyer confirms final adjudication process
- ambiguous or insufficient-information category is allowed

### 3. Memo usefulness

Candidate-discrepancy memos are useful to human reviewers.

Measurement:

Buyer reviewer can classify memo prompts as:

- useful
- ambiguous
- insufficient
- not useful

### 4. Boundary preservation

Pilot remains observable-only and avoids overclaiming.

Measurement:

No use of:

- model weights
- source code
- private prompts
- hidden activations
- private chain-of-thought
- automated verdicts
- production validation
- compliance claims

### 5. Repeatable delivery

SpecShift can produce a bounded delivery packet consistently.

Measurement:

- intake complete
- provenance complete
- memo complete
- limitations complete
- delivery checklist complete

## Failure or stop criteria

Stop, park, or rescope if:

- protected internals are required
- buyer cannot provide observable exported traces
- no buyer-controlled human adjudication path exists
- buyer asks for production validation
- buyer asks for automated verdicts
- buyer asks for compliance certification
- buyer asks for truth validation
- procurement, contract terms, paid pilot, licensing, exclusivity, acquisition, IP assignment, data transfer, or money movement becomes real without qualified legal/CPA support
- buyer expects a free pilot that transfers substantial value or protected method knowledge

## Allowed result categories

- useful_review_prompt
- ambiguous_review_prompt
- insufficient_information
- not_useful_for_this_workflow
- requires_more_observable_context
- pilot_not_in_scope

## Forbidden result categories

- validated_failure
- automated_verdict
- production_validated
- compliance_certified
- truth_validated
- legal_finding
- financial_finding

## Boundary

These criteria measure pilot usefulness and boundary fit only.

They do not validate production performance, certify compliance, determine truth, create legal/financial conclusions, or authorize automated action.
