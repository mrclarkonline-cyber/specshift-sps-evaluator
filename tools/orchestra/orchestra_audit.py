#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

EXPECTED_COMMANDS = [
    "orchestra_probe",
    "orchestra_conduct",
    "orchestra_signals",
    "orchestra_board",
    "radar_run",
    "radar_status",
    "radar_open",
    "orchestra_sources",
    "orchestra_fetch",
    "orchestra_global_observation",
    "fetch_et",
]

EXPECTED_PATHS = [
    "~/WORK/tools/orchestra/bin",
    "~/WORK/tools/orchestra/adapters",
    "~/WORK/tools/orchestra/lib",
    "~/WORK/tools/orchestra/config/global_observation_pipelines.json",
    "~/WORK/research/global_observation",
    "~/WORK/research/global_observation/reports",
    "~/WORK/WORKSTATION_CAPABILITY_MAP.txt",
    "~/WORK/tools/workstation/scripts/build_capability_map.py",
]

EXPECTED_PIPELINE_CATEGORIES = [
    "astronomy",
    "earth_observation",
    "aviation",
    "space",
    "geophysical",
    "human",
    "underwater_acoustic_networks",
    "planetary_probes",
    "news",
    "cybersecurity",
    "research_literature",
    "policy",
    "finance",
    "infrastructure",
]


@dataclass
class CommandStatus:
    command: str
    found: bool
    path: str | None
    smoke_test_status: str
    smoke_test_output: str


@dataclass
class PathStatus:
    label: str
    expanded_path: str
    exists: bool
    kind: str


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def expand(path: str) -> Path:
    return Path(os.path.expanduser(path))


def command_smoke_test(command: str) -> tuple[str, str]:
    # Only run safe status/help style invocations. Do not trigger fetching, crawling, or external activity.
    safe_args_by_command = {
        "orchestra_board": ["--help"],
        "orchestra_sources": ["--help"],
        "orchestra_probe": ["--help"],
        "orchestra_conduct": ["--help"],
        "orchestra_signals": ["--help"],
        "radar_status": [],
        "radar_open": ["--help"],
        "radar_run": ["--help"],
        "orchestra_fetch": ["--help"],
        "orchestra_global_observation": ["--help"],
        "fetch_et": ["--help"],
    }

    if shutil.which(command) is None:
        return "missing", ""

    args = [command] + safe_args_by_command.get(command, ["--help"])
    try:
        completed = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=8,
            check=False,
        )
        output = (completed.stdout or "").strip()
        compact = "\n".join(output.splitlines()[:8])
        if completed.returncode == 0:
            return "pass", compact
        return f"nonzero_exit_{completed.returncode}", compact
    except subprocess.TimeoutExpired:
        return "timeout", ""
    except Exception as exc:
        return "error", str(exc)


def inspect_commands() -> list[CommandStatus]:
    statuses: list[CommandStatus] = []
    for command in EXPECTED_COMMANDS:
        path = shutil.which(command)
        smoke_status, smoke_output = command_smoke_test(command)
        statuses.append(CommandStatus(
            command=command,
            found=path is not None,
            path=path,
            smoke_test_status=smoke_status,
            smoke_test_output=smoke_output,
        ))
    return statuses


def inspect_paths() -> list[PathStatus]:
    statuses: list[PathStatus] = []
    for label in EXPECTED_PATHS:
        path = expand(label)
        if path.is_dir():
            kind = "directory"
        elif path.is_file():
            kind = "file"
        else:
            kind = "missing"
        statuses.append(PathStatus(
            label=label,
            expanded_path=str(path),
            exists=path.exists(),
            kind=kind,
        ))
    return statuses


def inspect_registry() -> dict:
    registry_path = expand("~/WORK/tools/orchestra/config/global_observation_pipelines.json")
    result = {
        "path": str(registry_path),
        "exists": registry_path.exists(),
        "valid_json": False,
        "top_level_type": None,
        "category_hits": {},
        "notes": [],
    }

    if not registry_path.exists():
        result["notes"].append("Registry file missing at expected path.")
        return result

    try:
        payload = json.loads(registry_path.read_text(encoding="utf-8"))
        result["valid_json"] = True
        result["top_level_type"] = type(payload).__name__
        text = json.dumps(payload).lower()
        for category in EXPECTED_PIPELINE_CATEGORIES:
            result["category_hits"][category] = category.lower() in text
    except Exception as exc:
        result["notes"].append(f"Failed to parse JSON: {exc}")

    return result


