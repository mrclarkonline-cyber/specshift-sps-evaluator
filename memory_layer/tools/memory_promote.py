from pathlib import Path
import datetime
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "inbox"
PROMOTIONS = ROOT / "promotions"

def slugify(name: str) -> str:
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "-", name).strip("-")
    return name or "promotion"

def main() -> int:
    if len(sys.argv) < 4:
        print("Usage: python3 memory_layer/tools/memory_promote.py <inbox-file> <promoted-page> <reason>")
        return 2

    inbox_file = Path(sys.argv[1]).expanduser()
    promoted_page = sys.argv[2]
    reason = sys.argv[3]

    if not inbox_file.exists():
        print(f"Inbox/source file not found: {inbox_file}")
        return 1

    today = datetime.date.today().isoformat()
    slug = slugify(Path(promoted_page).stem)
    record = PROMOTIONS / f"{today}-{slug}.md"

    record.write_text(
        "# Promotion Record\n\n"
        f"Date: {today}\n"
        "Reviewer: Ben / SpecShift operator\n"
        f"Source item: {inbox_file}\n"
        f"Promoted page: {promoted_page}\n"
        "Lifecycle stage: Synthesized\n"
        "Public-safe: Pending review\n"
        "Private-safe: Yes\n"
        "Counsel-only: No\n"
        "Core-protected risk: Review required\n"
        f"Reason for promotion: {reason}\n"
        "Evidence summary: Pending operator synthesis\n"
        "Contradictions or caveats: Pending review\n"
        "Replacement / supersedes: None stated\n"
        "Next action: Review promoted wiki page and update status fields\n",
        encoding="utf-8",
    )

    print(f"Promotion record created: {record}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
