import importlib.util
from pathlib import Path

MODULE_PATH = Path("tools/claim_logic/claim_logic_audit_gate.py")

def load_module():
    spec = importlib.util.spec_from_file_location("claim_logic_audit_gate", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_safe_non_claims_pass():
    module = load_module()
    text = Path("tests/fixtures/claim_logic/audit_gate/safe_non_claims.md").read_text(encoding="utf-8")
    result = module.scan_text(text)
    assert result["status"] == "pass"
    assert result["blocked_count"] == 0

def test_unsafe_assertions_fail():
    module = load_module()
    text = Path("tests/fixtures/claim_logic/audit_gate/unsafe_assertions.md").read_text(encoding="utf-8")
    result = module.scan_text(text)
    assert result["status"] == "fail"
    assert result["blocked_count"] >= 1

def test_ambiguous_review_mode():
    module = load_module()
    text = Path("tests/fixtures/claim_logic/audit_gate/ambiguous_review.md").read_text(encoding="utf-8")
    result = module.scan_text(text)
    assert result["status"] == "review"
    assert result["review_count"] >= 1

def test_ambiguous_fail_on_review_mode():
    module = load_module()
    text = Path("tests/fixtures/claim_logic/audit_gate/ambiguous_review.md").read_text(encoding="utf-8")
    result = module.scan_text(text, fail_on_review=True)
    assert result["status"] == "review_fail"
