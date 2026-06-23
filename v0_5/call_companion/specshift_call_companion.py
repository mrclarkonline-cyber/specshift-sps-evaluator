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
SUITE_PATH = V05 / "unknown_domain_adversarial_suite_v0_5.json"

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

def load_suite_cases():
    data = json.loads(SUITE_PATH.read_text(encoding="utf-8"))
    return data.get("test_cases", [])

def select_relevant_cases(contact, limit=7):
    workflow_text = " ".join([
        str(contact.get("workflow", "")),
        str(contact.get("systems", "")),
        str(contact.get("trusted_inputs", "")),
        str(contact.get("agent_actions", "")),
        str(contact.get("human_handoffs", "")),
        str(contact.get("data_failure_handling", "")),
        str(contact.get("completion_verification", "")),
        str(contact.get("recovery_path", "")),
        str(contact.get("failure_patterns", "")),
    ]).lower()

    keyword_map = {
        "provenance": ["unverified", "input", "source", "document", "email", "screenshot", "proxy", "evidence", "trusted", "attachment"],
        "stale_state": ["stale", "old", "outdated", "cache", "current", "timestamp", "data freshness", "inventory"],
        "scope": ["permission", "approval", "authorize", "authority", "spending", "procurement", "scope", "limit", "policy"],
        "handoff": ["handoff", "owner", "ownership", "human", "review", "legal", "finance", "approval"],
        "completion": ["complete", "final", "done", "archive", "closed", "task completion", "verification"],
        "recovery": ["rollback", "recover", "recovery", "escalation", "fallback", "error", "wrong payment"],
        "multi_system": ["crm", "billing", "finance", "inventory", "erp", "systems", "database", "shipping", "reconciliation"],
        "boundary": ["legal", "hr", "clinical", "distress", "safety", "professional", "high-risk", "consequences"],
        "pseudo_rigor": ["model", "framework", "math", "prediction", "neutral", "governance", "confidence", "complete"],
        "infrastructure": ["offline", "network", "low-resource", "manual", "spreadsheet", "physical", "analog"]
    }

    category_weights = {
        "provenance": ["provenance", "proxy", "payload"],
        "stale_state": ["stale", "latent", "state"],
        "scope": ["scope", "authority", "permission", "policy"],
        "handoff": ["handoff", "ownership", "human"],
        "completion": ["completion", "final-state", "false"],
        "recovery": ["rollback", "recovery", "circular"],
        "multi_system": ["multi-system", "synchronization", "state", "reconciliation"],
        "boundary": ["boundary", "professional", "distress", "customary", "cross-cultural"],
        "pseudo_rigor": ["pseudo", "decorative", "neutral", "moral", "claim"],
        "infrastructure": ["infrastructure", "analog", "digital", "degraded"]
    }

    active_signals = []
    for signal, words in keyword_map.items():
        if any(word in workflow_text for word in words):
            active_signals.append(signal)

    if not active_signals:
        active_signals = ["provenance", "scope", "stale_state", "completion", "handoff", "recovery"]

    scored = []
    for case in load_suite_cases():
        haystack = " ".join([
            str(case.get("id", "")),
            str(case.get("category", "")),
            str(case.get("adversarial_prompt", "")),
            str(case.get("target_failure_mode", "")),
            str(case.get("failure_column", ""))
        ]).lower()

        score = 0
        reasons = []

        for signal in active_signals:
            for marker in category_weights.get(signal, []):
                if marker in haystack:
                    score += 3
                    reasons.append(signal)
                    break

        for word in workflow_text.split():
            if len(word) > 5 and word in haystack:
                score += 1

        if score > 0:
            scored.append((score, case, sorted(set(reasons))))

    scored.sort(key=lambda x: (-x[0], x[1].get("id", "")))
    selected = scored[:limit]

    if len(selected) < min(limit, 5):
        fallback_ids = {"01", "04", "06", "07", "10", "12", "13", "20", "23", "25"}
        existing = {item[1].get("id") for item in selected}
        for case in load_suite_cases():
            if case.get("id") in fallback_ids and case.get("id") not in existing:
                selected.append((1, case, ["default_first_pass"]))
                existing.add(case.get("id"))
            if len(selected) >= limit:
                break

    result = []
    for score, case, reasons in selected:
        result.append({
            "id": case.get("id"),
            "category": case.get("category"),
            "target_failure_mode": case.get("target_failure_mode"),
            "failure_column": case.get("failure_column"),
            "selection_reasons": reasons,
            "score": score
        })

    return result

