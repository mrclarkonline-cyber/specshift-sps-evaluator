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
WAVES = PRIVATE / "private_wave_queues_v0_1"

CONTACTS = PRIVATE / "prospect_contacts_unverified.csv"
ASSIGN = PIPE / "choice_c_company_wave_assignments_v0_1.csv"

PRIVATE_WAVE1 = WAVES / "private_wave1_precision_pilot_seekers.csv"
PRIVATE_VERIFY = PRIVATE / "private_wave1_verification_queue_v0_1.csv"

REPO_COMPANY_QUALITY = PIPE / "choice_c_wave1_company_quality_v0_1.csv"
SUMMARY = PIPE / "choice_c_wave_quality_summary_v0_1.json"

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-']+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")

VERIFY_FIELDS = [
    "priority_rank",
    "company",
    "contact_name",
    "title",
    "email",
    "fit_score",
    "fit_tier",
    "quality_flags",
    "manual_review",
    "verification_status",
    "outreach_allowed",
    "recommended_action",
    "notes"
]

REPO_FIELDS = [
    "priority_rank",
    "company",
    "fit_score",
    "fit_tier",
    "quality_flags",
    "manual_review",
    "recommended_action"
]

HIGH_SIGNAL = {
    "Cognition AI": 100,
    "Anysphere": 99,
    "Cursor": 99,
    "Modern Treasury": 98,
    "Stripe": 98,
    "Ramp": 97,
    "BlackLine": 96,
    "Workiva": 95,
    "LangChain": 94,
    "LangSmith": 94,
    "LlamaIndex": 94,
    "Glean": 93,
    "Sierra": 92,
    "Decagon": 91,
    "Cresta": 90,
    "Harvey": 89,
    "Google / Alphabet": 88,
    "Intuit / QuickBooks": 88,
    "Oracle NetSuite": 87,
    "Target": 86,
    "Walmart": 86,
    "Zilliz / Milvus": 85,
    "LangChain / LangSmith": 84,
    "Alibaba": 80,
    "Huawei": 75,
}

SENSITIVE = {
    "OpenAI", "Anthropic", "Google / Alphabet", "Google DeepMind", "Google Cloud",
    "Microsoft", "Microsoft Azure", "Amazon", "Amazon Web Services",
    "Alibaba", "Huawei", "DeepSeek", "Qwen", "xAI", "Palantir", "Anduril",
    "Shield AI", "Helsing", "Leidos", "SAIC", "Booz Allen Hamilton"
}

def read_csv(path):
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(path, fields, rows, private=False):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    if private:
        path.chmod(0o600)

def valid_email(email):
    email = (email or "").strip()
    return bool(email and email.upper() != "N/A" and EMAIL_RE.match(email))

def score_row(row):
    company = (row.get("company") or "").strip()
    title = (row.get("title") or "").lower()
    email = (row.get("email") or "").strip()
    source_file = row.get("source_file", "")

    score = HIGH_SIGNAL.get(company, 60)
    flags = []

    if source_file == "repo_company_target_only":
        score -= 18
        flags.append("needs_contact")

    if not valid_email(email):
        score -= 15
        flags.append("missing_or_invalid_email")

    if company in SENSITIVE or row.get("manual_review") == "yes":
        score -= 8
        flags.append("manual_review")

    if any(x in title for x in ["vp", "chief", "cto", "founder", "head", "director", "gm"]):
        score += 5
    elif title.strip():
        score += 1
    else:
        score -= 5
        flags.append("missing_title")

    if any(x in title for x in ["reliability", "integrity", "risk", "trust", "governance", "safety", "assurance", "platform", "operations"]):
        score += 6

    if any(x in title for x in ["sales", "marketing", "communications", "public relations"]):
        score -= 8
        flags.append("possibly_wrong_function")

    score = max(0, min(100, score))

    if score >= 90:
        tier = "A"
    elif score >= 80:
        tier = "B"
    elif score >= 65:
        tier = "C"
    else:
        tier = "Hold"

    return score, tier, sorted(set(flags))