def write_markdown_report(output_path: Path, command_statuses: list[CommandStatus], path_statuses: list[PathStatus], registry: dict) -> None:
    found_count = sum(1 for item in command_statuses if item.found)
    path_count = sum(1 for item in path_statuses if item.exists)
    smoke_pass_count = sum(1 for item in command_statuses if item.smoke_test_status == "pass")

    lines: list[str] = []
    lines.append("# Orchestra Implementation Audit")
    lines.append("")
    lines.append(f"Generated at UTC: {utc_now()}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Expected commands found: {found_count}/{len(command_statuses)}")
    lines.append(f"- Safe smoke tests passed: {smoke_pass_count}/{len(command_statuses)}")
    lines.append(f"- Expected paths found: {path_count}/{len(path_statuses)}")
    lines.append(f"- Registry exists: {registry.get('exists')}")
    lines.append(f"- Registry valid JSON: {registry.get('valid_json')}")
    lines.append("")
    lines.append("## Safety Boundary")
    lines.append("")
    lines.append("This audit performs local discovery and safe help/status checks only. It does not fetch external data, crawl sources, run radar collection, probe third-party systems, or trigger automated actions.")
    lines.append("")
    lines.append("## Command Status")
    lines.append("")
    for item in command_statuses:
        mark = "PASS" if item.found else "MISSING"
        lines.append(f"### {item.command}")
        lines.append("")
        lines.append(f"- Status: {mark}")
        lines.append(f"- Path: {item.path or 'not found'}")
        lines.append(f"- Safe smoke test: {item.smoke_test_status}")
        if item.smoke_test_output:
            lines.append("- Smoke output excerpt:")
            lines.append("")
            lines.append("```text")
            lines.append(item.smoke_test_output[:1200])
            lines.append("```")
        lines.append("")

    lines.append("## Expected Path Status")
    lines.append("")
    for item in path_statuses:
        mark = "PASS" if item.exists else "MISSING"
        lines.append(f"- [{mark}] {item.label}")
        lines.append(f"  - expanded: {item.expanded_path}")
        lines.append(f"  - kind: {item.kind}")
    lines.append("")

    lines.append("## Registry Category Coverage")
    lines.append("")
    hits = registry.get("category_hits", {})
    if not hits:
        lines.append("No registry category coverage detected.")
    else:
        for category, present in hits.items():
            mark = "PRESENT" if present else "MISSING"
            lines.append(f"- [{mark}] {category}")
    lines.append("")

    lines.append("## Implementation Gate")
    lines.append("")
    if found_count == len(command_statuses) and registry.get("exists") and registry.get("valid_json"):
        lines.append("Status: ORCHESTRA_BASELINE_PRESENT")
        lines.append("")
        lines.append("Orchestra appears locally discoverable at the command and registry level.")
    else:
        lines.append("Status: ORCHESTRA_INCOMPLETE_OR_PARTIAL")
        lines.append("")
        lines.append("One or more expected commands, paths, or registry checks are missing. Fix these before treating Orchestra as fully implemented.")
    lines.append("")

    lines.append("## Next Human-Review Actions")
    lines.append("")
    lines.append("1. Confirm missing command wrappers are intentionally absent or create them under the Orchestra bin path.")
    lines.append("2. Confirm global_observation_pipelines.json contains the desired fast-relevance categories.")
    lines.append("3. Confirm fetch commands support dry-run/status mode before live data acquisition.")
    lines.append("4. Confirm outputs land under ~/WORK/research/global_observation/reports or a documented repo path.")
    lines.append("5. Confirm no command performs active probing, targeting, credential use, or external automation without explicit human action.")
    lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    command_statuses = inspect_commands()
    path_statuses = inspect_paths()
    registry = inspect_registry()

    report_path = Path("docs/workstation/orchestra_implementation_audit_latest.md")
    json_path = Path("docs/workstation/orchestra_implementation_audit_latest.json")

    write_markdown_report(report_path, command_statuses, path_statuses, registry)

    payload = {
        "generated_at_utc": utc_now(),
        "commands": [asdict(item) for item in command_statuses],
        "paths": [asdict(item) for item in path_statuses],
        "registry": registry,
    }
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    found_count = sum(1 for item in command_statuses if item.found)
    smoke_pass_count = sum(1 for item in command_statuses if item.smoke_test_status == "pass")
    path_count = sum(1 for item in path_statuses if item.exists)

    print("=== Orchestra Audit ===")
    print(f"commands_found: {found_count}/{len(command_statuses)}")
    print(f"safe_smoke_passed: {smoke_pass_count}/{len(command_statuses)}")
    print(f"paths_found: {path_count}/{len(path_statuses)}")
    print(f"registry_exists: {registry.get('exists')}")
    print(f"registry_valid_json: {registry.get('valid_json')}")
    print(f"markdown_report: {report_path}")
    print(f"json_report: {json_path}")

    if found_count == len(command_statuses) and registry.get("exists") and registry.get("valid_json"):
        print("PASS Orchestra baseline present")
        return 0

    print("WARN Orchestra appears partial; report written for remediation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
