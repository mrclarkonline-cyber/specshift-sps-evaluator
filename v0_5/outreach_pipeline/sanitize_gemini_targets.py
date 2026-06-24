#!/usr/bin/env python3
import csv
import json
import re
from pathlib import Path
from datetime import datetime

BASE = Path.home() / "specshift_terminal_intelligence"
PIPE = BASE / "v0_5" / "outreach_pipeline"

RAW = PIPE / "gemini_raw_unverified_company_targets_v0_1.csv"
SAN = PIPE / "sanitized_company_targets_v0_1.csv"
REPORT = PIPE / "sanitized_company_targets_report_v0_1.json"

APPROVED_PACKS = {
    "finance": "Finance/Reconciliation Agent Diagnostic Pack",
    "procurement": "Procurement Agent Diagnostic Pack",
    "customer": "Customer Support Escalation Agent Diagnostic Pack",
    "healthcare": "Healthcare Operations Agent Diagnostic Pack",
    "education": "Education/IEP Workflow Diagnostic Pack",
    "legal": "Legal Operations Workflow Diagnostic Pack candidate skin",
    "insurance": "Insurance Claims Agent Diagnostic Pack candidate skin",
    "hr": "HR Operations Agent Diagnostic Pack candidate skin",
    "supply": "Supply Chain / Logistics Agent Diagnostic Pack candidate skin",
    "incident": "Incident Response Coordination Pack candidate skin",
    "sales": "Sales / CRM Agent Diagnostic Pack candidate skin",
    "government": "Government Services Workflow Pack candidate skin",
    "core": "Core Agentic Workflow Diagnostic"
}

RISKY_WORDS = [
    "audit", "auditing", "assurance", "safety", "security", "compliance",
    "certification", "validation", "validated", "deployment approval",
    "defense", "autonomous", "weapon", "mission", "border", "drone",
    "clinical decision", "medical decision", "legal advice", "eligibility",
    "coverage determination", "hiring decision", "employee evaluation"
]

def norm_company(name):
    name = (name or "").strip()
    aliases = {
        "Google / Alphabet": "Google / Alphabet",
        "Alphabet": "Google / Alphabet",
        "Google DeepMind": "Google / Alphabet",
        "Google Cloud": "Google / Alphabet",
        "Microsoft Azure": "Microsoft",
        "Microsoft Nuance": "Microsoft Nuance",
        "Amazon Web Services": "Amazon",
        "AWS": "Amazon",
        "Alibaba Cloud": "Alibaba",
        "Alibaba DAMO Academy": "Alibaba",
        "Huawei Cloud": "Huawei",
        "Huawei Noah’s Ark Lab": "Huawei",
        "Target Tech": "Target",
        "Walmart Global Tech": "Walmart",
        "QuickBooks": "Intuit / QuickBooks",
        "Intuit": "Intuit / QuickBooks",
        "Netsuite": "Oracle NetSuite",
        "Oracle": "Oracle",
        "Oracle Health": "Oracle Health",
        "Snowflake Cortex": "Snowflake",
        "Ironclad AI": "Ironclad",
        "Scale AI Labs": "Scale AI",
        "LangSmith": "LangChain / LangSmith",
        "LangChain": "LangChain / LangSmith",
        "Milvus": "Zilliz / Milvus",
        "Zilliz": "Zilliz / Milvus"
    }
    return aliases.get(name, name)

def safe_workflow(text):
    t = (text or "").strip()
    replacements = {
        "Auditing": "review",
        "auditing": "review",
        "Audit": "Review",
        "audit": "review",
        "Assurance": "Review",
        "assurance": "review",
        "Safety": "Reliability",
        "safety": "reliability",
        "Security": "Boundary",
        "security": "boundary",
        "Compliance": "Process",
        "compliance": "process",
        "Validation": "Review",
        "validation": "review",
        "Validated": "Reviewed",
        "validated": "reviewed"
    }
    for old, new in replacements.items():
        t = t.replace(old, new)
    return t

