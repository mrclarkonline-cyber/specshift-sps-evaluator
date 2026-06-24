#!/usr/bin/env python3
import csv
import json
import re
from pathlib import Path
from datetime import datetime

BASE = Path.home() / "specshift_terminal_intelligence"
PIPE = BASE / "v0_5" / "outreach_pipeline"
PRIVATE = Path.home() / ".specshift"
INTAKE = PRIVATE / "incoming_lead_lists"

SOURCE_FILES = [
    INTAKE / "gemini-code-1782321032078.txt",
    INTAKE / "gemini-code-1782321056788.txt",
]

PRIVATE_CONTACTS = PRIVATE / "prospect_contacts_unverified.csv"
RAW_COMPANY = PIPE / "gemini_raw_unverified_company_targets_v0_1.csv"
SUMMARY = PIPE / "choice_c_overflow_safe_rebuild_summary_v0_1.json"

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-']+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")

PRIVATE_FIELDS = [
    "company",
    "contact_name",
    "title",
    "email",
    "source_file",
    "source",
    "verification_status",
    "outreach_allowed",
    "notes"
]

COMPANY_FIELDS = [
    "company",
    "category",
    "likely_workflow",
    "matched_pack_or_skin",
    "priority",
    "verification_status"
]

def find_header(lines):
    for i, line in enumerate(lines):
        low = line.lower().replace(" ", "").replace('"', "")
        if low.startswith("company,name,title,email") or low.startswith("company,contactname,title,email"):
            return i
    raise SystemExit("CSV header not found.")

def parse_file(path):
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    lines = [line for line in text.splitlines() if line.strip()]
    start = find_header(lines)
    useful = lines[start:]

    parsed = []
    reader = csv.reader(useful)
    header = next(reader)

    for row in reader:
        if not row or len(row) < 4:
            continue

        company = row[0].strip()
        name = row[1].strip()

        # Overflow-safe rule:
        # first field = company
        # second field = name/contact name
        # last field = email
        # everything between = title
        email = row[-1].strip()
        title = ", ".join(x.strip() for x in row[2:-1] if x is not None).strip()

        if not company:
            continue

        parsed.append({
            "company": company,
            "contact_name": name,
            "title": title,
            "email": email,
            "source_file": path.name,
            "source": "user_provided_raw_csv",
            "verification_status": "unverified",
            "outreach_allowed": "no",
            "notes": "Choice C overflow-safe rebuild. Verify independently before outreach."
        })

    return parsed

def classify(company, title):
    blob = f"{company} {title}".lower()

    if any(x in blob for x in ["insurance", "claims", "underwriting", "payer", "health plan", "reinsurance"]):
        return "Insurance", "Claims intake, evidence handling, underwriting support, escalation, and recovery-path review", "Insurance Claims Agent Diagnostic Pack candidate skin", "High"

    if any(x in blob for x in ["payment", "ledger", "billing", "accounting", "finance", "banking", "tax", "treasury", "reconciliation"]):
        return "Finance", "Financial workflow, reconciliation, evidence handling, escalation, and recovery-path review", "Finance/Reconciliation Agent Diagnostic Pack", "High"

    if any(x in blob for x in ["education", "learning", "student", "school", "lms", "assessment", "classroom", "khan", "quizlet", "coursera", "pearson", "ixl"]):
        return "Education", "Student support, recommendation, assessment, intervention, content-routing, and progress-monitoring workflow review", "Education/IEP Workflow Diagnostic Pack", "High"

    if any(x in blob for x in ["legal", "contract", "agreement", "ediscovery", "e-discovery"]):
        return "Legal Operations", "Legal-operations intake, document-routing, provenance, handoff, and boundary review", "Legal Operations Workflow Diagnostic Pack candidate skin", "High"

    if any(x in blob for x in ["health", "clinical", "medical", "ehr", "patient", "pharmacy", "hospital"]):
        return "Healthcare Operations", "Healthcare operations, intake, documentation, routing, escalation, and recovery-path review", "Healthcare Operations Agent Diagnostic Pack", "High"

    if any(x in blob for x in ["github", "gitlab", "cursor", "cognition", "replit", "devtool", "code", "developer", "ide"]):
        return "DevTools", "Agentic software, code-generation, task-completion, handoff, and evidence-boundary review", "Core Agentic Workflow Diagnostic", "High"

    if any(x in blob for x in ["logistics", "delivery", "freight", "shipping", "warehouse", "fulfillment", "inventory"]):
        return "Supply Chain / Logistics", "Supply chain, logistics, inventory-state, handoff, and recovery-path review", "Supply Chain / Logistics Agent Diagnostic Pack candidate skin", "Medium"

    if any(x in blob for x in ["defense", "mission", "autonomous flight", "drone", "border", "weapon"]):
        return "Hold Review", "Licensing-boundary review required before any outreach or engagement", "HOLD_REVIEW", "hold_review"

    return "Core AI / Enterprise", "Agentic workflow, evidence handling, scope boundary, handoff, escalation, and recovery-path review", "Core Agentic Workflow Diagnostic", "Medium"

def main():
    contacts = []
    for path in SOURCE_FILES:
        contacts.extend(parse_file(path))

    deduped_contacts = []
    seen_contact = set()
    invalid_emails = []

    for i, row in enumerate(contacts, start=1):
        key = (
            row["company"].lower(),
            row["contact_name"].lower(),
            row["email"].lower()
        )
        if key in seen_contact:
            continue
        seen_contact.add(key)
        deduped_contacts.append(row)

        email = row["email"].strip()
        if email not in {"N/A", "n/a", "NA", "na", ""} and not EMAIL_RE.match(email):
            invalid_emails.append({
                "row": i,
                "company": row["company"],
                "contact_name": row["contact_name"],
                "email": email,
                "title": row["title"]
            })

    PRIVATE.mkdir(parents=True, exist_ok=True)
    with PRIVATE_CONTACTS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=PRIVATE_FIELDS)
        writer.writeheader()
        writer.writerows(deduped_contacts)
    PRIVATE_CONTACTS.chmod(0o600)

    company_rows = []
    seen_company = set()
    for row in deduped_contacts:
        company = row["company"].strip()
        if not company:
            continue
        key = company.lower()
        if key in seen_company:
            continue
        seen_company.add(key)
        category, workflow, pack, priority = classify(company, row["title"])
        company_rows.append({
            "company": company,
            "category": category,
            "likely_workflow": workflow,
            "matched_pack_or_skin": pack,
            "priority": priority,
            "verification_status": "unverified"
        })

    with RAW_COMPANY.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COMPANY_FIELDS)
        writer.writeheader()
        writer.writerows(company_rows)

    summary = {
        "artifact_name": "Choice C Overflow-Safe Rebuild Summary v0.1",
        "created_at": datetime.now().isoformat(),
        "source_files": [str(p) for p in SOURCE_FILES],
        "private_contacts_total": len(deduped_contacts),
        "company_targets_total": len(company_rows),
        "invalid_non_na_email_rows": len(invalid_emails),
        "private_contacts_file": str(PRIVATE_CONTACTS),
        "repo_company_targets_file": str(RAW_COMPANY),
        "rule": "Private contacts rebuilt from source using overflow-safe parse. No email sent. Company targets only in repo."
    }

    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=2, ensure_ascii=False))

    if invalid_emails:
        print()
        print("Invalid email preview:")
        for row in invalid_emails[:25]:
            print(f"{row['company']} | {row['contact_name']} | email={row['email']!r} | title={row['title']!r}")

if __name__ == "__main__":
    main()
