import importlib.util
from pathlib import Path

MODULE_PATH = Path("tools/claim_logic/claim_logic_classifier.py")

def load_module():
    spec = importlib.util.spec_from_file_location("claim_logic_classifier", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_safe_denial_allows_risk_terms():
    module = load_module()
    result = module.classify_sentence("SpecShift does not provide production validation.")
    assert result["category"] == "SAFE_DENIAL"
    assert result["action"] == "ALLOW"

def test_safe_boundary_allows_human_adjudication():
    module = load_module()
    result = module.classify_sentence("Buyer retains human adjudication and final decisions.")
    assert result["category"] == "SAFE_BOUNDARY"
    assert result["action"] == "ALLOW"

def test_unsafe_certification_blocks():
    module = load_module()
    result = module.classify_sentence("We certify that your AI is compliant.")
    assert result["category"] == "UNSAFE_CERTIFICATION"
    assert result["action"] == "BLOCK_OR_REWRITE"

def test_unsafe_verdict_blocks():
    module = load_module()
    result = module.classify_sentence("Automated verdict: pass.")
    assert result["category"] == "UNSAFE_VERDICT"
    assert result["action"] == "BLOCK_OR_REWRITE"

def test_ambiguous_review_reviews():
    module = load_module()
    result = module.classify_sentence("Production validation may be relevant here.")
    assert result["category"] == "AMBIGUOUS_REVIEW"
    assert result["action"] == "REVIEW"
