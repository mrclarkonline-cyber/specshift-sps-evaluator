#!/usr/bin/env python3
import csv
import json
import re
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict

BASE = Path.home() / "specshift_terminal_intelligence"
PIPE = BASE / "v0_5" / "outreach_pipeline"
PRIVATE = Path.home() / ".specshift"
CONTACTS = PRIVATE / "prospect_contacts_unverified.csv"
COMPANY_TARGETS = PIPE / "sanitized_company_targets_v0_1.csv"
OUTDIR = PRIVATE / "private_wave_queues_v0_1"

ASSIGN_OUT = PIPE / "choice_c_company_wave_assignments_v0_1.csv"
SUMMARY_OUT = PIPE / "choice_c_wave_summary_v0_1.json"

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-']+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")
CITE_RE = re.compile(r"\s*\[cite:\s*\d+\]\s*$", re.I)

PRIVATE_FIELDS = [
    "company",
    "contact_name",
    "title",
    "email",
    "outreach_wave",
    "wave_name",
    "classification_category",
    "manual_review",
    "send_policy",
    "verification_status",
    "outreach_allowed",
    "wave_reason",
    "source_file",
    "notes"
]

ASSIGN_FIELDS = [
    "company",
    "outreach_wave",
    "wave_name",
    "classification_category",
    "manual_review",
    "send_policy",
    "wave_reason"
]

WAVE_FILES = {
    "Wave 0": "private_wave0_hygiene_all_contacts.csv",
    "Wave 1": "private_wave1_precision_pilot_seekers.csv",
    "Wave 2": "private_wave2_finance_devtools_expansion.csv",
    "Wave 3": "private_wave3_support_procurement_incident.csv",
    "Wave 4": "private_wave4_category_validators_partners.csv",
    "Wave 5": "private_wave5_regulated_long_cycle.csv",
    "Wave 6": "private_wave6_reserve_pool.csv",
}

WAVE_NAMES = {
    "Wave 0": "Hygiene and verification, not a send wave",
    "Wave 1": "Precision pilot seekers",
    "Wave 2": "Finance and devtools expansion",
    "Wave 3": "Support, procurement, and incident-response buyers",
    "Wave 4": "Category validators, partners, and adjacent evaluators",
    "Wave 5": "Regulated, critical, and long-cycle sectors",
    "Wave 6": "Reserve pool"
}

# High-fit first commercial wave. This is not automatic send approval.
WAVE1_EXACT = {
    "Cognition AI", "Anysphere", "Cursor", "Glean", "Sierra", "Decagon", "Cresta",
    "LangChain", "LangSmith", "LlamaIndex", "Harvey",
    "Modern Treasury", "Ramp", "Stripe", "BlackLine", "Workiva",
}

WAVE2_EXACT = {
    "Adyen", "Anrok", "Brex", "Chargebee", "Leapfin", "Marqeta", "Mercury",
    "Plaid", "QuickBooks", "Xero", "Zuora", "FloQast", "Airbase", "AppZen",
    "Candex", "Corcentric", "Divvy", "Earnix", "Emburse", "Expensify", "FIS",
    "Fiserv", "Justworks", "Klarna", "Marqeta", "Mesh Payments", "MineralTree",
    "Navan", "Oversight", "Papaya Global", "Paycom", "Paycor", "Payhawk",
    "Paylocity", "Pleo", "Pricefx", "Procurify", "Revolut Business", "Rippling",
    "Soldo", "Spendesk", "Taulia", "Teampay", "Tipalti", "Tradeshift", "Wise",
    "Zip"
}

