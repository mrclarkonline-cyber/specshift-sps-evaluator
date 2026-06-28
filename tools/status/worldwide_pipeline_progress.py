#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

PIPELINES = [
    ("01", "WHO Disease Outbreak News", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("02", "ReliefWeb / OCHA", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("03", "GDACS", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch1_14_source_access_checked_records.jsonl", "source-access-checked"),
    ("04", "World Bank Open Data", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch1_14_source_access_checked_records.jsonl", "source-access-checked"),
    ("05", "IMF Data", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch1_14_source_access_checked_records.jsonl", "source-access-checked"),
    ("06", "EU Open Data Portal", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("07", "ECDC", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch1_14_source_access_checked_records.jsonl", "source-access-checked"),
    ("08", "BBC World Service RSS verification", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch1_14_source_access_checked_records.jsonl", "source-access-checked"),
    ("09", "Deutsche Welle RSS verification", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch1_14_source_access_checked_records.jsonl", "source-access-checked"),
    ("10", "Canada Open Government", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch1_14_source_access_checked_records.jsonl", "source-access-checked"),
    ("11", "data.gov.uk", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch1_14_source_access_checked_records.jsonl", "source-access-checked"),
    ("12", "data.gov.au", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch1_14_source_access_checked_records.jsonl", "source-access-checked"),
    ("13", "Copernicus EMS / Data Space", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("14", "ECMWF", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch1_14_source_access_checked_records.jsonl", "source-access-checked"),
    ("15", "ESA / EUMETSAT", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch15_28_source_access_checked_records.jsonl", "source-access-checked"),
    ("16", "JMA", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch15_28_source_access_checked_records.jsonl", "source-access-checked"),
    ("17", "JAXA", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("18", "Geonet NZ", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch15_28_source_access_checked_records.jsonl", "source-access-checked"),
    ("19", "Geoscience Australia", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch15_28_source_access_checked_records.jsonl", "source-access-checked"),
    ("20", "Smithsonian Global Volcanism Program", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch15_28_source_access_checked_records.jsonl", "source-access-checked"),
    ("21", "FAO GIEWS", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("22", "IAEA IEC", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("23", "Africa CDC", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch15_28_source_access_checked_records.jsonl", "source-access-checked"),
    ("24", "PAHO", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch15_28_source_access_checked_records.jsonl", "source-access-checked"),
    ("25", "AHA Centre", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("26", "BMKG Indonesia", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch15_28_source_access_checked_records.jsonl", "source-access-checked"),
    ("27", "Singapore NEA", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch15_28_source_access_checked_records.jsonl", "source-access-checked"),
    ("28", "INEGI", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch15_28_source_access_checked_records.jsonl", "source-access-checked"),
    ("29", "ECLAC", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("30", "SSN Mexico", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch29_42_source_access_checked_records.jsonl", "source-access-checked"),
    ("31", "INPE Brazil", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch29_42_source_access_checked_records.jsonl", "source-access-checked"),
    ("32", "SERNAGEOMIN Chile", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch29_42_source_access_checked_records.jsonl", "source-access-checked"),
    ("33", "CDEMA", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("34", "SICA", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("35", "Reuters verification", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("36", "AFP verification", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch29_42_source_access_checked_records.jsonl", "source-access-checked"),
    ("37", "Al Jazeera", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch29_42_source_access_checked_records.jsonl", "source-access-checked"),
    ("38", "NHK World", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch29_42_source_access_checked_records.jsonl", "source-access-checked"),
    ("39", "Kyodo", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("40", "Yonhap", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch29_42_source_access_checked_records.jsonl", "source-access-checked"),
    ("41", "PTI", "memory_layer/wiki/operator_memory/worldwide_validated/phase2_batch29_42_source_access_checked_records.jsonl", "source-access-checked"),
    ("42", "PIB India", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("43", "Xinhua", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("44", "TASS", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("45", "OECD", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("46", "BIS", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("47", "IEA", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("48", "Global Fishing Watch", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("49", "IMO", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("50", "NSIDC", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("51", "SCAR / COMNAP", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("52", "Arctic Council / AMAP", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("53", "National Gazettes", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("54", "National Statistical Offices", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("55", "Multi-Country Contradiction Detector", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
    ("56", "Global anomaly flagger", "memory_layer/wiki/operator_memory/worldwide_implemented/phase2_all_implemented_records.jsonl", "implemented"),
]

STATUS_PROGRESS = {
    "registered": 20.0,
    "dry-run": 40.0,
    "configured": 60.0,
    "implemented": 80.0,
    "source-access-checked": 90.0,
    "validated": 100.0,
}


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records


def norm_num(value: object) -> str:
    try:
        return f"{int(value):02d}"
    except Exception:
        return str(value).zfill(2)


def find_record(num: str, name: str, source_path: str, expected: str) -> dict | None:
    records = load_jsonl(Path(source_path))
    target_num = norm_num(num)
    target_name = name.strip().lower()
    target_status = expected.strip().lower()

    for rec in records:
        rec_num = norm_num(rec.get("pipeline_number", rec.get("pipeline_id", "")))
        rec_name = str(rec.get("name", "")).strip().lower()
        rec_status = str(rec.get("status", "")).strip().lower()

        if rec_num == target_num and rec_name == target_name and rec_status == target_status:
            return rec

    return None


def score_for_record(rec: dict | None, expected: str) -> float:
    if not rec:
        return 0.0

    status = str(rec.get("status", expected)).strip().lower()
    status_score = STATUS_PROGRESS.get(status, 0.0)

    try:
        record_score = float(rec.get("phase_progress", status_score))
    except Exception:
        record_score = status_score

    return max(status_score, record_score)


def main() -> None:
    total = len(PIPELINES)
    registered = 0
    configured = 0
    implemented = 0
    score_sum = 0.0

    print("Worldwide Phase 2 pipeline status")
    print("=" * 71)
    print()

    for num, name, source_path, expected in PIPELINES:
        rec = find_record(num, name, source_path, expected)
        score = score_for_record(rec, expected)
        score_sum += score

        if score >= 20.0:
            registered += 1
        if score >= 60.0:
            configured += 1
        if score >= 80.0:
            implemented += 1

        print(f"{num}. [{expected.upper()}] {name}")
        print(f"    {source_path}")
        print(f"    Phase progress: {score:.1f}%")

    overall = score_sum / total if total else 0.0

    print()
    print(f"Worldwide expansion registration progress: {registered}/{total} = {(registered / total * 100.0 if total else 0.0):.1f}%")
    print(f"Worldwide expansion configuration progress: {configured}/{total} = {(configured / total * 100.0 if total else 0.0):.1f}%")
    print(f"Worldwide expansion implementation progress: {implemented}/{total} = {(implemented / total * 100.0 if total else 0.0):.1f}%")
    print(f"Overall Phase 2 progress score: {overall:.1f}%")
    print()
    print("Next worldwide build group:")
    if implemented == total:
        print("All worldwide Phase 2 pipelines are implemented at the registry/tracking layer.")
        print("Next: validate adapters/source access in bounded batches before claiming live ingestion.")
    else:
        for num, name, _source_path, _expected in PIPELINES:
            print(f"{int(num)}. {name}")


if __name__ == "__main__":
    main()
