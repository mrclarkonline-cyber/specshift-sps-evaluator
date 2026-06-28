#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

NOAA_ALERTS_URL = "https://api.weather.gov/alerts/active"
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


def alert_features(payload: dict[str, Any]) -> list[dict[str, Any]]:
    features = payload.get("features", [])
    if not isinstance(features, list):
        raise ValueError("NOAA payload field 'features' is not a list")
    return [f for f in features if isinstance(f, dict)]


def build_summary(payload: dict[str, Any], raw_sha256: str, source_url: str, retrieved_at_utc: str, raw_path: Path, limit: int) -> str:
    features = alert_features(payload)
    lines: list[str] = []
    lines.append("# NOAA/NWS Active Alert Digest")
    lines.append("")
    lines.append(f"Retrieved at UTC: {retrieved_at_utc}")
    lines.append(f"Source: {source_url}")
    lines.append(f"Raw payload SHA256: {raw_sha256}")
    lines.append(f"Raw payload path: {raw_path}")
    lines.append(f"Record count: {len(features)}")
    lines.append("")
    lines.append("## Safety Boundary")
    lines.append("")
    lines.append("This digest preserves official NOAA/NWS alert language for situational awareness only.")
    lines.append("")
    lines.append("Do not reinterpret severity, certainty, urgency, affected areas, or safety actions beyond the issuing agency text.")
    lines.append("")
    lines.append("## Latest NOAA/NWS Alerts")
    lines.append("")

    for idx, feature in enumerate(features[:limit], start=1):
        props = feature.get("properties", {})
        if not isinstance(props, dict):
            props = {}

        alert_id = safe_get(props, "id", safe_get(feature, "id", "unknown"))
        event = safe_get(props, "event", "unknown")
        area = safe_get(props, "areaDesc", "unknown")
        severity = safe_get(props, "severity", "unknown")
        certainty = safe_get(props, "certainty", "unknown")
        urgency = safe_get(props, "urgency", "unknown")
        status = safe_get(props, "status", "unknown")
        message_type = safe_get(props, "messageType", "unknown")
        effective = safe_get(props, "effective", "unknown")
        expires = safe_get(props, "expires", "unknown")
        sender_name = safe_get(props, "senderName", "unknown")
        headline = safe_get(props, "headline", "")
        instruction = safe_get(props, "instruction", "")

        lines.append(f"### {idx}. {event}")
        lines.append("")
        lines.append(f"- Alert ID: {alert_id}")
        lines.append(f"- Area: {area}")
        lines.append(f"- Severity: {severity}")
        lines.append(f"- Certainty: {certainty}")
        lines.append(f"- Urgency: {urgency}")
        lines.append(f"- Status: {status}")
        lines.append(f"- Message type: {message_type}")
        lines.append(f"- Effective: {effective}")
        lines.append(f"- Expires: {expires}")
        lines.append(f"- Sender: {sender_name}")
        if headline:
            lines.append(f"- Headline: {headline}")
        if instruction:
            lines.append(f"- Official instruction excerpt: {instruction[:700]}")
        lines.append("- Uncertainty label: official_alert_preserve_agency_language")
        lines.append("- Source tier: tier_1_authoritative")
        lines.append("")

    lines.append("## Claim Safety Note")
    lines.append("")
    lines.append("A NOAA/NWS alert item confirms an official alert record. It does not authorize reinterpretation of risk, geography, severity, or action beyond official emergency guidance.")
    lines.append("")
    return "\n".join(lines)


def write_outputs(raw_data: bytes, source_url: str, limit: int) -> FetchResult:
    retrieved_at_utc, slug = utc_now_slug()
    day = slug[:8]
    day_dir = REPORT_ROOT / f"{day[:4]}-{day[4:6]}-{day[6:8]}"
    raw_dir = day_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    raw_sha256 = sha256_bytes(raw_data)
    raw_path = raw_dir / f"noaa_alerts_{slug}.json"
    summary_path = day_dir / "earth_weather_noaa_alerts.md"

    payload = json.loads(raw_data.decode("utf-8"))
    features = alert_features(payload)

    raw_path.write_bytes(raw_data)
    summary_path.write_text(build_summary(payload, raw_sha256, source_url, retrieved_at_utc, raw_path, limit), encoding="utf-8")

    return FetchResult(retrieved_at_utc, source_url, raw_sha256, raw_path, summary_path, len(features))


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch NOAA/NWS active alerts for official public alert awareness.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    print("=== NOAA/NWS Alert Fetch ===")
    print(f"source_url: {NOAA_ALERTS_URL}")
    print("mode: dry-run" if args.dry_run else "mode: live-fetch")
    print("safety: preserve agency language; no impact overclaiming")

    if args.limit < 1:
        print("FAIL --limit must be >= 1")
        return 1

    if args.dry_run:
        print("PASS dry-run configuration")
        print("No network calls performed.")
        print("No files written.")
        return 0

    try:
        raw_data = fetch_bytes(NOAA_ALERTS_URL)
        result = write_outputs(raw_data, NOAA_ALERTS_URL, args.limit)
    except urllib.error.URLError as exc:
        print(f"FAIL network error fetching NOAA/NWS alerts: {exc}")
        return 2
    except json.JSONDecodeError as exc:
        print(f"FAIL invalid JSON from NOAA/NWS alerts: {exc}")
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