WAVE3_EXACT = {
    "Ada", "Agiloft", "Balto", "Basware", "Conga", "Coupa", "Cresta", "Decagon",
    "Dialpad", "Dialpad Ai Contact Center", "DocuSign CLM", "Evisort", "Fairmarkit",
    "Five9", "Forethought", "Freshdesk", "Freshservice", "Freshworks", "Genesys",
    "Gladly", "Globality", "Gorgias", "Help Scout", "Icertis", "Intercom", "Ironclad",
    "Ironclad AI", "Ivalua", "Jaggaer", "Keelvar", "Kustomer", "LegalOn", "LivePerson",
    "Maven AGI", "Medallia", "Medius", "NICE", "NICE CXone", "Observe.AI",
    "Oracle Procurement Cloud", "Precoro", "Salesforce Service Cloud", "SAP Ariba",
    "Scout RFP", "ServiceNow", "ServiceNow Customer Service Management", "Sirion",
    "Talkdesk", "Tropic", "Twilio Flex", "Uniphore", "UserTesting", "UserVoice",
    "Vendr", "Verint", "Workday Strategic Sourcing", "Zendesk", "Zendesk Sell", "Zycus"
}

WAVE4_EXACT = {
    "Accenture", "Appen", "Arize AI", "Arthur AI", "Booz Allen Hamilton", "CalypsoAI",
    "Capgemini", "Casetext", "Chainalysis", "Cognizant", "Credo AI", "Deloitte",
    "DISCO", "EPAM", "EY", "Faculty AI", "Fiddler AI", "Galileo", "Globant",
    "Harvey", "HCLTech", "HiddenLayer", "Holistic AI", "Humanloop", "Infosys",
    "Invisible Technologies", "iMerit", "KPMG", "Lakera", "LexisNexis", "NTT Data",
    "OneTrust", "Patronus AI", "Primer AI", "Protect AI", "PwC", "Relativity",
    "Robust Intelligence", "TCS", "Thomson Reuters", "Thoughtworks", "WhyLabs", "Wipro"
}

SENSITIVE_EXACT = {
    "OpenAI", "Anthropic", "Google DeepMind", "Google Cloud", "Alphabet", "Microsoft",
    "Microsoft Azure", "Amazon", "Amazon Web Services", "Amazon Web Services (AWS)",
    "Apple", "Meta", "NVIDIA", "xAI", "DeepSeek", "Qwen", "01.AI", "Alibaba Cloud",
    "Alibaba DAMO Academy", "Baidu", "Baidu Research", "ByteDance", "Huawei Cloud",
    "Huawei Noah’s Ark Lab", "JD Cloud", "SenseTime", "Tencent", "Tencent AI Lab",
    "Zhipu AI", "iFlytek", "MiniMax", "Moonshot AI", "Palantir", "Anduril", "Shield AI",
    "Helsing", "Leidos", "SAIC", "Axon", "Booz Allen Hamilton"
}

def clean_email(email):
    email = (email or "").strip()
    email = CITE_RE.sub("", email).strip()
    return email

def read_csv(path):
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def blob_contains(blob, terms):
    return any(term in blob for term in terms)

