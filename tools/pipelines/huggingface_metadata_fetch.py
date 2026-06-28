#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HF_MODELS_URL = "https://huggingface.co/api/models"
REPORT_ROOT = Path("reports/fast_relevance")


@dataclass
class FetchResult:
    retrieved_at_utc: str
    source_url: str
    raw_sha256: str
    raw_path: Path
    summary_path: Path
    record_count: int


def utc_now_slug() -> tuple[str, str]:
    now = datetime.now(timezone.utc)
    return now.isoformat().replace("+00:00", "Z"), now.strftime("%Y%m%dT%H%M%SZ")


def build_url(limit: int, sort: str, direction: str, search: str | None) -> str:
    params = {"limit": str(limit), "sort": sort, "direction": direction}
    if search:
        params["search"] = search
    return HF_MODELS_URL + "?" + urllib.parse.urlencode(params)


def fetch_bytes(url: str, timeout: int = 30) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "SpecShiftLabsResearchWorkstation/0.1 ben@specshiftlabs.com",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_str(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value).strip()


def model_records(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, list):
        raise ValueError("Hugging Face model payload is not a list")
    return [r for r in payload if isinstance(r, dict)]


def build_summary(records: list[dict[str, Any]], raw_sha256: str, source_url: str, retrieved_at_utc: str, raw_path: Path, limit: int) -> str:
    lines: list[str] = []
    lines.append("# Hugging Face Model Metadata Digest")
    lines.append("")
    lines.append(f"Retrieved at UTC: {retrieved_at_utc}")
    lines.append(f"Source query: {source_url}")
    lines.append(f"Raw payload SHA256: {raw_sha256}")
    lines.append(f"Raw payload path: {raw_path}")
    lines.append(f"Record count: {len(records)}")
    lines.append("")
    lines.append("## Safety Boundary")
    lines.append("")
    lines.append("This digest is public model metadata awareness only.")
    lines.append("")
    lines.append("Do not download, execute, load, or trust remote model artifacts from this pipeline. Model cards, tags, downloads, and benchmark claims are self-reported or platform metadata unless independently verified.")
    lines.append("")
    lines.append("## Latest / Selected Hugging Face Model Records")
    lines.append("")

    for idx, model in enumerate(records[:limit], start=1):
        model_id = safe_str(model.get("modelId"), "unknown")
        author = safe_str(model.get("author"), "unknown")
        downloads = safe_str(model.get("downloads"), "unknown")
        likes = safe_str(model.get("likes"), "unknown")
        last_modified = safe_str(model.get("lastModified"), "unknown")
        pipeline_tag = safe_str(model.get("pipeline_tag"), "unknown")
        tags = model.get("tags", [])
        tags_label = ", ".join(str(t) for t in tags[:20]) if isinstance(tags, list) else "unknown"

        lines.append(f"### {idx}. {model_id}")
        lines.append("")
        lines.append(f"- Author: {author}")
        lines.append(f"- Last modified: {last_modified}")
        lines.append(f"- Downloads: {downloads}")
        lines.append(f"- Likes: {likes}")
        lines.append(f"- Pipeline tag: {pipeline_tag}")
        lines.append(f"- Tags: {tags_label}")
        lines.append(f"- Model page: https://huggingface.co/{model_id}")
        lines.append("- Uncertainty label: self_reported_platform_metadata")
        lines.append("- Source tier: tier_3_self_reported_metadata")
        lines.append("- Claim safety note: metadata only; no artifact execution or capability validation")
        lines.append("")

    lines.append("## Claim Safety Note")
    lines.append("")
    lines.append("A Hugging Face metadata record confirms a public model listing or metadata item. It does not establish safety, license sufficiency, benchmark validity, production readiness, or actual capability.")
    lines.append("")
    return "\n".join(lines)


def write_outputs(raw_data: bytes, source_url: str, limit: int) -> FetchResult:
    retrieved_at_utc, slug = utc_now_slug()
    day = slug[:8]
    day_dir = REPORT_ROOT / f"{day[:4]}-{day[4:6]}-{day[6:8]}"
    raw_dir = day_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    raw_sha256 = sha256_bytes(raw_data)
    raw_path = raw_dir / f"huggingface_metadata_{slug}.json"
    summary_path = day_dir / "ai_models_huggingface_metadata.md"

    payload = json.loads(raw_data.decode("utf-8"))
    records = model_records(payload)

    raw_path.write_bytes(raw_data)
    summary_path.write_text(build_summary(records, raw_sha256, source_url, retrieved_at_utc, raw_path, limit), encoding="utf-8")

    return FetchResult(retrieved_at_utc, source_url, raw_sha256, raw_path, summary_path, len(records))


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch Hugging Face public model metadata.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--sort", default="lastModified")
    parser.add_argument("--direction", default="-1")
    parser.add_argument("--search", default=None)
    args = parser.parse_args()

    if args.limit < 1:
        print("FAIL --limit must be >= 1")
        return 1

    source_url = build_url(args.limit, args.sort, args.direction, args.search)

    print("=== Hugging Face Metadata Fetch ===")
    print(f"source_url: {source_url}")
    print("mode: dry-run" if args.dry_run else "mode: live-fetch")
    print("safety: metadata only; no model download or execution")

    if args.dry_run:
        print("PASS dry-run configuration")
        print("No network calls performed.")
        print("No files written.")
        return 0

    try:
        raw_data = fetch_bytes(source_url)
        result = write_outputs(raw_data, source_url, args.limit)
    except urllib.error.URLError as exc:
        print(f"FAIL network error fetching Hugging Face metadata: {exc}")
        return 2
    except json.JSONDecodeError as exc:
        print(f"FAIL invalid JSON from Hugging Face metadata: {exc}")
        return 3
    except Exception as exc:
        print(f"FAIL unexpected error: {exc}")
        return 4

    print(f"PASS fetched records: {result.record_count}")
    print(f"retrieved_at_utc: {result.retrieved_at_utc}")
    print(f"raw_sha256: {result.raw_sha256}")
    print(f"raw_path: {result.raw_path}")
    print(f"summary_path: {result.summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
