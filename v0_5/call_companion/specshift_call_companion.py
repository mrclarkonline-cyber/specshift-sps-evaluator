#!/usr/bin/env python3
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
import textwrap

BASE = Path.home() / "specshift_terminal_intelligence"
V05 = BASE / "v0_5"
OUT = BASE / "outreach_drafts"
OUT.mkdir(exist_ok=True)

SCOPING_SCRIPT = V05 / "focused_diagnostic_pilot_scoping_call_script_v0_1.json"
ONE_PAGER = V05 / "specshift_focused_diagnostic_pilot_one_pager_v0_1.pdf"
PILOT_BRIEF_TXT = V05 / "pilot_scoping_brief_v0_1.txt"
CHECKLIST_TXT = V05 / "pilot_appendix_guardrail_checklist_v0_1.txt"

FROM_EMAIL = "ben@specshiftlabs.com"

SIGNATURE = """Benjamin J. Clark
Founder, SpecShift Labs LLC
Interpretation Review Layer
ben@specshiftlabs.com
https://www.specshiftlabs.com/
ORCID: 0009-0005-8622-0251"""

BOUNDARY = (
    "SpecShift Architectural Logic Diagnostics is a pre-deployment diagnostic "
    "and architecture-stage review process. It is not a benchmark, certification, "
    "compliance audit, runtime monitor, security tool, deployment approval, or "
    "guarantee of AI safety."
)

def slug(s):
    s = re.sub(r"[^a-zA-Z0-9]+", "_", str(s).strip().lower()).strip("_")
    return s or "unknown"

def ask(prompt, default=""):
    if default:
        value = input(f"{prompt} [{default}]: ").strip()
        return value or default
    return input(f"{prompt}: ").strip()

def load_script():
    return json.loads(SCOPING_SCRIPT.read_text(encoding="utf-8"))

def print_call_script():
    data = load_script()
    print()
    print("=" * 72)
    print("SpecShift Focused Diagnostic Pilot - 20-Minute Scoping Call")
    print("=" * 72)
    print()
    print("Boundary:")
    print(textwrap.fill(data["standing_boundary_line"], width=88))
    print()
    print("Opening:")
    print(textwrap.fill(data["opening_script"], width=88))
    print()
    print("Agenda:")
    for item in data["agenda"]:
        print(f"- {item}")
    print()
    print("Scoping questions:")
    for i, q in enumerate(data["scoping_questions"], start=1):
        print(f"{i}. {q}")
    print()
    print("Fit signals:")
    for item in data["fit_signals"]:
        print(f"- {item}")
    print()
    print("No-fit signals:")
    for item in data["no_fit_signals"]:
        print(f"- {item}")
    print()
    print("Close:")
    print(textwrap.fill(data["close_script"], width=88))
    print("=" * 72)
    print()

def choose_attachments(stage):
    attachments = [ONE_PAGER]
    notes = ["Focused Diagnostic Pilot One-Pager PDF"]

    if stage == "qualified":
        if PILOT_BRIEF_TXT.exists():
            attachments.append(PILOT_BRIEF_TXT)
            notes.append("Pilot Scoping Brief text")
    elif stage == "deep_interest":
        if PILOT_BRIEF_TXT.exists():
            attachments.append(PILOT_BRIEF_TXT)
            notes.append("Pilot Scoping Brief text")
        if CHECKLIST_TXT.exists():
            attachments.append(CHECKLIST_TXT)
            notes.append("Pilot Appendix Guardrail Checklist text")

    return attachments, notes

def build_followup(contact):
    name = contact.get("name") or "there"
    company = contact.get("company") or "your team"
    workflow = contact.get("workflow") or "the workflow we discussed"
    failure_patterns = contact.get("failure_patterns") or "evidence handling, scope boundaries, handoffs, escalation thresholds, and recovery paths"
    next_step = contact.get("next_step") or "a short pilot scope outline"

    subject = f"SpecShift follow-up: focused diagnostic pilot for {workflow}"

    body = f"""Hi {name},

Thanks for taking the time to discuss {workflow}.

Based on the conversation, the potential fit is a focused diagnostic pilot for one concrete AI-agent workflow at {company}. The review would stay bounded to architecture-stage analysis and selected synthetic scenarios, with attention to: {failure_patterns}.

The likely next step would be {next_step}. A useful pilot scope would define:

- the workflow to review
- the systems or data sources it touches
- the inputs treated as trusted
- the actions the agent can recommend, initiate, or complete
- the human approvals or handoffs currently required
- how stale, incomplete, or conflicting data is handled
- how task completion is verified
- what escalation or recovery path exists if the workflow fails or becomes ambiguous

Boundary: {BOUNDARY}

I attached the focused diagnostic pilot one-pager for context.

Best,
{SIGNATURE}
"""

    return subject, body

