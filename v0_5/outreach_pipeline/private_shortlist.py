#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path

BASE = Path.home() / "specshift_terminal_intelligence"
TARGETS = BASE / "v0_5" / "outreach_pipeline" / "sanitized_company_targets_v0_1.csv"
CONTACTS = Path.home() / ".specshift" / "prospect_contacts_unverified.csv"
SHORTLIST = Path.home() / ".specshift" / "private_outreach_shortlist.csv"

SHORTLIST_FIELDS = [
    "rank",
    "company",
    "contact_name",
    "title",
    "email",
    "matched_pack_or_skin",
    "priority",
    "verification_status",
    "outreach_allowed",
    "reason"
]

PREFERRED_PACKS = [
    "Finance/Reconciliation Agent Diagnostic Pack",
    "Insurance Claims Agent Diagnostic Pack candidate skin",
    "Education/IEP Workflow Diagnostic Pack",
    "Legal Operations Workflow Diagnostic Pack candidate skin",
    "Core Agentic Workflow Diagnostic",
    "Customer Support Escalation Agent Diagnostic Pack",
    "Healthcare Operations Agent Diagnostic Pack",
    "Supply Chain / Logistics Agent Diagnostic Pack candidate skin"
]

def read_csv(path):
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def score_target(target):
    score = 0
    priority = (target.get("priority") or "").lower()
    pack = target.get("matched_pack_or_skin") or ""
    company = target.get("company") or ""

    if priority == "high":
        score += 100
    elif priority == "medium":
        score += 50
    elif priority == "hold_review":
        score -= 1000

    if pack in PREFERRED_PACKS:
        score += 50 - PREFERRED_PACKS.index(pack)

    strong_names = [
        "OpenAI", "Anthropic", "Cognition AI", "Cursor", "GitHub", "Stripe",
        "Ramp", "Brex", "Modern Treasury", "BlackLine", "Workiva",
        "State Farm", "Progressive", "Allstate", "Chubb", "Guidewire",
        "IXL Learning", "PowerSchool", "Instructure", "Khan Academy",
        "Curriculum Associates"
    ]

    if company in strong_names:
        score += 75

    return score

def build(args):
    targets = read_csv(TARGETS)
    contacts = read_csv(CONTACTS)

    contacts_by_company = {}
    for c in contacts:
        company = (c.get("company") or "").strip().lower()
        if company:
            contacts_by_company.setdefault(company, []).append(c)

    joined = []
    for t in targets:
        company = (t.get("company") or "").strip()
        if not company:
            continue

        if (t.get("priority") or "").lower() == "hold_review" and not args.include_hold:
            continue

        company_contacts = contacts_by_company.get(company.lower(), [])
        if not company_contacts:
            continue

        for c in company_contacts:
            joined.append({
                "score": score_target(t),
                "company": company,
                "contact_name": c.get("contact_name", ""),
                "title": c.get("title", ""),
                "email": c.get("email", ""),
                "matched_pack_or_skin": t.get("matched_pack_or_skin", ""),
                "priority": t.get("priority", ""),
                "verification_status": c.get("verification_status", "unverified"),
                "outreach_allowed": c.get("outreach_allowed", "no"),
                "reason": "High-fit company target with private contact preserved under Choice C"
            })

    joined.sort(key=lambda r: (-r["score"], r["company"].lower(), r["contact_name"].lower()))
    selected = joined[:args.limit]

    SHORTLIST.parent.mkdir(parents=True, exist_ok=True)
    with SHORTLIST.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SHORTLIST_FIELDS)
        writer.writeheader()
        for i, row in enumerate(selected, start=1):
            out = {k: row.get(k, "") for k in SHORTLIST_FIELDS}
            out["rank"] = i
            writer.writerow(out)

    SHORTLIST.chmod(0o600)

    print(f"Private contacts available: {len(contacts)}")
    print(f"Company targets available: {len(targets)}")
    print(f"Shortlist written: {SHORTLIST}")
    print(f"Shortlist rows: {len(selected)}")
    print()
    print("Top preview, emails masked:")
    for i, row in enumerate(selected[:15], start=1):
        email = row.get("email", "")
        masked = email
        if "@" in email:
            local, domain = email.split("@", 1)
            masked = local[:2] + "***@" + domain
        print(f"{i}. {row['company']} | {row['contact_name']} | {row['matched_pack_or_skin']} | {masked}")

def main():
    parser = argparse.ArgumentParser(description="Build private SpecShift outreach shortlist")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--include-hold", action="store_true")
    args = parser.parse_args()
    build(args)

if __name__ == "__main__":
    main()
