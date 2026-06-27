# Outreach Lessons — Current Conversation Scrape

Source(s): Current ChatGPT conversation, SpecShift outreach workflow, local Terminal logs
Last updated: 2026-06-26
Public-safe: No
Private-safe: Yes
Counsel-only: No
Core-protected: Yes
Confidence: High for operational lessons; medium for exact delivery/landing interpretation
Contradictions: None known; delivery status depends on user-reported bounces/landing
Promotion status: Operator memory / working wiki

Status: Durable operator memory  
Scope: Important lessons from the current SpecShift outreach/send workflow  
Protected core: No protected scoring, ordering, or implementation mechanics included

## Core Lesson

The contact problem was not primarily the email body. The first major failure mode was the contact layer.

Person-name/title/email rows generated from AI or pattern guesses are unsafe. They can look plausible while being fabricated, stale, role-inaccurate, or routed to nonexistent addresses.

Going forward, company targeting may be generated or assisted by AI, but recipient routing must be treated as a separate verification layer.

## Contact Source Rule

Use company names and target functions as planning inputs.

Do not trust:
- AI-generated individual names
- AI-generated titles
- guessed executive emails
- first-name CEO/founder emails
- guessed firstname.lastname patterns
- impressive-sounding AI-risk titles with no public evidence

Acceptable route hierarchy:

1. Published official contact form
2. Published sales, partnerships, enterprise, vendor, or business inquiry route
3. Published business email alias
4. Role inbox candidate on a verified domain, only as a test
5. Manual route research
6. Hold

## Alias Experiment Results

The `sales@domain` experiment was cleaner than guessed person emails, but not reliable enough to be treated as a complete outreach strategy.

Working interpretation:

- `sales@domain` is a useful first alias test.
- It works often enough to surface real routes.
- It fails often enough that non-landing aliases must be quarantined.
- Domain verification does not prove mailbox existence.

Important boundary:

`domain verified != mailbox verified`

MX records, SPF, DMARC, A/AAAA, and web presence prove a domain is real and mail-capable. They do not prove `sales@`, `contact@`, `support@`, or any other alias exists.

## Wave 7 Repair Rule

Wave 7 is the repair queue, not trash.

Move to Wave 7 when:
- alias bounced
- alias did not land
- domain exists but mailbox route failed
- route is legal/privacy/support when sales/vendor route is needed
- route requires manual research
- alias is typo-contaminated or otherwise uncertain

Keep in the original wave when:
- message appears to land
- no bounce is reported
- route is pending but not confirmed failed

## Support@ Experiment

`support@domain` is a reasonable Wave 7 repair experiment only if the email is framed as a routing request, not a sales pitch.

Support teams should receive a first-sentence reroute ask.

Approved Wave 7B subject:

routing question: agentic workflow reliability

Approved Wave 7B first sentence:

I’m writing to ask whether you can route this to the team that owns AI workflow reliability, automation integrity, product risk, or enterprise evaluation.

Reason:

Support inboxes often exist and are trained for triage, but they should not receive the normal sales/pilot email. The support version should be lower-pressure and explicitly ask for routing.

## First-Contact Email Rules

No attachments on first contact.

First contact should be:
- text-only
- short
- low-friction
- bounded
- not overclaiming
- asking for routing or permission to send a one-pager

Attachment rule:

Send a one-pager only after a positive reply or when specifically requested. Unsolicited attachments increase spam/security friction and contradict the trust posture.

## Current Safe Subject Lines

For direct sales/vendor route:

agent handoffs vs. operational evidence

For support/reroute route:

routing question: agentic workflow reliability

## Message Posture

SpecShift should be framed as:

- bounded diagnostic review
- observable workflow trace review
- claimed completion versus operational evidence
- false completion
- missed handoffs
- stale state
- weak recovery paths
- authority creep / permission drift
- no model weights
- no code transfer
- no training rights
- no access to proprietary core systems beyond agreed review packet

Avoid:
- claims of live buyer validation
- claims that companies already need or use equivalent systems
- implying insider knowledge
- implying accusation
- overclaiming production proof
- proprietary method details

## SMTP / Sending Rules

Use Proton SMTP directly:

- host: smtp.protonmail.ch
- port: 587
- user: ben@specshiftlabs.com

Do not store or print SMTP token.

All sends must be:
- guarded by exact typed confirmation
- logged
- paced
- text-only attachment-checked
- reversible at the queue level before sending

## Confirmation Phrase Pattern

Use wave-specific exact confirmations:

- SEND SALES WAVE1
- SEND SALES WAVE2
- SEND SALES WAVE3
- SEND SALES WAVE4
- SEND SALES WAVE5
- SEND SALES WAVE6
- SEND SUPPORT WAVE7B

If the confirmation phrase is wrong, the sender must stop without sending.

## Operational Learning

The outreach system has become a routing experiment.

The goal is no longer “send to 1,000 companies.”

The goal is:

1. Identify which routing patterns actually land.
2. Quarantine failures.
3. Preserve working routes.
4. Repair the rest.
5. Avoid fake-person data permanently.

## Business Lesson

Even a low landing rate was useful because it converted an unsafe 1,000-company target list into structured categories:

- landed or likely landed
- failed alias
- domain repair hold
- official route needed
- support reroute experiment
- manual research needed

This is now an evidence-producing outreach workflow, not a blind blast.

## Protected Core Reminder

Do not expose:
- proprietary scoring
- internal diagnostic ordering
- implementation mechanics
- protected method internals

Outreach language should describe the review layer, not how the protected diagnostic process works.