def classify(row):
    company = row.get("company", "")
    category = (row.get("category", "") or "").lower()
    workflow = (row.get("likely_workflow", "") or "").lower()
    pack = (row.get("matched_pack_or_skin", "") or "").lower()
    blob = " ".join([company.lower(), category, workflow, pack])

    hold = False
    reasons = []

    if any(x in blob for x in ["defense", "mission", "border", "drone", "autonomous flight", "weapon", "frontline"]):
        hold = True
        reasons.append("defense/autonomy licensing review required")

    if any(x in blob for x in ["clinical decision", "medical decision", "diagnosis", "radiology decision", "disease detection"]):
        reasons.append("healthcare professional-boundary review required")

    if any(x in blob for x in ["legal advice", "contract approval", "eligibility", "coverage determination", "hiring decision"]):
        reasons.append("professional-decision boundary review required")

    if any(x in blob for x in ["finance", "financial", "payments", "ledger", "billing", "bank", "tax", "accounting", "reconciliation", "revenue", "subscription", "treasury"]):
        lane = APPROVED_PACKS["finance"]
    elif any(x in blob for x in ["procure", "spend", "supplier", "erp", "coupa"]):
        lane = APPROVED_PACKS["procurement"]
    elif any(x in blob for x in ["support", "customer", "conversation", "cx", "service"]):
        lane = APPROVED_PACKS["customer"]
    elif any(x in blob for x in ["health", "ehr", "clinical", "patient", "payer", "pharmacy", "medical", "life sciences"]):
        lane = APPROVED_PACKS["healthcare"]
    elif any(x in blob for x in ["education", "edtech", "student", "lms", "assessment", "learning"]):
        lane = APPROVED_PACKS["education"]
    elif any(x in blob for x in ["legal", "contract", "ediscovery", "e-discovery", "agreement", "law"]):
        lane = APPROVED_PACKS["legal"]
    elif any(x in blob for x in ["insurance", "claims", "coverage"]):
        lane = APPROVED_PACKS["insurance"]
    elif any(x in blob for x in ["hr", "human resources", "workday", "benefits", "employee"]):
        lane = APPROVED_PACKS["hr"]
    elif any(x in blob for x in ["supply", "logistics", "freight", "shipping", "inventory", "fulfillment", "delivery", "warehouse"]):
        lane = APPROVED_PACKS["supply"]
    elif any(x in blob for x in ["incident", "runbook", "pager", "observability", "alert", "soc"]):
        lane = APPROVED_PACKS["incident"]
    elif any(x in blob for x in ["sales", "crm", "deal", "revenue operations"]):
        lane = APPROVED_PACKS["sales"]
    elif any(x in blob for x in ["government", "public service", "federal", "agency"]):
        lane = APPROVED_PACKS["government"]
    else:
        lane = APPROVED_PACKS["core"]

    if hold:
        priority = "hold_review"
    else:
        raw_priority = (row.get("priority", "") or "").strip().lower()
        priority = raw_priority if raw_priority in {"high", "medium", "low"} else "medium"

    risky_hits = sorted({w for w in RISKY_WORDS if w in blob})
    if risky_hits and "risky wording sanitized" not in reasons:
        reasons.append("risky wording sanitized")

    return lane, priority, "; ".join(reasons), ", ".join(risky_hits)

def main():
    if not RAW.exists():
        print(f"Missing input CSV: {RAW}")
        print("Create it by pasting Gemini's CSV into that file, then rerun.")
        raise SystemExit(1)

    with RAW.open("r", newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    seen = {}
    output = []
    risky_total = 0
    hold_total = 0

    for row in rows:
        company = norm_company(row.get("company", ""))
        if not company:
            continue

        lane, priority, notes, risky_hits = classify(row)
        if priority == "hold_review":
            hold_total += 1
        if risky_hits:
            risky_total += 1

        clean = {
            "company": company,
            "category": row.get("category", "").strip(),
            "likely_workflow": safe_workflow(row.get("likely_workflow", "")),
            "matched_pack_or_skin": lane,
            "priority": priority,
            "verification_status": "unverified",
            "contact_status": "company_only_no_contact_verified",
            "outreach_allowed": "no",
            "requires_independent_contact_verification": "yes",
            "notes": notes,
            "risky_terms_found": risky_hits
        }

        key = company.lower()
        if key not in seen:
            seen[key] = clean
        else:
            old = seen[key]
            rank = {"high": 3, "medium": 2, "low": 1, "hold_review": 0}
            if rank.get(clean["priority"], 0) > rank.get(old["priority"], 0):
                old["priority"] = clean["priority"]
            if clean["matched_pack_or_skin"] != old["matched_pack_or_skin"]:
                old["notes"] = (old["notes"] + "; duplicate had alternate lane: " + clean["matched_pack_or_skin"]).strip("; ")

    output = sorted(seen.values(), key=lambda r: (r["priority"] != "high", r["priority"] != "medium", r["company"].lower()))

    fields = [
        "company",
        "category",
        "likely_workflow",
        "matched_pack_or_skin",
        "priority",
        "verification_status",
        "contact_status",
        "outreach_allowed",
        "requires_independent_contact_verification",
        "notes",
        "risky_terms_found"
    ]

    with SAN.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output)

    report = {
        "artifact_name": "Sanitized Company Targets Report v0.1",
        "created_at": datetime.now().isoformat(),
        "input_csv": str(RAW),
        "output_csv": str(SAN),
        "input_rows": len(rows),
        "deduplicated_company_rows": len(output),
        "rows_with_risky_terms": risky_total,
        "hold_review_rows": hold_total,
        "rule": "Company targets only. All contacts unverified. Outreach not allowed until independent contact verification.",
        "approved_pack_skin_vocabulary": sorted(set(APPROVED_PACKS.values())),
        "not_for_memory": True
    }

    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