def main():
    wave1 = read_csv(PRIVATE_WAVE1)
    assignments = read_csv(ASSIGN)

    expected_wave1_companies = {
        (r.get("company") or "").strip()
        for r in assignments
        if (r.get("outreach_wave") or "").strip() == "Wave 1"
    }

    wave1_companies = {
        (r.get("company") or "").strip()
        for r in wave1
        if (r.get("company") or "").strip()
    }

    missing_from_private_wave1 = sorted(expected_wave1_companies - wave1_companies)

    company_best = {}
    for row in wave1:
        company = (row.get("company") or "").strip()
        if not company:
            continue

        score, tier, flags = score_row(row)
        enriched = {
            **row,
            "fit_score": score,
            "fit_tier": tier,
            "quality_flags": ";".join(flags) if flags else "none"
        }

        if company not in company_best or score > company_best[company]["fit_score"]:
            company_best[company] = enriched

    ranked = sorted(
        company_best.values(),
        key=lambda r: (-int(r["fit_score"]), r.get("company", ""))
    )

    private_rows = []
    repo_rows = []

    for idx, r in enumerate(ranked, start=1):
        flags = r.get("quality_flags", "")
        has_contact = bool((r.get("contact_name") or "").strip())
        has_email = valid_email(r.get("email"))
        manual = r.get("manual_review", "no")

        if "needs_contact" in flags:
            action = "find_verified_business_contact"
        elif not has_email:
            action = "verify_or_replace_email"
        elif manual == "yes":
            action = "manual_individual_review_before_draft"
        else:
            action = "verify_role_and_company_before_draft"

        private_rows.append({
            "priority_rank": idx,
            "company": r.get("company", ""),
            "contact_name": r.get("contact_name", ""),
            "title": r.get("title", ""),
            "email": r.get("email", ""),
            "fit_score": r.get("fit_score", ""),
            "fit_tier": r.get("fit_tier", ""),
            "quality_flags": flags,
            "manual_review": manual,
            "verification_status": "unverified",
            "outreach_allowed": "no",
            "recommended_action": action,
            "notes": "No send. Verify independently before draft."
        })

        repo_rows.append({
            "priority_rank": idx,
            "company": r.get("company", ""),
            "fit_score": r.get("fit_score", ""),
            "fit_tier": r.get("fit_tier", ""),
            "quality_flags": flags,
            "manual_review": manual,
            "recommended_action": action
        })

    write_csv(PRIVATE_VERIFY, VERIFY_FIELDS, private_rows, private=True)
    write_csv(REPO_COMPANY_QUALITY, REPO_FIELDS, repo_rows)

    counts = Counter(r["fit_tier"] for r in private_rows)
    actions = Counter(r["recommended_action"] for r in private_rows)
    flags = Counter()
    for r in private_rows:
        for f in (r["quality_flags"] or "").split(";"):
            if f:
                flags[f] += 1

    summary = {
        "artifact_name": "Choice C Wave Quality Summary v0.1",
        "created_at": datetime.now().isoformat(),
        "rule": "Quality pass only. No email sent. Private verification queue remains local.",
        "wave1_expected_companies": len(expected_wave1_companies),
        "wave1_private_companies": len(wave1_companies),
        "wave1_ranked_companies": len(private_rows),
        "missing_from_private_wave1": missing_from_private_wave1,
        "fit_tier_counts": dict(counts),
        "recommended_action_counts": dict(actions),
        "quality_flag_counts": dict(flags),
        "private_verification_queue": str(PRIVATE_VERIFY),
        "repo_company_quality_file": str(REPO_COMPANY_QUALITY)
    }

    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))

    if missing_from_private_wave1:
        raise SystemExit("FAIL: Wave 1 still missing private rows/placeholders.")

if __name__ == "__main__":
    main()