def assign_company(company):
    c = company.strip()
    blob = c.lower()

    manual_review = "no"
    send_policy = "not_allowed_until_verified"

    if c in SENSITIVE_EXACT:
        manual_review = "yes"
        send_policy = "manual_individual_review_only"

    if c in WAVE1_EXACT:
        return {
            "outreach_wave": "Wave 1",
            "classification_category": "Precision pilot seeker",
            "manual_review": manual_review,
            "send_policy": send_policy,
            "wave_reason": "Highest-fit near-term pilot target: agentic workflow, devtool, finance/reconciliation, or support automation pain."
        }

    if c in WAVE2_EXACT:
        return {
            "outreach_wave": "Wave 2",
            "classification_category": "Finance / reconciliation or devtools expansion",
            "manual_review": manual_review,
            "send_policy": send_policy,
            "wave_reason": "Strong buyer fit, likely operational pain, but should follow Wave 1 learning."
        }

    if c in WAVE3_EXACT:
        return {
            "outreach_wave": "Wave 3",
            "classification_category": "Support / procurement / incident-response buyer",
            "manual_review": manual_review,
            "send_policy": send_policy,
            "wave_reason": "Good vertical-pack fit with workflow handoff, false-completion, escalation, and recovery-path review."
        }

    if c in WAVE4_EXACT:
        return {
            "outreach_wave": "Wave 4",
            "classification_category": "Validator / partner / category reader",
            "manual_review": manual_review,
            "send_policy": send_policy,
            "wave_reason": "Adjacent evaluator, consultant, governance, security, or AI assurance category reader."
        }

    regulated_terms = [
        "insurance", "life", "health", "healthcare", "clinic", "medical", "pharma",
        "bank", "capital", "financial", "reinsurance", "mutual", "assurance",
        "telecom", "mobile", "energy", "grid", "electric", "semiconductor", "systems",
        "motors", "motor", "automotive", "autonomy", "robotics", "defense", "gov",
        "civic", "tyler", "transit", "rail", "shipping", "logistics", "freight",
        "construction", "industrial", "security", "cyber", "cloud infrastructure"
    ]

    wave5_exact_terms = [
        "aig", "axa", "allianz", "allstate", "state farm", "geico", "progressive",
        "chubb", "zurich", "metlife", "prudential", "massmutual", "nationwide",
        "cigna", "humana", "unitedhealth", "optum", "kaiser", "epic", "mayo",
        "jpmorgan", "goldman", "barclays", "hsbc", "ubs", "nubank", "tesla",
        "waymo", "cruise", "aurora", "rivian", "lucid", "toyota", "volvo",
        "zoox", "asml", "amd", "intel", "tsmc", "micron", "cerebras", "groq",
        "abb", "siemens", "bosch", "honeywell", "shell", "enel", "aramco",
        "verizon", "at&t", "vodafone", "ericsson", "nokia", "maersk", "fedex",
        "ups", "dhl", "xpo", "union pacific", "walmart", "target", "costco",
        "home depot", "lowe"
    ]

    if blob_contains(blob, wave5_exact_terms) or blob_contains(blob, regulated_terms):
        return {
            "outreach_wave": "Wave 5",
            "classification_category": "Regulated, critical, infrastructure, or long-cycle sector",
            "manual_review": manual_review,
            "send_policy": send_policy if manual_review == "yes" else "slow_verified_only",
            "wave_reason": "Large budget but slower procurement, higher compliance load, or sensitive operational context."
        }

    if manual_review == "yes":
        return {
            "outreach_wave": "Wave 6",
            "classification_category": "Reserve pool with manual-review flag",
            "manual_review": manual_review,
            "send_policy": send_policy,
            "wave_reason": "Sensitive or strategic company. Do not include in batch send."
        }

    return {
        "outreach_wave": "Wave 6",
        "classification_category": "Reserve pool",
        "manual_review": "no",
        "send_policy": "hold_until_better_evidence_or_specific_signal",
        "wave_reason": "Valid company target, but not the strongest first-wave fit."
    }

