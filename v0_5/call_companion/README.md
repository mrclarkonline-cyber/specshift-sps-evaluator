# SpecShift Call Companion v0.1

Terminal helper for focused diagnostic pilot conversations and Proton Mail follow-up drafts.

Run:

cd ~/specshift_terminal_intelligence
python3 v0_5/call_companion/specshift_call_companion.py

Modes:

1. Show scoping script only
2. Run call mode: script + notes + Proton-ready follow-up draft
3. Email mode: type contact/workflow and generate Proton-ready follow-up draft

Email safety:

SpecShift email is handled through ben@specshiftlabs.com on Proton Mail.

The tool does not auto-send email and does not use Apple Mail.

It creates:
- copy/paste Proton Mail draft .txt
- reference .eml
- call notes .json
- attachment path list .txt

Send manually through Proton Mail after review.

Signature used:

Benjamin J. Clark
Founder, SpecShift Labs LLC
Interpretation Review Layer
ben@specshiftlabs.com
https://www.specshiftlabs.com/
ORCID: 0009-0005-8622-0251

Default attachments:

Initial:
- Focused Diagnostic Pilot One-Pager PDF

Qualified:
- One-Pager PDF
- Pilot Scoping Brief text

Deep interest:
- One-Pager PDF
- Pilot Scoping Brief text
- Guardrail Checklist appendix text


## Pilot scope outline generator

The tool now creates a pilot scope outline alongside the Proton-ready email draft.

Generated outputs may include:
- Proton-ready follow-up email text
- reference `.eml`
- call notes JSON
- attachment path list
- pilot scope outline `.txt`
- pilot scope outline `.json`

The scope outline is an internal draft only. It is not legal-reviewed and is not a statement of work.
