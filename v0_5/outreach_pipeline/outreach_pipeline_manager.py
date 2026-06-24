#!/usr/bin/env python3
import argparse
import csv
from datetime import date
from pathlib import Path

BASE = Path.home() / "specshift_terminal_intelligence"
OUTREACH = BASE / "v0_5" / "outreach_pipeline"
TARGETS = OUTREACH / "outreach_targets_v0_1.csv"
TOUCHES = OUTREACH / "outreach_touch_log_v0_1.csv"

TARGET_FIELDS = [
    "target_id",
    "company",
    "target_person",
    "role",
    "email",
    "source",
    "buyer_category",
    "likely_workflow",
    "matched_pack_or_skin",
    "priority",
    "status",
    "last_touch_date",
    "next_action",
    "notes"
]

TOUCH_FIELDS = [
    "touch_id",
    "date",
    "target_id",
    "company",
    "contact_email",
    "touch_type",
    "subject",
    "artifact_sent",
    "response_status",
    "next_action",
    "notes"
]

def read_rows(path):
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_rows(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

def next_id(rows, prefix, field):
    nums = []
    for row in rows:
        value = row.get(field, "")
        if value.startswith(prefix):
            try:
                nums.append(int(value[len(prefix):]))
            except ValueError:
                pass
    return f"{prefix}{max(nums + [0]) + 1:03d}"

def add_target(args):
    rows = read_rows(TARGETS)
    target_id = args.target_id or next_id(rows, "T", "target_id")

    row = {
        "target_id": target_id,
        "company": args.company or "",
        "target_person": args.person or "",
        "role": args.role or "",
        "email": args.email or "",
        "source": args.source or "",
        "buyer_category": args.buyer_category or "",
        "likely_workflow": args.workflow or "",
        "matched_pack_or_skin": args.pack or "",
        "priority": args.priority or "medium",
        "status": args.status or "not_contacted",
        "last_touch_date": "",
        "next_action": args.next_action or "send bounded outreach or identify one concrete workflow",
        "notes": args.notes or ""
    }

    rows.append(row)
    write_rows(TARGETS, TARGET_FIELDS, rows)
    print(f"Added target: {target_id} {row['company']} {row['email']}")

def log_touch(args):
    targets = read_rows(TARGETS)
    touches = read_rows(TOUCHES)
    touch_id = args.touch_id or next_id(touches, "C", "touch_id")

    company = args.company or ""
    email = args.email or ""

    for row in targets:
        if row.get("target_id") == args.target_id:
            company = company or row.get("company", "")
            email = email or row.get("email", "")
            row["last_touch_date"] = args.date or date.today().isoformat()
            row["status"] = args.response_status or row.get("status", "")
            row["next_action"] = args.next_action or row.get("next_action", "")
            break

    touch = {
        "touch_id": touch_id,
        "date": args.date or date.today().isoformat(),
        "target_id": args.target_id or "",
        "company": company,
        "contact_email": email,
        "touch_type": args.touch_type or "initial_email",
        "subject": args.subject or "",
        "artifact_sent": args.artifact_sent or "focused diagnostic pilot one-pager",
        "response_status": args.response_status or "contacted",
        "next_action": args.next_action or "",
        "notes": args.notes or ""
    }

    touches.append(touch)
    write_rows(TOUCHES, TOUCH_FIELDS, touches)
    write_rows(TARGETS, TARGET_FIELDS, targets)
    print(f"Logged touch: {touch_id} target={args.target_id}")

def list_targets(args):
    rows = read_rows(TARGETS)
    if not rows:
        print("No targets found.")
        return

    print("Targets:")
    for row in rows:
        print(
            f"{row.get('target_id')} | {row.get('priority')} | {row.get('status')} | "
            f"{row.get('company')} | {row.get('target_person')} | {row.get('email')} | "
            f"{row.get('matched_pack_or_skin')} | next: {row.get('next_action')}"
        )

def list_touches(args):
    rows = read_rows(TOUCHES)
    if not rows:
        print("No touch log rows found.")
        return

    print("Touches:")
    for row in rows:
        print(
            f"{row.get('touch_id')} | {row.get('date')} | {row.get('target_id')} | "
            f"{row.get('company')} | {row.get('touch_type')} | {row.get('response_status')} | "
            f"next: {row.get('next_action')}"
        )

def dashboard(args):
    targets = read_rows(TARGETS)
    touches = read_rows(TOUCHES)

    by_status = {}
    by_priority = {}
    for row in targets:
        by_status[row.get("status", "")] = by_status.get(row.get("status", ""), 0) + 1
        by_priority[row.get("priority", "")] = by_priority.get(row.get("priority", ""), 0) + 1

    print("SpecShift Outreach Pipeline Dashboard")
    print(f"Targets: {len(targets)}")
    print(f"Touches: {len(touches)}")
    print("Status counts:")
    for key, value in sorted(by_status.items()):
        print(f"- {key or 'blank'}: {value}")
    print("Priority counts:")
    for key, value in sorted(by_priority.items()):
        print(f"- {key or 'blank'}: {value}")
    print()
    print("Rule: focused outreach only, no bulk sending, one buyer/workflow at a time.")

def main():
    parser = argparse.ArgumentParser(description="SpecShift focused outreach pipeline manager")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("add-target")
    p.add_argument("--target-id")
    p.add_argument("--company", required=True)
    p.add_argument("--person", default="")
    p.add_argument("--role", default="")
    p.add_argument("--email", default="")
    p.add_argument("--source", default="")
    p.add_argument("--buyer-category", default="")
    p.add_argument("--workflow", default="")
    p.add_argument("--pack", default="")
    p.add_argument("--priority", default="medium")
    p.add_argument("--status", default="not_contacted")
    p.add_argument("--next-action", default="")
    p.add_argument("--notes", default="")
    p.set_defaults(func=add_target)

    p = sub.add_parser("log-touch")
    p.add_argument("--touch-id")
    p.add_argument("--target-id", required=True)
    p.add_argument("--date", default="")
    p.add_argument("--company", default="")
    p.add_argument("--email", default="")
    p.add_argument("--touch-type", default="initial_email")
    p.add_argument("--subject", default="")
    p.add_argument("--artifact-sent", default="focused diagnostic pilot one-pager")
    p.add_argument("--response-status", default="contacted")
    p.add_argument("--next-action", default="")
    p.add_argument("--notes", default="")
    p.set_defaults(func=log_touch)

    p = sub.add_parser("list-targets")
    p.set_defaults(func=list_targets)

    p = sub.add_parser("list-touches")
    p.set_defaults(func=list_touches)

    p = sub.add_parser("dashboard")
    p.set_defaults(func=dashboard)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
