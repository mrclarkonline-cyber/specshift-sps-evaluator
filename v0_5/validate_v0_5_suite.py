#!/usr/bin/env python3
"""
Validate Unknown-Domain Scaffold Adversarial Test Suite v0.5.

Internal validator only.
Not a benchmark.
Not a certification.
Not a compliance or safety tool.
"""

import json
import re
import sys
from pathlib import Path

REQUIRED_TOP = {
    "suite_metadata",
    "suite_name",
    "status",
    "description",
    "test_cases",
}

REQUIRED_METADATA = {
    "version",
    "generation_date",
    "source_planning_matrix_id",
    "status",
    "performance_claims",
}

REQUIRED_CASE_FIELDS = {
    "id",
    "category",
    "test_type",
    "system_role",
    "context",
    "adversarial_prompt",
    "target_failure_mode",
    "failure_column",
    "scoring_rubric",
}

OPTIONAL_CASE_FIELDS = {
    "expected_weak_response",
    "strong_response_criteria",
    "notes",
}

FORBIDDEN_TEXT_PATTERNS = [
    r"\bbenchmark\b",
    r"\bcertification\b",
    r"\bcertified\b",
    r"\bcompliance product\b",
    r"\bsecurity tool\b",
    r"\baudit replacement\b",
    r"\bdeployment-readiness\b",
    r"\bguarantee\b",
    r"\bvalidated benchmark\b",
    r"\bnamed model\b",
    r"\bvendor\b",
]

CONDITION_MARKERS = [
    "if ",
    "when ",
    "unless ",
    "without ",
    "fails if",
    "fails when",
    "invalid if",
    "invalid when",
]

RUBRIC_DIMS = [
    "provenance",
    "observable_anchor",
    "failure_column_quality",
    "proxy_honesty",
    "claim_boundary",
    "implementation_safety",
    "workflow_traceability",
    "human_review_trigger",
    "operational_impact",
    "recovery_path",
]

RUBRIC_SUBFIELDS = {
    "expected_behavior",
    "pass_condition",
    "fail_condition",
}

TEST_TYPES = {
    "adversarial_attack",
    "edge_case",
    "stress_test",
    "schema_integrity",
    "boundary_condition",
}

CONTROLLED_CATEGORIES = {
    "provenance_confusion",
    "decorative_math",
    "missing_failure_column",
    "proxy_collapse",
    "false_neutrality",
    "scope_overextension",
    "silent_policy_violation",
    "stale_data_as_current",
    "multi_system_state_mismatch",
    "false_final_state_claim",
    "rollback_failure",
    "ambiguous_handoff_ownership",
    "synthetic_data_drift",
    "upstream_payload_logic_override",
    "circular_validation_resource_exhaustion",
    "cross_jurisdictional_policy_collision",
    "latent_condition_decay",
    "analog_digital_fracture",
    "customary_authority_misalignment",
    "degraded_infrastructure_triage",
    "cross_cultural_distress_idiom",
    "professional_boundary_overreach",
    "moral_disagreement_shape",
    "unknown_domain_overclaim",
}

def fail(errors, message):
    errors.append(message)

def nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())

def has_condition_marker(text):
    lowered = text.lower()
    return any(marker in lowered for marker in CONDITION_MARKERS)

def scan_forbidden_text(obj):
    blob = json.dumps(obj, ensure_ascii=False).lower()
    hits = []
    for pattern in FORBIDDEN_TEXT_PATTERNS:
        if re.search(pattern, blob):
            hits.append(pattern)
    return hits

