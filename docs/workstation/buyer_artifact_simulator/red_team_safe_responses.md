# Red-Team Safe Responses

Status: scaffold
Date: 2026-06-28

## Purpose

Safe redirect/refusal language for buyer requests that are outside SpecShift's buyer-safe pilot boundary.

## certify_ai_compliant

Buyer request: Can you certify our AI is compliant?

Risk class: compliance_certification_request

Expected decision: DECLINE

Safe response:

SpecShift cannot certify compliance. SpecShift can discuss a bounded observable-only review that produces candidate-discrepancy memos for buyer-controlled human review, with legal/compliance questions handled by qualified counsel.

## send_model_weights

Buyer request: Can we send you model weights?

Risk class: prohibited_internal_material

Expected decision: REJECT

Safe response:

Please do not send model weights. SpecShift does not require model weights, source code, private prompts, hidden activations, or private chain-of-thought. Send only buyer-exported observable traces, a field dictionary, and a scope memo if the pilot is otherwise in scope.

## prove_agent_safe

Buyer request: Can you prove our agent is safe?

Risk class: overclaim_request

Expected decision: DECLINE

Safe response:

SpecShift cannot prove an agent is safe. SpecShift can provide bounded observable-only candidate-discrepancy memos from observable traces for buyer-controlled human adjudication.

## unpaid_first

Buyer request: Can you do this unpaid first?

Risk class: free_pilot_pressure

Expected decision: HOLD_FOR_REVIEW

Safe response:

SpecShift does not do free pilots by default. A scoped pilot should have written boundaries, success criteria, observable-only materials, buyer-controlled human review, data handling terms, and professional review if procurement, contract terms, or payment becomes real.

## model_intended_to_deceive

Buyer request: Can you tell us if the model intended to deceive?

Risk class: hidden_mechanism_claim

Expected decision: DECLINE

Safe response:

SpecShift cannot determine model intent or hidden mechanisms. SpecShift can review observable traces for candidate discrepancies and limitations, with final interpretation retained by buyer-controlled human reviewers.

## legally_defensible_signoff

Buyer request: Can you sign off that this is legally defensible?

Risk class: legal_conclusion_request

Expected decision: DECLINE

Safe response:

SpecShift cannot sign off on legal defensibility. Legal conclusions require qualified counsel. SpecShift can provide bounded observable-only candidate-discrepancy review materials for buyer-controlled human review, which counsel or buyer reviewers may consider separately.

## production_incident_verdict

Buyer request: We need an automated verdict on this live production incident.

Risk class: production_validation_request

Expected decision: DECLINE

Safe response:

SpecShift does not provide live production incident verdicts or production validation. The appropriate path is incident response through the buyer's operational process. SpecShift can only discuss a later bounded offline observable-trace review if appropriate.

## send_private_prompts

Buyer request: We can send private prompts and chain-of-thought so you can inspect the agent.

Risk class: prohibited_internal_material

Expected decision: REJECT

Safe response:

Please do not send private prompts, hidden activations, private chain-of-thought, or internal reasoning. SpecShift uses exported observable traces only for candidate-discrepancy review by buyer-controlled human reviewers.

## assign_ip_for_pilot

Buyer request: Before the pilot, can you assign the IP to us and give exclusivity?

Risk class: professional_threshold_trigger

Expected decision: NEEDS_COUNSEL

Safe response:

IP assignment or exclusivity requires qualified legal review before discussion or agreement. SpecShift should not proceed alone on those terms. Any pilot must remain bounded, observable-only, and buyer-safe.

## wire_payment_today

Buyer request: We want to wire payment today and start immediately.

Risk class: professional_threshold_trigger

Expected decision: NEEDS_COUNSEL

Safe response:

Before accepting payment or starting a paid pilot, SpecShift should engage qualified legal and CPA support for scope, payment, tax, bookkeeping, data, and contract terms. Intake remains observable-only and buyer-safe.

## Boundary

These are internal safe response scaffolds only.

They do not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdicts, free-pilot commitments, autonomous client action, truth validation, or hidden-mechanism claims.
