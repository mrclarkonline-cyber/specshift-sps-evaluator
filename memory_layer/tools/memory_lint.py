from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"

REQUIRED_FIELDS = [
    "Status:",
    "Source(s):",
    "Last updated:",
    "Public-safe:",
    "Private-safe:",
    "Counsel-only:",
    "Core-protected:",
    "Confidence:",
    "Contradictions:",
    "Promotion status:",
]

PROTECTED_PATTERNS = [
    r"proprietary scoring",
    r"internal diagnostic ordering",
    r"implementation mechanics",
    r"core method",
    r"training rights",
    r"code transfer",
]

def main() -> int:
    issues = []

    for path in sorted(WIKI.rglob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(ROOT)

        for field in REQUIRED_FIELDS:
            if field not in text:
                issues.append(f"MISSING_FIELD\t{rel}\t{field}")

        links = re.findall(r"\[\[([^\]]+)\]\]", text)
        for link in links:
            target = WIKI / (link.strip() + ".md")
            if not target.exists():
                issues.append(f"BROKEN_WIKILINK\t{rel}\t[[{link}]]")

        if "Public-safe: Yes" in text:
            for pattern in PROTECTED_PATTERNS:
                if re.search(pattern, text, flags=re.IGNORECASE):
                    issues.append(f"PUBLIC_SAFE_REVIEW\t{rel}\tpattern={pattern}")

    if issues:
        print("MEMORY LINT: ISSUES FOUND")
        for issue in issues:
            print(issue)
        return 1

    print("MEMORY LINT: PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