def write_email_files(contact, subject, body, attachments):
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"{stamp}_{slug(contact.get('company', 'unknown'))}_{slug(contact.get('name', 'unknown'))}"

    txt = OUT / f"{base_name}_proton_ready_email.txt"
    eml = OUT / f"{base_name}_reference_email.eml"
    notes_json = OUT / f"{base_name}_call_notes.json"
    attach_txt = OUT / f"{base_name}_attachment_paths.txt"

    attachment_lines = "\n".join(str(a) for a in attachments)

    txt.write_text(
        f"""PROTON MAIL READY DRAFT
Copy/paste this into Proton Mail manually.

From: {FROM_EMAIL}
To: {contact.get('email', '')}
Subject: {subject}

{body}

ATTACHMENTS TO ADD MANUALLY:
{attachment_lines}
""",
        encoding="utf-8"
    )

    eml.write_text(
        f"""From: {FROM_EMAIL}
To: {contact.get('email', '')}
Subject: {subject}
Content-Type: text/plain; charset=utf-8

{body}

Attachment paths to add manually:
{attachment_lines}
""",
        encoding="utf-8"
    )

    attach_txt.write_text(attachment_lines + "\n", encoding="utf-8")

    contact_record = dict(contact)
    contact_record["from_email"] = FROM_EMAIL
    contact_record["signature"] = SIGNATURE
    contact_record["subject"] = subject
    contact_record["body"] = body
    contact_record["attachments"] = [str(a) for a in attachments]
    contact_record["created_at"] = datetime.now().isoformat()
    contact_record["email_workflow"] = "Manual send through Proton Mail. No Apple Mail. No auto-send."
    notes_json.write_text(json.dumps(contact_record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return txt, eml, notes_json, attach_txt

def open_outreach_folder():
    print()
    print("Open outreach_drafts folder now? This helps you copy the draft and attach files manually in Proton Mail.")
    choice = ask("Open folder? yes/no", "yes").lower()
    if choice in {"y", "yes"}:
        subprocess.run(["open", str(OUT)], check=False)
        print("Opened outreach_drafts folder.")
    else:
        print("Skipped opening folder.")

def print_generated(txt, eml, notes_json, attach_txt, attachments, attachment_notes):
    print()
    print("Generated Proton-ready materials:")
    print(f"- Copy/paste email draft: {txt}")
    print(f"- Reference .eml archive: {eml}")
    print(f"- Call notes JSON: {notes_json}")
    print(f"- Attachment path list: {attach_txt}")

    print()
    print("Attachments to add manually in Proton Mail:")
    for note, path in zip(attachment_notes, attachments):
        print(f"- {note}: {path}")

    print()
    print("Safety:")
    print("- Nothing was sent.")
    print("- Apple Mail was not used.")
    print("- Open Proton Mail manually.")
    print("- Copy the draft from the TXT file.")
    print("- Add the listed attachments manually.")
    print("- Review before sending.")

def call_mode():
    print_call_script()
    print("Capture call notes")
    print("-" * 72)
    contact = {
        "name": ask("Contact name"),
        "email": ask("Contact email"),
        "company": ask("Company"),
        "role": ask("Role/title"),
        "workflow": ask("Candidate workflow"),
        "systems": ask("Systems/data sources touched"),
        "trusted_inputs": ask("Inputs treated as trusted"),
        "agent_actions": ask("Actions agent can recommend/initiate/complete"),
        "human_handoffs": ask("Human approvals/handoffs/review points"),
        "data_failure_handling": ask("Handling for stale/incomplete/conflicting data"),
        "completion_verification": ask("How completion is verified"),
        "recovery_path": ask("Escalation/recovery path"),
        "failure_patterns": ask("Likely failure patterns to review", "evidence handling, scope boundaries, handoffs, escalation thresholds, and recovery paths"),
        "fit_assessment": ask("Fit assessment: fit / maybe / no-fit", "maybe"),
        "next_step": ask("Next step", "send a short pilot scope outline")
    }

    stage = "qualified" if contact["fit_assessment"].lower() == "fit" else "initial"
    attachments, attachment_notes = choose_attachments(stage)
    subject, body = build_followup(contact)
    txt, eml, notes_json, attach_txt = write_email_files(contact, subject, body, attachments)
    print_generated(txt, eml, notes_json, attach_txt, attachments, attachment_notes)
    open_outreach_folder()

def email_mode():
    print("Generate Proton-ready follow-up email draft")
    print("-" * 72)
    contact = {
        "name": ask("Contact name"),
        "email": ask("Contact email"),
        "company": ask("Company"),
        "role": ask("Role/title"),
        "workflow": ask("Candidate workflow"),
        "failure_patterns": ask("Likely failure patterns to review", "evidence handling, scope boundaries, handoffs, escalation thresholds, and recovery paths"),
        "next_step": ask("Next step", "send a short pilot scope outline")
    }

    stage = ask("Attachment level: initial / qualified / deep_interest", "initial").lower()
    if stage not in {"initial", "qualified", "deep_interest"}:
        stage = "initial"

    attachments, attachment_notes = choose_attachments(stage)
    subject, body = build_followup(contact)
    txt, eml, notes_json, attach_txt = write_email_files(contact, subject, body, attachments)
    print_generated(txt, eml, notes_json, attach_txt, attachments, attachment_notes)
    open_outreach_folder()

def main():
    print("SpecShift Call Companion v0.1 - Proton Mail Manual Draft Workflow")
    print("1. Show scoping script only")
    print("2. Run call mode: script + notes + Proton-ready follow-up draft")
    print("3. Email mode: create Proton-ready follow-up draft from typed contact/workflow")
    choice = ask("Choose 1/2/3", "1")

    if choice == "1":
        print_call_script()
    elif choice == "2":
        call_mode()
    elif choice == "3":
        email_mode()
    else:
        print("Unknown choice. Exiting.")
        raise SystemExit(1)

if __name__ == "__main__":
    main()
