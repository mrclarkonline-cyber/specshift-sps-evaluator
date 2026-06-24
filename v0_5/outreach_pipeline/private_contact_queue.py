#!/usr/bin/env python3
import argparse
import csv
from collections import Counter
from pathlib import Path

PRIVATE_CONTACTS = Path.home() / ".specshift" / "prospect_contacts_unverified.csv"

FIELDS = [
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

def read_rows():
    if not PRIVATE_CONTACTS.exists():
        return []
    with PRIVATE_CONTACTS.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_rows(rows):
    PRIVATE_CONTACTS.parent.mkdir(parents=True, exist_ok=True)
    with PRIVATE_CONTACTS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in FIELDS})
    PRIVATE_CONTACTS.chmod(0o600)

def dashboard(args):
    rows = read_rows()
    print("SpecShift Private Contact Queue")
    print(f"Private file: {PRIVATE_CONTACTS}")
    print(f"Total contacts: {len(rows)}")
    print()

    if not rows:
        print("No private contacts found.")
        return

    print("Verification status:")
    for key, value in sorted(Counter(r.get("verification_status", "blank") for r in rows).items()):
        print(f"- {key or 'blank'}: {value}")

    print()
    print("Outreach allowed:")
    for key, value in sorted(Counter(r.get("outreach_allowed", "blank") for r in rows).items()):
        print(f"- {key or 'blank'}: {value}")

    print()
    print("Source files:")
    for key, value in sorted(Counter(r.get("source_file", "blank") for r in rows).items()):
        print(f"- {key or 'blank'}: {value}")

    print()
    print("Rule: do not send outreach unless verification_status=verified and outreach_allowed=yes.")

def list_companies(args):
    rows = read_rows()
    companies = sorted({r.get("company", "").strip() for r in rows if r.get("company", "").strip()})
    for company in companies:
        print(company)

def search(args):
    q = args.query.lower().strip()
    rows = read_rows()
    matches = []
    for i, row in enumerate(rows, start=1):
        blob = " ".join([
            row.get("company", ""),
            row.get("contact_name", ""),
            row.get("title", ""),
            row.get("email", ""),
            row.get("verification_status", ""),
            row.get("outreach_allowed", "")
        ]).lower()
        if q in blob:
            matches.append((i, row))

    print(f"Matches: {len(matches)}")
    for i, row in matches[:args.limit]:
        email = row.get("email", "")
        masked = email
        if "@" in email:
            local, domain = email.split("@", 1)
            masked = (local[:2] + "***@" + domain) if local else "***@" + domain
        print(
            f"{i}: {row.get('company')} | {row.get('contact_name')} | "
            f"{row.get('title')} | {masked} | "
            f"{row.get('verification_status')} | outreach={row.get('outreach_allowed')}"
        )

def mark_verified(args):
    rows = read_rows()
    company_q = args.company.lower().strip()
    email_q = args.email.lower().strip()

    changed = 0
    for row in rows:
        if row.get("company", "").lower().strip() == company_q and row.get("email", "").lower().strip() == email_q:
            row["verification_status"] = "verified"
            row["outreach_allowed"] = "yes" if args.allow_outreach else "no"
            note = row.get("notes", "")
            add = "Verified manually."
            row["notes"] = (note + " " + add).strip()
            changed += 1

    if changed == 0:
        raise SystemExit("No matching contact found.")

    write_rows(rows)
    print(f"Updated contacts: {changed}")

def main():
    parser = argparse.ArgumentParser(description="SpecShift private contact queue manager")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("dashboard")
    p.set_defaults(func=dashboard)

    p = sub.add_parser("list-companies")
    p.set_defaults(func=list_companies)

    p = sub.add_parser("search")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=25)
    p.set_defaults(func=search)

    p = sub.add_parser("mark-verified")
    p.add_argument("--company", required=True)
    p.add_argument("--email", required=True)
    p.add_argument("--allow-outreach", action="store_true")
    p.set_defaults(func=mark_verified)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