def main():
    contacts = read_csv(CONTACTS)
    repo_targets = read_csv(COMPANY_TARGETS)

    # Clean citation artifacts from private emails.
    changed = 0
    for r in contacts:
        old = r.get("email", "")
        new = clean_email(old)
        if new != old:
            r["email"] = new
            changed += 1

    # Persist cleaned private contacts.
    if contacts:
        fields = list(contacts[0].keys())
        with CONTACTS.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(contacts)
        CONTACTS.chmod(0o600)

    private_companies = {
        (r.get("company") or "").strip()
        for r in contacts
        if (r.get("company") or "").strip()
    }

    repo_companies = {
        (r.get("company") or "").strip()
        for r in repo_targets
        if (r.get("company") or "").strip()
    }

    all_companies = sorted(private_companies | repo_companies)

    assignments = []
    for company in all_companies:
        a = assign_company(company)
        wave = a["outreach_wave"]
        assignments.append({
            "company": company,
            "outreach_wave": wave,
            "wave_name": WAVE_NAMES[wave],
            "classification_category": a["classification_category"],
            "manual_review": a["manual_review"],
            "send_policy": a["send_policy"],
            "wave_reason": a["wave_reason"]
        })

    # Invariant: every company appears exactly once in company assignments.
    counts = Counter(a["company"] for a in assignments)
    duplicate_assignments = sorted([c for c, n in counts.items() if n != 1])
    missing_from_assignments = sorted(set(all_companies) - set(counts))

    if duplicate_assignments or missing_from_assignments:
        raise SystemExit({
            "duplicate_assignments": duplicate_assignments[:20],
            "missing_from_assignments": missing_from_assignments[:20]
        })

    with ASSIGN_OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=ASSIGN_FIELDS)
        writer.writeheader()
        writer.writerows(assignments)

    # Private wave queues.
    OUTDIR.mkdir(parents=True, exist_ok=True)
    OUTDIR.chmod(0o700)

    assignment_by_company = {a["company"]: a for a in assignments}

    wave_rows = defaultdict(list)
    invalid_contacts = 0

    for r in contacts:
        company = (r.get("company") or "").strip()
        if not company:
            continue

        a = assignment_by_company.get(company)
        if not a:
            raise SystemExit(f"Missing assignment for contact company: {company}")

        email = clean_email(r.get("email", ""))
        is_valid_email = bool(email and email.upper() != "N/A" and EMAIL_RE.match(email))
        if not is_valid_email:
            invalid_contacts += 1

        base = {
            "company": company,
            "contact_name": r.get("contact_name", ""),
            "title": r.get("title", ""),
            "email": email,
            "outreach_wave": a["outreach_wave"],
            "wave_name": a["wave_name"],
            "classification_category": a["classification_category"],
            "manual_review": a["manual_review"],
            "send_policy": a["send_policy"],
            "verification_status": "unverified",
            "outreach_allowed": "no",
            "wave_reason": a["wave_reason"],
            "source_file": r.get("source_file", ""),
            "notes": "No send. Verify contact, role, company, and email independently before outreach."
        }

        wave_rows["Wave 0"].append({
            **base,
            "outreach_wave": "Wave 0",
            "wave_name": WAVE_NAMES["Wave 0"],
            "classification_category": "Hygiene and verification",
            "send_policy": "not_a_send_wave"
        })

        wave_rows[a["outreach_wave"]].append(base)

    for wave, filename in WAVE_FILES.items():
        path = OUTDIR / filename
        rows = wave_rows.get(wave, [])
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=PRIVATE_FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        path.chmod(0o600)

    wave_counts = Counter(a["outreach_wave"] for a in assignments)
    manual_counts = Counter(a["manual_review"] for a in assignments)
    contact_wave_counts = {w: len(rows) for w, rows in sorted(wave_rows.items())}

    summary = {
        "artifact_name": "Choice C Wave Summary v0.1",
        "created_at": datetime.now().isoformat(),
        "rule": "No email sent. Wave 0 is hygiene only. Every company assigned exactly once to Wave 1-6. Private contacts stay local.",
        "private_contact_rows": len(contacts),
        "private_contact_companies": len(private_companies),
        "repo_company_targets": len(repo_companies),
        "union_company_total": len(all_companies),
        "company_assignments_total": len(assignments),
        "missing_company_assignments": len(missing_from_assignments),
        "duplicate_company_assignments": len(duplicate_assignments),
        "private_email_citation_artifacts_removed": changed,
        "private_invalid_or_missing_email_rows_after_cleanup": invalid_contacts,
        "company_wave_counts": dict(sorted(wave_counts.items())),
        "private_contact_wave_counts": contact_wave_counts,
        "manual_review_company_counts": dict(sorted(manual_counts.items())),
        "repo_assignment_csv": str(ASSIGN_OUT),
        "private_wave_dir": str(OUTDIR),
        "not_for_memory": True
    }

    SUMMARY_OUT.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