def validate(path):
    errors = []
    p = Path(path)
    if not p.exists():
        raise SystemExit(f"FAIL: file not found: {p}")

    data = json.loads(p.read_text(encoding="utf-8"))

    missing_top = REQUIRED_TOP - set(data)
    if missing_top:
        fail(errors, f"Missing top-level fields: {sorted(missing_top)}")

    if data.get("status") != "internal draft stress-test suite, not a validated benchmark":
        fail(errors, "status must equal: internal draft stress-test suite, not a validated benchmark")

    metadata = data.get("suite_metadata", {})
    if not isinstance(metadata, dict):
        fail(errors, "suite_metadata must be an object")
    else:
        missing_meta = REQUIRED_METADATA - set(metadata)
        if missing_meta:
            fail(errors, f"Missing suite_metadata fields: {sorted(missing_meta)}")
        if metadata.get("performance_claims") != "none":
            fail(errors, "suite_metadata.performance_claims must be 'none'")

    cases = data.get("test_cases")
    if not isinstance(cases, list):
        fail(errors, "test_cases must be a list")
        cases = []

    if len(cases) != 25:
        fail(errors, f"test_cases must contain exactly 25 cases, found {len(cases)}")

    ids = []
    prompts_normalized = []

    for i, case in enumerate(cases, start=1):
        prefix = f"case[{i}]"

        if not isinstance(case, dict):
            fail(errors, f"{prefix} must be an object")
            continue

        missing = REQUIRED_CASE_FIELDS - set(case)
        if missing:
            fail(errors, f"{prefix} missing required fields: {sorted(missing)}")

        forbidden_fields = set(case) - REQUIRED_CASE_FIELDS - OPTIONAL_CASE_FIELDS
        if forbidden_fields:
            fail(errors, f"{prefix} has unexpected fields: {sorted(forbidden_fields)}")

        cid = case.get("id")
        if not nonempty_string(cid):
            fail(errors, f"{prefix}.id must be non-empty string")
        else:
            ids.append(cid)

        category = case.get("category")
        if category not in CONTROLLED_CATEGORIES:
            fail(errors, f"{prefix}.category is not controlled value: {category!r}")

        test_type = case.get("test_type")
        if test_type not in TEST_TYPES:
            fail(errors, f"{prefix}.test_type is not controlled value: {test_type!r}")

        for field in [
            "system_role",
            "context",
            "adversarial_prompt",
            "target_failure_mode",
            "failure_column",
        ]:
            if not nonempty_string(case.get(field)):
                fail(errors, f"{prefix}.{field} must be non-empty string")

        prompt = case.get("adversarial_prompt", "")
        if nonempty_string(prompt):
            prompts_normalized.append(re.sub(r"\s+", " ", prompt.strip().lower()))

        failure_column = case.get("failure_column", "")
        if nonempty_string(failure_column) and not has_condition_marker(failure_column):
            fail(errors, f"{prefix}.failure_column lacks conditional/falsifiable marker")

        strong = case.get("strong_response_criteria")
        if strong is not None:
            if not isinstance(strong, list) or not all(nonempty_string(x) for x in strong):
                fail(errors, f"{prefix}.strong_response_criteria must be list of non-empty strings")
            if isinstance(strong, list):
                for j, criterion in enumerate(strong, start=1):
                    if len(criterion.split()) > 25:
                        fail(errors, f"{prefix}.strong_response_criteria[{j}] may not be atomic enough")

        weak = case.get("expected_weak_response")
        if weak is not None and not nonempty_string(weak):
            fail(errors, f"{prefix}.expected_weak_response must be non-empty string if present")

        rubric = case.get("scoring_rubric")
        if not isinstance(rubric, dict):
            fail(errors, f"{prefix}.scoring_rubric must be object")
        else:
            rubric_keys = set(rubric)
            if rubric_keys != set(RUBRIC_DIMS):
                fail(errors, f"{prefix}.scoring_rubric keys mismatch: {sorted(rubric_keys)}")
            for dim in RUBRIC_DIMS:
                entry = rubric.get(dim)
                if not isinstance(entry, dict):
                    fail(errors, f"{prefix}.scoring_rubric.{dim} must be object")
                    continue
                if set(entry) != RUBRIC_SUBFIELDS:
                    fail(errors, f"{prefix}.scoring_rubric.{dim} subfields mismatch: {sorted(entry)}")
                for sub in RUBRIC_SUBFIELDS:
                    if not nonempty_string(entry.get(sub)):
                        fail(errors, f"{prefix}.scoring_rubric.{dim}.{sub} must be non-empty string")

    if len(ids) != len(set(ids)):
        fail(errors, "Duplicate id values detected")

    if len(prompts_normalized) != len(set(prompts_normalized)):
        fail(errors, "Duplicate adversarial_prompt values detected after normalization")

    # Forbidden-claim scan with allowed internal disclosure/status carve-outs.
    # Required status/disclosure text must not trip the claim scanner.
    scan_copy = dict(data)
    scan_copy.pop("status", None)
    scan_copy.pop("suite_name", None)

    if isinstance(scan_copy.get("suite_metadata"), dict):
        meta = dict(scan_copy["suite_metadata"])
        meta.pop("status", None)
        scan_copy["suite_metadata"] = meta

    forbidden_hits = scan_forbidden_text(scan_copy)
    allowed_patterns = {
        r"\bbenchmark\b",
        r"\bvalidated benchmark\b",
    }
    filtered_hits = [hit for hit in forbidden_hits if hit not in allowed_patterns]
    if filtered_hits:
        fail(errors, f"Forbidden buyer-facing claim language detected: {filtered_hits}")

    return errors

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: validate_v0_5_suite.py path/to/v0_5_suite.json")

    errors = validate(sys.argv[1])
    if errors:
        print("Validation: FAIL")
        for err in errors:
            print(f"- {err}")
        raise SystemExit(1)

    print("Validation: PASS")

if __name__ == "__main__":
    main()
