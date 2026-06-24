#!/usr/bin/env python3
import argparse
import csv
import re
from pathlib import Path

CONTACTS = Path.home() / ".specshift" / "prospect_contacts_unverified.csv"
ISSUES = Path.home() / ".specshift" / "private_contacts_email_integrity_issues.csv"
FIXED = Path.home() / ".specshift" / "prospect_contacts_unverified.fixed_candidate.csv"

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-']+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")

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

ISSUE_FIELDS = [
    "row_number",
    "company",
    "contact_name",
    "title",
    "email",
    "issue",
    "suggested_action"
]

def valid_email(value):
    value = (value or "").strip()
    if value in {"", "N/A", "n/a", "NA", "na"}:
        return False
    return bool(EMAIL_RE.match(value))

def read_rows():
    with CONTACTS.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_rows(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in FIELDS})
    path.chmod(0o600)

def check(args):
    rows = read_rows()
    issues = []

    for idx, row in enumerate(rows, start=2):
        email = (row.get("email") or "").strip()
        title = (row.get("title") or "").strip()

        if not valid_email(email):
            issue = "invalid_or_missing_email"
            if "@" not in email and "@" in title:
                issue = "possible_column_shift_email_in_title"

            issues.append({
                "row_number": idx,
                "company": row.get("company", ""),
                "contact_name": row.get("contact_name", ""),
                "title": title,
                "email": email,
                "issue": issue,
                "suggested_action": "reimport from source with robust CSV repair or verify manually"
            })

    with ISSUES.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=ISSUE_FIELDS)
        writer.writeheader()
        writer.writerows(issues)
    ISSUES.chmod(0o600)

    print(f"Private contacts checked: {len(rows)}")
    print(f"Invalid/missing email rows: {len(issues)}")
    print(f"Issues file: {ISSUES}")

    if issues:
        print()
        print("Preview:")
        for item in issues[:25]:
            print(
                f"{item['row_number']}: {item['company']} | {item['contact_name']} | "
                f"email_field={item['email']!r} | issue={item['issue']}"
            )

def apply_safe_repair(args):
    rows = read_rows()
    fixed = []
    changed = 0

    for row in rows:
        row = dict(row)
        email = (row.get("email") or "").strip()
        title = (row.get("title") or "").strip()

        # Conservative repair only:
        # If email field is not valid but title contains a trailing valid email-like token,
        # move that token into email and remove it from title.
        if not valid_email(email):
            parts = title.split()
            if parts:
                candidate = parts[-1].strip().strip(",;")
                if valid_email(candidate):
                    row["email"] = candidate
                    row["title"] = " ".join(parts[:-1]).strip().strip(",")
                    note = row.get("notes", "")
                    row["notes"] = (note + " Email field repaired from title token.").strip()
                    changed += 1

        fixed.append(row)

    write_rows(FIXED, fixed)

    print(f"Rows read: {len(rows)}")
    print(f"Candidate repairs made: {changed}")
    print(f"Fixed candidate written: {FIXED}")
    print()
    print("This did not overwrite the original file.")
    print("Review the fixed candidate before promoting it.")

def promote(args):
    if not FIXED.exists():
        raise SystemExit(f"No fixed candidate found: {FIXED}")

    # Verify candidate has no invalid emails except explicit N/A rows.
    with FIXED.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    invalid = []
    for idx, row in enumerate(rows, start=2):
        email = (row.get("email") or "").strip()
        if not valid_email(email):
            invalid.append((idx, row.get("company", ""), row.get("contact_name", ""), email))

    if invalid and not args.allow_invalid:
        print(f"Invalid rows remain: {len(invalid)}")
        for item in invalid[:25]:
            print(f"{item[0]}: {item[1]} | {item[2]} | email={item[3]!r}")
        raise SystemExit("Stop. Use --allow-invalid only if you accept unresolved invalid rows.")

    CONTACTS.write_text(FIXED.read_text(encoding="utf-8"), encoding="utf-8")
    CONTACTS.chmod(0o600)

    print(f"Promoted fixed candidate to: {CONTACTS}")
    print(f"Rows: {len(rows)}")
    print(f"Invalid rows remaining: {len(invalid)}")

def main():
    parser = argparse.ArgumentParser(description="Private contact email integrity checker")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("check")
    p.set_defaults(func=check)

    p = sub.add_parser("repair-candidate")
    p.set_defaults(func=apply_safe_repair)

    p = sub.add_parser("promote")
    p.add_argument("--allow-invalid", action="store_true")
    p.set_defaults(func=promote)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
