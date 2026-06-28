#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

REQUIRED_STRINGS = [
    "Source",
    "Retrieved at UTC",
]

RISKY_PHRASES = [
    "proves",
    "confirmed proof",
    "definitively shows",
    "guarantees",
    "validated conclusion",
    "investment advice",
    "legal advice",
    "medical advice",
    "exploit code",
    "attack chain",
]


def check_file(path: Path) -> list[str]:
    issues: list[str] = []

    if not path.exists():
        return [f"missing file: {path}"]

    text = path.read_text(encoding="utf-8", errors="replace")
    lowered = text.lower()

    for required in REQUIRED_STRINGS:
        if required.lower() not in lowered:
            issues.append(f"{path}: missing required provenance marker '{required}'")

    if "uncertainty label" not in lowered:
        issues.append(f"{path}: missing uncertainty label")

    if "claim safety" not in lowered:
        issues.append(f"{path}: missing claim safety note")

    for phrase in RISKY_PHRASES:
        if phrase in lowered:
            issues.append(f"{path}: risky phrase found '{phrase}'")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Run lightweight claim-safety checks on generated digest files.")
    parser.add_argument("--path", default="reports/fast_relevance", help="File or directory to scan.")
    parser.add_argument("--dry-run", action="store_true", help="Validate configuration only.")
    args = parser.parse_args()

    print("=== Claim Safety Gate ===")
    print(f"path: {args.path}")
    print("mode: dry-run" if args.dry_run else "mode: scan")
    print("safety: flags provenance/uncertainty gaps and risky overclaiming phrases")

    if args.dry_run:
        print("PASS dry-run configuration")
        print("No files scanned.")
        print("No files mutated.")
        return 0

    root = Path(args.path)
    if not root.exists():
        print(f"PASS no report path yet: {root}")
        print("No generated reports to scan.")
        return 0

    files: list[Path]
    if root.is_file():
        files = [root]
    else:
        files = sorted(p for p in root.rglob("*.md") if p.is_file())

    issues: list[str] = []
    for file in files:
        issues.extend(check_file(file))

    if issues:
        print("FAIL claim safety issues found")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print(f"PASS scanned markdown files: {len(files)}")
    print("No claim safety issues found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
