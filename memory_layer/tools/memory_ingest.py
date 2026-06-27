from pathlib import Path
import datetime
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "inbox"

def slugify(name: str) -> str:
    stem = Path(name).stem.lower()
    stem = re.sub(r"[^a-z0-9]+", "-", stem).strip("-")
    return stem or "untitled"

def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python3 memory_layer/tools/memory_ingest.py <source-file> [title]")
        return 2

    source = Path(sys.argv[1]).expanduser()
    if not source.exists():
        print(f"Source not found: {source}")
        return 1

    title = sys.argv[2] if len(sys.argv) > 2 else source.stem
    slug = slugify(title)
    today = datetime.date.today().isoformat()
    dest = INBOX / f"{today}-{slug}.md"

    raw_text = source.read_text(encoding="utf-8", errors="replace")

    dest.write_text(
        f"# {title}\n\n"
        f"Date captured: {today}\n"
        f"Source file: {source}\n"
        f"Lifecycle stage: Inbox\n"
        f"Public-safe: Unreviewed\n"
        f"Core-protected risk: Unreviewed\n\n"
        f"## Raw Content\n\n"
        f"{raw_text}\n",
        encoding="utf-8",
    )

    print(f"Ingested to {dest}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