def write_case_selection(contact):
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"{stamp}_{slug(contact.get('company', 'unknown'))}_{slug(contact.get('name', 'unknown'))}"
    cases_txt = OUT / f"{base_name}_selected_v0_5_cases.txt"
    cases_json = OUT / f"{base_name}_selected_v0_5_cases.json"

    selected = select_relevant_cases(contact)

    lines = [
        "Selected v0.5 Candidate Cases for Focused Diagnostic Pilot",
        "Internal case-selection aid. Not buyer-facing final copy.",
        "",
        f"Company: {contact.get('company', '')}",
        f"Workflow: {contact.get('workflow', '')}",
        "",
        "Boundary:",
        BOUNDARY,
        "",
        "Selected cases:"
    ]

    for item in selected:
        lines.append("")
        lines.append(f"Case {item['id']} - {item['category']}")
        lines.append(f"Target failure mode: {item['target_failure_mode']}")
        lines.append(f"Selection reasons: {', '.join(item['selection_reasons'])}")
        lines.append(f"Failure column: {item['failure_column']}")

    lines.append("")
    lines.append("Use note:")
    lines.append("Use these cases as a starting selection only. Final pilot scope should be manually reviewed and narrowed to match the actual buyer workflow.")
    lines.append("")

    cases_txt.write_text("\n".join(lines), encoding="utf-8")

    record = {
        "artifact_name": "Selected v0.5 Candidate Cases for Focused Diagnostic Pilot",
        "status": "internal case-selection aid, not buyer-facing final copy",
        "contact": contact,
        "selected_cases": selected,
        "boundary": BOUNDARY,
        "use_note": "Starting selection only; manually review before pilot proposal.",
        "created_at": datetime.now().isoformat()
    }
    cases_json.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return cases_txt, cases_json

