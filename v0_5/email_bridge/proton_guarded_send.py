#!/usr/bin/env python3
import argparse
import json
import mimetypes
import smtplib
import subprocess
import ssl
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

CONFIG = Path.home() / ".specshift" / "proton_bridge_config.json"
LOG_DIR = Path.home() / ".specshift" / "email_logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
SEND_LOG = LOG_DIR / "guarded_send_log.jsonl"

SERVICE = "specshift_proton_smtp_token"
ACCOUNT = "ben@specshiftlabs.com"
EXPECTED_FROM = "ben@specshiftlabs.com"

def get_token():
    return subprocess.check_output(
        [
            "security",
            "find-generic-password",
            "-a", ACCOUNT,
            "-s", SERVICE,
            "-w"
        ],
        text=True
    ).strip()

def load_config():
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    if cfg.get("from_email") != EXPECTED_FROM:
        raise SystemExit("Config from_email does not match ben@specshiftlabs.com.")
    return cfg

def add_attachment(msg, path):
    p = Path(path).expanduser()
    if not p.exists() or not p.is_file():
        raise SystemExit(f"Attachment not found: {p}")

    ctype, encoding = mimetypes.guess_type(str(p))
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)
    data = p.read_bytes()
    msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=p.name)

def build_message(from_email, to_email, subject, body, attachments):
    msg = EmailMessage()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    for attachment in attachments:
        add_attachment(msg, attachment)

    return msg

def preview(from_email, to_email, subject, body, attachments, smtp_host, smtp_port):
    print()
    print("=" * 72)
    print("SpecShift Guarded Proton SMTP Send Preview")
    print("=" * 72)
    print(f"From: {from_email}")
    print(f"To: {to_email}")
    print(f"SMTP: {smtp_host}:{smtp_port}")
    print(f"Subject: {subject}")
    print()
    print("Body:")
    print(body)
    print()
    print("Attachments:")
    if attachments:
        for a in attachments:
            print(f"- {Path(a).expanduser()}")
    else:
        print("- none")
    print("=" * 72)
    print()

def write_log(to_email, subject, attachments):
    record = {
        "created_at": datetime.now().isoformat(),
        "from": EXPECTED_FROM,
        "to": to_email,
        "subject": subject,
        "attachments": [str(Path(a).expanduser()) for a in attachments],
        "send_method": "Proton SMTP submission via guarded terminal sender",
        "confirmation_required": f"SEND {to_email}",
        "body_logged": False
    }
    with SEND_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def main():
    parser = argparse.ArgumentParser(
        description="Guarded one-email Proton SMTP sender for SpecShift. Requires exact typed confirmation."
    )
    parser.add_argument("--to", required=True, help="Recipient email address")
    parser.add_argument("--subject", required=True, help="Email subject")
    parser.add_argument("--body", help="Email body text")
    parser.add_argument("--body-file", help="Path to text file containing email body")
    parser.add_argument("--attach", action="append", default=[], help="Attachment path. May be repeated.")
    parser.add_argument("--dry-run", action="store_true", help="Preview only. Do not send.")
    args = parser.parse_args()

    if not args.body and not args.body_file:
        raise SystemExit("Provide --body or --body-file.")

    if args.body_file:
        body = Path(args.body_file).expanduser().read_text(encoding="utf-8")
    else:
        body = args.body

    cfg = load_config()
    smtp_host = cfg["smtp_host"]
    smtp_port = int(cfg["smtp_port"])
    smtp_user = cfg["smtp_username"]
    from_email = cfg["from_email"]

    preview(from_email, args.to, args.subject, body, args.attach, smtp_host, smtp_port)

    if args.dry_run:
        print("DRY RUN: no email sent.")
        return

    required = f"SEND {args.to}"
    confirm = input(f"Type exactly {required} to send this email: ").strip()
    if confirm != required:
        raise SystemExit("Cancelled. No email sent.")

    token = get_token()
    msg = build_message(from_email, args.to, args.subject, body, args.attachments if hasattr(args, "attachments") else args.attach)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(smtp_user, token)
        server.send_message(msg)

    write_log(args.to, args.subject, args.attach)
    print("SEND RESULT: PASS")
    print("Email sent.")
    print(f"Local send log: {SEND_LOG}")

if __name__ == "__main__":
    main()
