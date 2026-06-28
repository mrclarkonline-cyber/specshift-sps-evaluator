#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

USGS_4_5_DAY_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson"
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
    iso = now.isoformat().replace("+00:00", "Z")
    slug = now.strftime("%Y%m%dT%H%M%SZ")
    return iso, slug


def fetch_bytes(url: str, timeout: int = 30) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "SpecShiftLabsResearchWorkstation/0.1 ben@specshiftlabs.com",
            "Accept": "application/geo+json, application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_get(obj: dict[str, Any], key: str, default: str = "") -> str:
    value = obj.get(key, default)
    if value is None:
        return default
    return str(value).strip()


def epoch_ms_to_utc(value: Any) -> str:
    if value is None:
        return "unknown"
    try:
        ms = int(value)
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat().replace("+00:00", "Z")
    except Exception:
        return "unknown"


def sorted_features(payload: dict[str, Any]) -> list[dict[str, Any]]:
    features = payload.get("features", [])
    if not isinstance(features, list):
        raise ValueError("USGS payload field 'features' is not a list")

    valid = [f for f in features if isinstance(f, dict)]

    def sort_key(item: dict[str, Any]) -> float:
        props = item.get("properties", {})
        if not isinstance(props, dict):
            return 0.0
        try:
            return float(props.get("time", 0) or 0)
        except Exception:
            return 0.0

    return sorted(valid, key=sort_key, reverse=True)


def coordinates_for(feature: dict[str, Any]) -> str:
    geom = feature.get("geometry", {})
    if not isinstance(geom, dict):
        return "unknown"
    coords = geom.get("coordinates", [])
    if not isinstance(coords, list) or len(coords) < 2:
        return "unknown"

    lon = coords[0]
    lat = coords[1]
    depth = coords[2] if len(coords) > 2 else "unknown"
    return f"lat={lat}, lon={lon}, depth_km={depth}"


def build_summary(
    payload: dict[str, Any],
    raw_sha256: str,
    source_url: str,
    retrieved_at_utc: str,
    raw_path: Path,
    limit: int,
) -> str:
    features = sorted_features(payload)
    metadata = payload.get("metadata", {})
    if not isinstance(metadata, dict):
        metadata = {}

    title = safe_get(metadata, "title", "USGS Earthquake Feed")
    generated = epoch_ms_to_utc(metadata.get("generated"))
    count = len(features)

    lines: list[str] = []
    lines.append("# USGS Earthquake GeoJSON Digest")
    lines.append("")
    lines.append(f"Retrieved at UTC: {retrieved_at_utc}")
    lines.append(f"Source: {source_url}")
    lines.append(f"Feed title: {title}")
    lines.append(f"USGS generated time: {generated}")
    lines.append(f"Raw payload SHA256: {raw_sha256}")
    lines.append(f"Raw payload path: {raw_path}")
    lines.append(f"Record count: {count}")
    lines.append("")
    lines.append("## Safety Boundary")
    lines.append("")
    lines.append("This digest is official public geophysical telemetry for situational awareness.")
    lines.append("")
    lines.append("Do not infer cause, intent, prediction, infrastructure impact, or emergency action from this feed alone. USGS earthquake records may be preliminary and can be revised.")
    lines.append("")
    lines.append("## Latest Earthquake Records")
    lines.append("")

    for idx, feature in enumerate(features[:limit], start=1):
        props = feature.get("properties", {})
        if not isinstance(props, dict):
            props = {}

        event_id = safe_get(feature, "id", "unknown")
        place = safe_get(props, "place", "unknown")
        magnitude = safe_get(props, "mag", "unknown")
        event_time = epoch_ms_to_utc(props.get("time"))
        updated_time = epoch_ms_to_utc(props.get("updated"))
        status = safe_get(props, "status", "unknown")
        alert = safe_get(props, "alert", "unknown")
        tsunami = safe_get(props, "tsunami", "unknown")
        event_type = safe_get(props, "type", "earthquake")
        detail = safe_get(props, "detail", "")
        coords = coordinates_for(feature)

        lines.append(f"### {idx}. {event_id}")
        lines.append("")
        lines.append(f"- Type: {event_type}")
        lines.append(f"- Place: {place}")
        lines.append(f"- Magnitude: {magnitude}")
        lines.append(f"- Coordinates: {coords}")
        lines.append(f"- Event time UTC: {event_time}")
        lines.append(f"- Updated time UTC: {updated_time}")
        lines.append(f"- USGS status: {status}")
        lines.append(f"- USGS alert: {alert}")
        lines.append(f"- Tsunami flag: {tsunami}")
        if detail:
            lines.append(f"- USGS detail URL: {detail}")
        lines.append("- Uncertainty label: official_telemetry_preliminary_possible")
        lines.append("- Source tier: tier_1_authoritative")
        lines.append("")

    lines.append("## Claim Safety Note")
    lines.append("")
    lines.append("A USGS feed item confirms that USGS reported an earthquake event record. It does not by itself establish final magnitude, final impact, cause, risk to a specific location, or required action. Use official emergency guidance for safety decisions.")
    lines.append("")

    return "\n".join(lines)


def write_outputs(raw_data: bytes, limit: int) -> FetchResult:
    retrieved_at_utc, slug = utc_now_slug()
    day = slug[:8]
    day_dir = REPORT_ROOT / f"{day[:4]}-{day[4:6]}-{day[6:8]}"
    raw_dir = day_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    raw_sha256 = sha256_bytes(raw_data)
    raw_path = raw_dir / f"usgs_earthquake_{slug}.geojson"
    summary_path = day_dir / "earth_hazards_usgs_earthquake.md"

    payload = json.loads(raw_data.decode("utf-8"))
    features = sorted_features(payload)

    raw_path.write_bytes(raw_data)
    summary = build_summary(
        payload=payload,
        raw_sha256=raw_sha256,
        source_url=USGS_4_5_DAY_URL,
        retrieved_at_utc=retrieved_at_utc,
        raw_path=raw_path,
        limit=limit,
    )
    summary_path.write_text(summary, encoding="utf-8")

    return FetchResult(
        retrieved_at_utc=retrieved_at_utc,
        source_url=USGS_4_5_DAY_URL,
        raw_sha256=raw_sha256,
        raw_path=raw_path,
        summary_path=summary_path,
        record_count=len(features),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch USGS Earthquake GeoJSON for public geophysical awareness.")
    parser.add_argument("--dry-run", action="store_true", help="Validate configuration without network fetch.")
    parser.add_argument("--limit", type=int, default=10, help="Number of latest earthquake records to summarize.")
    args = parser.parse_args()

    print("=== USGS Earthquake Fetch ===")
    print(f"source_url: {USGS_4_5_DAY_URL}")
    print("mode: dry-run" if args.dry_run else "mode: live-fetch")
    print("safety: public geophysical awareness only")

    if args.limit < 1:
        print("FAIL --limit must be >= 1")
        return 1

    if args.dry_run:
        print("PASS dry-run configuration")
        print("No network calls performed.")
        print("No files written.")
        return 0

    try:
        raw_data = fetch_bytes(USGS_4_5_DAY_URL)
        result = write_outputs(raw_data, args.limit)
    except urllib.error.URLError as exc:
        print(f"FAIL network error fetching USGS feed: {exc}")
        return 2
    except json.JSONDecodeError as exc:
        print(f"FAIL invalid JSON/GeoJSON from USGS feed: {exc}")
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