def build_pilot_scope_outline(contact):
    company = contact.get("company") or "the buyer"
    workflow = contact.get("workflow") or "the selected workflow"
    systems = contact.get("systems") or "to be confirmed"
    trusted_inputs = contact.get("trusted_inputs") or "to be confirmed"
    agent_actions = contact.get("agent_actions") or "to be confirmed"
    human_handoffs = contact.get("human_handoffs") or "to be confirmed"
    data_failure_handling = contact.get("data_failure_handling") or "to be confirmed"
    completion_verification = contact.get("completion_verification") or "to be confirmed"
    recovery_path = contact.get("recovery_path") or "to be confirmed"
    failure_patterns = contact.get("failure_patterns") or "evidence handling, scope boundaries, handoffs, escalation thresholds, and recovery paths"
    selected_cases = select_relevant_cases(contact)
    selected_case_summary = "\n".join(
        f"- Case {item['id']} ({item['category']}): {item['target_failure_mode']}"
        for item in selected_cases
    ) or "- To be selected after workflow scoping"

    return f"""Focused Diagnostic Pilot Scope Outline

Status:
Internal scope outline draft. Not legal-reviewed. Not a statement of work.

Buyer / organization:
{company}

Selected workflow:
{workflow}

Pilot purpose:
Run a bounded, pre-deployment diagnostic review of one concrete AI-agent workflow using selected synthetic scenarios. The review is intended to surface candidate failure patterns and design-review gaps before broader rollout.

Standing boundary:
{BOUNDARY}

Candidate failure patterns to review:
{failure_patterns}

Selected v0.5 candidate cases:
{selected_case_summary}

Known workflow context:
- Systems or data sources touched: {systems}
- Inputs treated as trusted: {trusted_inputs}
- Agent actions: {agent_actions}
- Human approvals, handoffs, or review points: {human_handoffs}
- Handling for stale, incomplete, conflicting, or low-fidelity data: {data_failure_handling}
- Task-completion verification: {completion_verification}
- Escalation, rollback, or recovery path: {recovery_path}

Proposed review focus:
1. Input evidence and provenance handling
2. Scope and approval boundary clarity
3. Multi-system state or handoff gaps
4. False task-completion or premature closure risk
5. Escalation and recovery-path adequacy

Expected deliverables:
- Executive findings memo
- Failure-pattern review against selected synthetic scenarios
- Limitation and boundary map
- Handoff, evidence, escalation, and recovery-path gap list
- Recommended design-review next steps

Buyer-provided materials needed:
- Workflow description or architecture sketch
- Representative prompts, tasks, or decision paths
- Description of systems, data sources, approvals, and handoffs
- Any known failure concerns or prior examples, if available
- Confirmation of what materials can be used for review

Fit gate:
Green if there is one concrete workflow, meaningful downside if it fails silently, enough bounded context for review, and willingness to treat this as diagnostic rather than certification.

Yellow if the workflow is real but context, access, or decision owner is unclear.

Red if the buyer wants certification, compliance sign-off, runtime protection, cybersecurity testing, deployment approval, free consulting, or guaranteed safety.

Next step:
Confirm whether this scope is accurate. If yes, convert this outline into a narrow pilot proposal with milestones, deliverables, non-certification language, and an off-ramp condition.

Failure column:
This scope outline stops fitting if the buyer expects certification, compliance approval, runtime monitoring, security testing, deployment approval, legal advice, HR decision-making, or guaranteed safety.
"""

def write_scope_outline(contact):
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"{stamp}_{slug(contact.get('company', 'unknown'))}_{slug(contact.get('name', 'unknown'))}"
    scope_txt = OUT / f"{base_name}_pilot_scope_outline.txt"
    scope_json = OUT / f"{base_name}_pilot_scope_outline.json"

    outline = build_pilot_scope_outline(contact)
    scope_txt.write_text(outline, encoding="utf-8")

    record = {
        "artifact_name": "Focused Diagnostic Pilot Scope Outline",
        "status": "internal scope outline draft, not legal-reviewed, not statement of work",
        "contact": contact,
        "outline": outline,
        "created_at": datetime.now().isoformat(),
        "boundary": BOUNDARY
    }
    scope_json.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return scope_txt, scope_json

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
    scope_txt, scope_json = write_scope_outline(contact)
    cases_txt, cases_json = write_case_selection(contact)
    print_generated(txt, eml, notes_json, attach_txt, attachments, attachment_notes)
    print()
    print("Generated pilot scope outline:")
    print(f"- Scope TXT: {scope_txt}")
    print(f"- Scope JSON: {scope_json}")
    print()
    print("Generated selected v0.5 case list:")
    print(f"- Cases TXT: {cases_txt}")
    print(f"- Cases JSON: {cases_json}")
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
    scope_txt, scope_json = write_scope_outline(contact)
    cases_txt, cases_json = write_case_selection(contact)
    print_generated(txt, eml, notes_json, attach_txt, attachments, attachment_notes)
    print()
    print("Generated pilot scope outline:")
    print(f"- Scope TXT: {scope_txt}")
    print(f"- Scope JSON: {scope_json}")
    print()
    print("Generated selected v0.5 case list:")
    print(f"- Cases TXT: {cases_txt}")
    print(f"- Cases JSON: {cases_json}")
    open_outreach_folder()

def main():
    print("SpecShift Call Companion v0.1 - Proton Mail Manual Draft Workflow")
    print("1. Show scoping script only")
    print("2. Run call mode: script + notes + Proton-ready follow-up draft + scope outline")
    print("3. Email mode: create Proton-ready follow-up draft + scope outline")
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
